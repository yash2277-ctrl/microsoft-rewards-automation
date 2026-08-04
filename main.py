import json
import logging
import time
from datetime import datetime
from rewards_automation_playwright import RewardsAutomation

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("config.json not found!")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing config.json: {str(e)}")
        return None

def print_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║     Microsoft Rewards Automation Tool               ║
    ║     Multi-Profile Points Collector                  ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    """Main automation runner"""
    print_banner()
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Failed to load configuration. Please check config.json")
        return
    
    profiles = config.get('profiles', [])
    settings = config.get('settings', {})
    
    if not profiles:
        print("❌ No profiles configured in config.json")
        return
    
    print(f"📋 Loaded {len(profiles)} profiles")
    print(f"⚙️  Settings: Headless={settings.get('headless', False)}, "
          f"Wait Time={settings.get('wait_time', 3)}s\n")
    
    # Confirm start
    print("Ready to start automation for the following profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"  {i}. {profile['name']} - "
              f"{profile['pc_searches']} PC + {profile['mobile_searches']} Mobile searches")
    
    print("\n▶️  Starting automation in 3 seconds...")
    time.sleep(3)
    
    # Process each profile
    total_profiles = len(profiles)
    successful = 0
    failed = 0
    
    for i, profile in enumerate(profiles, 1):
        print(f"\n{'#'*60}")
        print(f"Processing Profile {i}/{total_profiles}: {profile['name']}")
        print(f"{'#'*60}\n")
        
        try:
            automation = RewardsAutomation(profile, settings)
            if automation.run_automation():
                successful += 1
                print(f"✅ Successfully completed automation for {profile['name']}")
            else:
                failed += 1
                print(f"⚠️  Automation completed with warnings for {profile['name']}")
            
            # Wait between profiles
            if i < total_profiles:
                wait_time = 10
                print(f"\n⏳ Waiting {wait_time} seconds before next profile...")
                time.sleep(wait_time)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Automation interrupted by user")
            break
        except Exception as e:
            failed += 1
            logging.error(f"Error processing profile {profile['name']}: {str(e)}")
            print(f"❌ Error processing {profile['name']}")
    
    # Final summary
    print(f"\n{'='*60}")
    print("AUTOMATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Profiles: {total_profiles}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    print("📊 Check 'rewards_automation.log' for detailed logs")
    print("\n✨ Automation finished! Have a great day!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program terminated by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error occurred. Check logs for details.")
