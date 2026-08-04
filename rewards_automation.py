import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from search_terms import SearchTermsGenerator
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rewards_automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class RewardsAutomation:
    """Microsoft Rewards automation handler"""
    
    def __init__(self, profile_config, settings):
        self.profile_config = profile_config
        self.settings = settings
        self.driver = None
        self.search_generator = SearchTermsGenerator()
        self.ua = UserAgent()
        
    def setup_driver(self, mobile=False):
        """Setup Edge browser with profile"""
        try:
            edge_options = Options()
            
            # Use specific Edge profile - FIX: Use user-data-dir instead
            user_data_dir = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data")
            edge_options.add_argument(f"user-data-dir={user_data_dir}")
            edge_options.add_argument(f"--profile-directory={self.profile_config['edge_profile_name']}")
            
            # Set user agent for mobile simulation
            if mobile:
                mobile_ua = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
                edge_options.add_argument(f"user-agent={mobile_ua}")
                edge_options.add_argument("--window-size=375,812")
            
            # Additional options
            if self.settings.get('headless', False):
                edge_options.add_argument('--headless')
            
            edge_options.add_argument('--disable-blink-features=AutomationControlled')
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize driver without Service (let Selenium find driver automatically)
            self.driver = webdriver.Edge(options=edge_options)
            
            logging.info(f"Browser initialized for profile: {self.profile_config['name']}")
            return True
            
        except Exception as e:
            logging.error(f"Error setting up driver: {str(e)}")
            return False
    
    def perform_search(self, search_term):
        """Perform a single Bing search"""
        try:
            self.driver.get("https://www.bing.com")
            time.sleep(self.settings.get('wait_time', 3))
            
            # Find search box and enter term
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)
            
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
        
        if not self.setup_driver(mobile=False):
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
            if self.driver:
                self.driver.quit()
    
    def complete_mobile_searches(self):
        """Complete mobile searches for the profile"""
        logging.info(f"Starting mobile searches for {self.profile_config['name']}")
        
        if not self.setup_driver(mobile=True):
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
            if self.driver:
                self.driver.quit()
    
    def check_rewards_page(self):
        """Check Microsoft Rewards page for status"""
        try:
            self.driver.get("https://rewards.microsoft.com")
            time.sleep(5)
            
            # Check if we can access rewards page
            if "rewards.microsoft.com" in self.driver.current_url:
                logging.info("Successfully accessed Rewards page")
                return True
            return False
            
        except Exception as e:
            logging.error(f"Error checking rewards page: {str(e)}")
            return False
    
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
