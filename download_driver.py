import requests
import zipfile
import os
import sys

def download_edge_driver():
    """Download Edge WebDriver for version 150"""
    
    edge_version = "150.0.4078.48"
    driver_url = f"https://msedgedriver.azureedge.net/{edge_version}/edgedriver_win64.zip"
    
    print(f"Downloading Edge WebDriver for version {edge_version}...")
    
    try:
        # Download the driver
        response = requests.get(driver_url, timeout=30)
        response.raise_for_status()
        
        # Save zip file
        zip_path = "edgedriver.zip"
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        print("Download complete! Extracting...")
        
        # Extract the driver
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Clean up zip file
        os.remove(zip_path)
        
        print("✅ Edge WebDriver installed successfully!")
        print(f"Driver location: {os.path.abspath('msedgedriver.exe')}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading driver: {str(e)}")
        return False

if __name__ == "__main__":
    download_edge_driver()
