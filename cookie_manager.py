import json
import os
import logging

class CookieManager:
    """Manage browser cookies for persistent login"""
    
    def __init__(self):
        self.cookie_dir = "cookies"
        if not os.path.exists(self.cookie_dir):
            os.makedirs(self.cookie_dir)
    
    def get_cookie_file(self, profile_name):
        """Get cookie file path for a profile"""
        safe_name = profile_name.replace(" ", "_").replace("/", "_")
        return os.path.join(self.cookie_dir, f"{safe_name}_cookies.json")
    
    def save_cookies(self, context, profile_name):
        """Save cookies from browser context"""
        try:
            cookies = context.cookies()
            cookie_file = self.get_cookie_file(profile_name)
            
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            logging.info(f"✓ Cookies saved for {profile_name}")
            return True
        except Exception as e:
            logging.error(f"Error saving cookies: {str(e)}")
            return False
    
    def load_cookies(self, context, profile_name):
        """Load cookies into browser context"""
        try:
            cookie_file = self.get_cookie_file(profile_name)
            
            if not os.path.exists(cookie_file):
                logging.info(f"No saved cookies found for {profile_name}")
                return False
            
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            
            context.add_cookies(cookies)
            logging.info(f"✓ Cookies loaded for {profile_name}")
            return True
        except Exception as e:
            logging.error(f"Error loading cookies: {str(e)}")
            return False
    
    def has_cookies(self, profile_name):
        """Check if cookies exist for a profile"""
        cookie_file = self.get_cookie_file(profile_name)
        return os.path.exists(cookie_file)
    
    def delete_cookies(self, profile_name):
        """Delete saved cookies for a profile"""
        try:
            cookie_file = self.get_cookie_file(profile_name)
            if os.path.exists(cookie_file):
                os.remove(cookie_file)
                logging.info(f"Cookies deleted for {profile_name}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error deleting cookies: {str(e)}")
            return False
