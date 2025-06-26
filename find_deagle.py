import time
import re
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
import subprocess
import os
import psutil

class SteamMarketBlueGemScanner:
    def __init__(self):
        self.base_url = "https://steamcommunity.com/market"
        self.driver = None
        self.setup_driver()
    
    def kill_chrome_processes(self):
        """
        Kill all Chrome processes to ensure clean start
        """
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'chrome' in proc.info['name'].lower():
                    try:
                        proc.kill()
                    except:
                        pass
            time.sleep(3)
            print("Killed existing Chrome processes")
        except:
            print("Could not kill Chrome processes automatically")
    
    def setup_driver(self):
        """
        Setup Chrome driver with your profile using a simpler approach
        """
        print("Setting up Chrome with your profile...")
        
        # Kill existing Chrome processes
        self.kill_chrome_processes()
        
        chrome_options = Options()
        
        # Find your Chrome profile path
        import platform
        system = platform.system()
        username = os.getenv('USERNAME') or os.getenv('USER')
        
        if system == "Windows":
            profile_path = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"
        elif system == "Darwin":  # macOS
            profile_path = f"/Users/{username}/Library/Application Support/Google/Chrome"
        else:  # Linux
            profile_path = f"/home/{username}/.config/google-chrome"
        
        # Use a copy approach that actually works
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp(prefix="chrome_temp_")
        
        try:
            # Copy only essential files
            if os.path.exists(profile_path):
                default_profile = os.path.join(profile_path, "Default")
                temp_default = os.path.join(temp_dir, "Default")
                
                if os.path.exists(default_profile):
                    os.makedirs(temp_default, exist_ok=True)
                    
                    # Copy essential files only
                    essential_files = [
                        "Preferences",
                        "Secure Preferences", 
                        "Extensions",
                        "Local Storage",
                        "Cookies",
                        "Login Data"
                    ]
                    
                    for file_name in essential_files:
                        src = os.path.join(default_profile, file_name)
                        dst = os.path.join(temp_default, file_name)
                        if os.path.exists(src):
                            try:
                                if os.path.isdir(src):
                                    shutil.copytree(src, dst, dirs_exist_ok=True)
                                else:
                                    shutil.copy2(src, dst)
                            except:
                                pass
                
                chrome_options.add_argument(f"--user-data-dir={temp_dir}")
                print(f"Using temporary profile: {temp_dir}")
            else:
                print("Profile not found, using default")
                
        except Exception as e:
            print(f"Profile copy failed: {e}, using default profile")
        
        # Essential Chrome options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions-file-access-check")
        chrome_options.add_argument("--disable-extensions-http-throttling")
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-default-apps")
        
        # Don't disable extensions
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Chrome started successfully!")
            print("Please install CSFloat Market Checker extension if not already installed")
            
            # Give time for extensions to load
            time.sleep(5)
            
            # Navigate to Chrome Extensions page to help user
            print("Opening Chrome extensions page...")
            self.driver.get("chrome://extensions/")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"Error starting Chrome: {e}")
            return False
    
    def wait_for_user_setup(self):
        """
        Wait for user to install CSFloat and navigate to Steam Market
        """
        print("\n" + "="*80)
        print("SETUP INSTRUCTIONS")
        print("="*80)
        print("1. Chrome has opened - you should see the Extensions page")
        print("2. If CSFloat is not installed:")
        print("   - Go to Chrome Web Store")
        print("   - Search for 'CSFloat Market Checker'") 
        print("   - Install the extension")
        print("3. Navigate to Steam Market and login if needed")
        print("4. Go to: https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Field-Tested%29")
        print("5. Wait for CSFloat to load and show blue percentages")
        print("6. Press Enter here when ready...")
        print("="*80)
        
        input("Press Enter when you're on Steam Market page with CSFloat data visible: ")
        
        # Navigate to the first page to ensure we're on the right site
        print("Navigating to Steam Market page...")
        try:
            market_url = "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Field-Tested%29"
            self.driver.get(market_url)
            time.sleep(5)
            print("Successfully navigated to Steam Market")
        except Exception as e:
            print(f"Error navigating to Steam Market: {e}")
            return False
        
        return True
    
    def extract_blue_gem_data_from_text(self, text_content):
        """
        Extract data from visible text content
        """
        data = {
            'pattern': None,
            'float': None,
            'blue_front': None,
            'blue_back': None,
            'price': None
        }
        
        # Extract Paint Seed
        pattern_matches = re.findall(r'Paint\s*Seed:\s*(\d+)', text_content, re.IGNORECASE)
        if pattern_matches:
            data['pattern'] = int(pattern_matches[0])
        
        # Extract Float
        float_matches = re.findall(r'Float:\s*(\d+\.\d+)', text_content, re.IGNORECASE)
        if float_matches:
            data['float'] = float(float_matches[0])
        
        # Extract Blue percentages - multiple formats
        blue_patterns = [
            r'Blue\s*\(Front\s*/\s*Back\):\s*(\d+\.?\d*)%\s*/\s*(\d+\.?\d*)%',
            r'Blue.*?(\d+\.?\d*)%.*?/.*?(\d+\.?\d*)%',
            r'(\d+\.?\d*)%\s*/\s*(\d+\.?\d*)%'
        ]
        
        for pattern in blue_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                try:
                    data['blue_front'] = float(matches[0][0])
                    data['blue_back'] = float(matches[0][1])
                    break
                except:
                    continue
        
        # Extract price
        price_matches = re.findall(r'\$[\d,]+\.\d+', text_content)
        if price_matches:
            data['price'] = price_matches[0]
        
        return data
    
    def scan_current_page(self):
        """
        Scan the current page for listings
        """
        try:
            # Wait for page to load
            time.sleep(3)
            
            # Get all text content from the page
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Try to find listing elements
            selectors = [
                '.market_listing_row_link',
                '.market_listing_row',
                '[id*="listing"]'
            ]
            
            listings = []
            for selector in selectors:
                try:
                    found_listings = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_listings:
                        listings = found_listings
                        print(f"Found {len(listings)} listings")
                        break
                except:
                    continue
            
            if not listings:
                print("No listings found with standard selectors")
                print("Checking page content...")
                
                if "Paint Seed:" in page_text:
                    print("Found CSFloat data in page!")
                    # Extract all data from page text
                    return [page_text]
                else:
                    print("No CSFloat data detected")
                    return []
            
            return listings
            
        except Exception as e:
            print(f"Error scanning page: {e}")
            return []
    
    def navigate_to_page_number(self, page_num):
        """
        Navigate to specific page number on Steam Market
        """
        try:
            start_pos = (page_num - 1) * 100
            
            # Use the correct Steam Market URL for Desert Eagle
            base_url = "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Field-Tested%29"
            new_url = f"{base_url}?start={start_pos}&count=100"
            
            print(f"Navigating to page {page_num}: {new_url}")
            self.driver.get(new_url)
            
            # Wait for page and CSFloat to load
            time.sleep(8)
            
            return True
            
        except Exception as e:
            print(f"Error navigating to page {page_num}: {e}")
            return False
    
    def scan_blue_gem_range(self, min_blue, max_blue, start_page=1, end_page=5):
        """
        Scan pages for Blue Gem items
        """
        found_items = []
        total_scanned = 0
        items_with_blue_data = 0
        
        print(f"Searching for Blue Gem: {min_blue}% - {max_blue}% (Front)")
        print(f"Page range: {start_page} - {end_page}")
        print("=" * 80)
        
        # Wait for user setup
        if not self.wait_for_user_setup():
            return [], 0, 0
        
        for page in range(start_page, end_page + 1):
            print(f"\nScanning page {page}...")
            
            # Navigate to page (except first page)
            if page > start_page:
                if not self.navigate_to_page_number(page):
                    continue
            
            # Scan current page
            listings = self.scan_current_page()
            
            if not listings:
                print("No listings found on this page")
                continue
            
            page_found = 0
            page_with_blue = 0
            
            # Process listings
            for i, listing in enumerate(listings):
                total_scanned += 1
                
                # Extract data
                if isinstance(listing, str):
                    # Page text approach
                    item_data = self.extract_blue_gem_data_from_text(listing)
                else:
                    # Element approach
                    try:
                        listing_text = listing.text
                        item_data = self.extract_blue_gem_data_from_text(listing_text)
                    except:
                        continue
                
                # Debug output
                if item_data['pattern'] or item_data['blue_front'] or item_data['float']:
                    print(f"  Item: Pattern={item_data['pattern']}, Blue={item_data['blue_front']}, Float={item_data['float']}")
                
                if item_data['blue_front'] is not None:
                    items_with_blue_data += 1
                    page_with_blue += 1
                    
                    # Check range
                    if min_blue <= item_data['blue_front'] <= max_blue:
                        item_data['page'] = page
                        item_data['position'] = (page - 1) * 100 + i + 1
                        found_items.append(item_data)
                        page_found += 1
                        
                        blue_back_str = f"/{item_data['blue_back']:.1f}%" if item_data['blue_back'] else ""
                        print(f"  *** FOUND! Blue: {item_data['blue_front']:.1f}%{blue_back_str} | Pattern: #{item_data['pattern']} | Price: {item_data['price']}")
            
            print(f"Page {page}: found {page_found} suitable from {page_with_blue} with Blue data")
            
            # Pause between pages
            if page < end_page:
                time.sleep(3)
        
        return found_items, total_scanned, items_with_blue_data
    
    def display_results(self, found_items, total_scanned, items_with_blue_data, min_blue, max_blue):
        """
        Display search results
        """
        print("\n" + "=" * 80)
        print("BLUE GEM SEARCH RESULTS")
        print("=" * 80)
        
        print(f"Total scanned: {total_scanned} items")
        if total_scanned > 0:
            print(f"With Blue Gem data: {items_with_blue_data} items ({items_with_blue_data/total_scanned*100:.1f}%)")
        print(f"Searched range: {min_blue}% - {max_blue}% Blue (Front)")
        
        if not found_items:
            print("No items found in specified Blue Gem range")
            return
        
        print(f"Found suitable items: {len(found_items)}")
        print()
        
        # Sort by Blue percentage
        found_items.sort(key=lambda x: x['blue_front'] or 0, reverse=True)
        
        print("FOUND ITEMS:")
        print("-" * 80)
        
        for i, item in enumerate(found_items, 1):
            blue_back_str = f"/{item['blue_back']:.1f}%" if item['blue_back'] else ""
            print(f"{i:2d}. Blue: {item['blue_front']:.1f}%{blue_back_str}")
            if item['pattern']:
                print(f"    Pattern: #{item['pattern']}")
            if item['price']:
                print(f"    Price: {item['price']}")
            if item['float']:
                print(f"    Float: {item['float']:.6f}")
            print(f"    Page: {item['page']}")
            print()
    
    def close(self):
        """
        Close browser
        """
        if self.driver:
            self.driver.quit()

