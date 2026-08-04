import time
import logging
import random
from playwright.sync_api import sync_playwright
from search_terms import SearchTermsGenerator
from cookie_manager import CookieManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rewards_automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class RewardsAutomation:
    """Microsoft Rewards automation handler using Playwright"""
    
    def __init__(self, profile_config, settings):
        self.profile_config = profile_config
        self.settings = settings
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.search_generator = SearchTermsGenerator()
        self.cookie_manager = CookieManager()
        
    def setup_browser(self, mobile=False):
        """Setup Edge browser with profile using Playwright"""
        try:
            self.playwright = sync_playwright().start()
            
            # Launch Edge browser
            self.browser = self.playwright.chromium.launch(
                channel="msedge",
                headless=self.settings.get('headless', False)
            )
            
            # Setup context options
            context_options = {
                "viewport": {"width": 375, "height": 812} if mobile else {"width": 1920, "height": 1080}
            }
            
            # Add mobile user agent if needed
            if mobile:
                context_options["user_agent"] = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
            
            # Create context
            self.context = self.browser.new_context(**context_options)
            
            # Load saved cookies if they exist
            profile_name = self.profile_config['name']
            cookies_loaded = self.cookie_manager.load_cookies(self.context, profile_name)
            
            self.page = self.context.new_page()
            
            logging.info(f"Browser initialized for profile: {self.profile_config['name']}")
            
            # If no cookies, need to login
            if not cookies_loaded:
                logging.warning(f"⚠️  No saved login for {profile_name}. Please sign in...")
                return "NEED_LOGIN"
            
            return True
            
        except Exception as e:
            logging.error(f"Error setting up browser: {str(e)}")
            return False
    
    def wait_for_login(self):
        """Wait for user to manually log in, then save cookies"""
        try:
            profile_name = self.profile_config['name']
            
            print(f"\n{'='*60}")
            print(f"🔐 LOGIN REQUIRED FOR: {profile_name}")
            print(f"{'='*60}")
            print("1. The browser is now open")
            print("2. Please SIGN IN to your Microsoft account")
            print("3. Go to https://rewards.microsoft.com to verify you're logged in")
            print("4. Once signed in, press Enter here to continue...")
            print(f"{'='*60}\n")
            
            # Navigate to Bing to help them login
            self.page.goto("https://www.bing.com")
            
            # Wait for user to login
            input("Press Enter after you've signed in to Microsoft account...")
            
            # Verify they're logged in by checking rewards page
            print("Verifying login...")
            self.page.goto("https://rewards.microsoft.com")
            time.sleep(3)
            
            # Save the cookies
            self.cookie_manager.save_cookies(self.context, profile_name)
            
            print(f"✅ Login saved for {profile_name}! This won't be needed again.\n")
            return True
            
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass
    
    def perform_search(self, search_term):
        """Perform a single Bing search"""
        try:
            self.page.goto("https://www.bing.com", wait_until="domcontentloaded")
            time.sleep(self.settings.get('wait_time', 2))
            
            # Try multiple search box selectors
            try:
                # Try the main search input
                search_box = self.page.locator('#sb_form_q').first
                search_box.wait_for(timeout=5000)
            except:
                # Fallback to other common selectors
                try:
                    search_box = self.page.locator('input[name="q"]').first
                    search_box.wait_for(timeout=5000)
                except:
                    search_box = self.page.locator('textarea[name="q"]').first
                    search_box.wait_for(timeout=5000)
            
            # Click to focus, then type
            search_box.click()
            search_box.fill(search_term)
            search_box.press("Enter")
            
            # Wait for results
            time.sleep(self.settings.get('search_delay', 2))
            logging.info(f"Search completed: {search_term}")
            return True
            
        except Exception as e:
            logging.error(f"Error performing search: {str(e)}")
            return False
    
    def complete_pc_searches(self):
        """Complete PC searches for the profile"""
        logging.info(f"Starting PC searches for {self.profile_config['name']}")
        
        setup_result = self.setup_browser(mobile=False)
        if setup_result == "NEED_LOGIN":
            if not self.wait_for_login():
                return False
        elif not setup_result:
            return False
        
        try:
            pc_count = self.profile_config.get('pc_searches', 30)
            search_terms = self.search_generator.get_search_terms(pc_count)
            
            for i, term in enumerate(search_terms, 1):
                logging.info(f"PC Search {i}/{pc_count}: {term}")
                self.perform_search(term)
                time.sleep(random.uniform(2, 4))
            
            logging.info(f"Completed {pc_count} PC searches")
            return True
            
        except Exception as e:
            logging.error(f"Error in PC searches: {str(e)}")
            return False
        finally:
            self.cleanup()
    
    def complete_mobile_searches(self):
        """Complete mobile searches for the profile"""
        logging.info(f"Starting mobile searches for {self.profile_config['name']}")
        
        setup_result = self.setup_browser(mobile=True)
        if setup_result == "NEED_LOGIN":
            if not self.wait_for_login():
                return False
        elif not setup_result:
            return False
        
        try:
            mobile_count = self.profile_config.get('mobile_searches', 20)
            search_terms = self.search_generator.get_search_terms(mobile_count)
            
            for i, term in enumerate(search_terms, 1):
                logging.info(f"Mobile Search {i}/{mobile_count}: {term}")
                self.perform_search(term)
                time.sleep(random.uniform(2, 4))
            
            logging.info(f"Completed {mobile_count} mobile searches")
            return True
            
        except Exception as e:
            logging.error(f"Error in mobile searches: {str(e)}")
            return False
        finally:
            self.cleanup()
    
    def run_automation(self):
        """Run complete automation for this profile"""
        logging.info(f"\n{'='*50}")
        logging.info(f"Starting automation for {self.profile_config['name']}")
        logging.info(f"{'='*50}\n")
        
        try:
            # Complete PC searches
            if self.complete_pc_searches():
                logging.info("✓ PC searches completed successfully")
            else:
                logging.warning("✗ PC searches failed")
            
            time.sleep(5)
            
            # Complete mobile searches
            if self.complete_mobile_searches():
                logging.info("✓ Mobile searches completed successfully")
            else:
                logging.warning("✗ Mobile searches failed")
            
            logging.info(f"\nAutomation completed for {self.profile_config['name']}\n")
            return True
            
        except Exception as e:
            logging.error(f"Error in automation: {str(e)}")
            return False