def parse_blue_range(range_input):
    if '-' in range_input:
        try:
            min_blue, max_blue = map(float, range_input.split('-'))
            return min_blue, max_blue
        except ValueError:
            return None, None
    else:
        try:
            blue = float(range_input)
            return blue, blue
        except ValueError:
            return None, None

def parse_page_range(page_input):
    if '-' in page_input:
        try:
            start, end = map(int, page_input.split('-'))
            return start, end
        except ValueError:
            return None, None
    else:
        try:
            page = int(page_input)
            return page, page
        except ValueError:
            return None, None

def main():
    print("Steam Market Blue Gem Scanner for Desert Eagle | Heat Treated (FT)")
    print("Simplified version with manual setup")
    print("REQUIREMENTS:")
    print("1. pip install selenium webdriver-manager psutil")
    print("2. Chrome browser")
    print("=" * 80)
    
    scanner = None
    
    try:
        # Input ranges
        while True:
            try:
                blue_input = input("Enter Blue Gem % range (e.g., '45-100'): ").strip()
                min_blue, max_blue = parse_blue_range(blue_input)
                if min_blue is not None and 0 <= min_blue <= max_blue <= 100:
                    break
                print("Invalid range! Use format like '45-100' or '50'")
            except ValueError:
                print("Enter valid numbers")
        
        while True:
            try:
                pages_input = input("Enter page range (e.g., '69-71', default '1-3'): ").strip()
                if not pages_input:
                    start_page, end_page = 1, 3
                else:
                    start_page, end_page = parse_page_range(pages_input)
                    if start_page is None or start_page < 1 or end_page < start_page:
                        print("Invalid page range!")
                        continue
                break
            except ValueError:
                print("Enter valid numbers")
        
        # Start scanning
        print(f"\nStarting Chrome...")
        scanner = SteamMarketBlueGemScanner()
        
        found_items, total_scanned, items_with_blue_data = scanner.scan_blue_gem_range(
            min_blue, max_blue, start_page, end_page
        )
        scanner.display_results(found_items, total_scanned, items_with_blue_data, min_blue, max_blue)
        
    except KeyboardInterrupt:
        print("\nScanning interrupted")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if scanner:
            scanner.close()
    
    print("\nCompleted!")

if __name__ == "__main__":
    main()