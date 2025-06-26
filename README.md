CS2 Heat Treated Blue Gem Scanner
A Python tool for automatically scanning Steam Market listings to find Desert Eagle | Heat Treated (Field-Tested) skins with specific blue percentage patterns. This scanner integrates with the CSFloat Market Checker browser extension to identify high-blue Case Hardened patterns.

Features:
Automated Steam Market Scanning - Browse through multiple pages of Steam Market listings
Blue Percentage Filtering - Search for specific blue percentage ranges (e.g., 45-100%)
CSFloat Integration - Works with CSFloat Market Checker extension for accurate blue percentage data
Chrome Profile Support - Uses your existing Chrome profile with installed extensions
Detailed Results - Shows paint seed, float value, blue percentage, and price for found items
Rate Limiting - Built-in delays to respect Steam's rate limits

Prerequisites:
Python 3.7+
Google Chrome Browser
CSFloat Market Checker Extension - Install from Chrome Web Store

Install required Python packages:

bashpip install selenium webdriver-manager psutil beautifulsoup4 requests
Usage

Run the scanner:
bashpython find_deagle.py

Follow the setup instructions:
Chrome will automatically open to the extensions page
Ensure CSFloat Market Checker is installed and enabled
Navigate to the Steam Market page for Desert Eagle | Heat Treated (Field-Tested)
Wait for CSFloat data to load (you should see blue percentages)
Press Enter in the terminal when ready

Enter search parameters:
Blue percentage range (e.g., 45-100 for 45% to 100% blue)
Page range to scan (e.g., 1-5 to scan pages 1 through 5)

Review results:
The scanner will display found items with their blue percentages, paint seeds, float values, and prices
Items are sorted by blue percentage (highest first)

Example Output
BLUE GEM SEARCH RESULTS
================================================================================
Total scanned: 500 items
With Blue Gem data: 487 items (97.4%)
Searched range: 60.0% - 100.0% Blue (Front)
Found suitable items: 3

FOUND ITEMS:
--------------------------------------------------------------------------------
 1. Blue: 84.2%/12.3%
    Pattern: #321
    Price: $45.67
    Float: 0.234567
    Page: 2

 2. Blue: 78.9%/15.6%
    Pattern: #442
    Price: $38.92
    Float: 0.198765
    Page: 1
Configuration
Steam Market URL
The scanner is pre-configured for Desert Eagle | Heat Treated (Field-Tested). To scan other skins, modify the market_hash_name variable in the code.
Page Size
Steam Market displays 100 items per page by default. The scanner uses this setting for optimal performance.
Delays
Built-in delays between requests:
8 seconds between page loads
3 seconds between pages
Additional time for CSFloat data to load

How It Works:
Browser Automation: Uses Selenium to control Chrome with your existing profile
Extension Integration: Leverages CSFloat Market Checker for blue percentage data
Data Extraction: Parses page content to extract paint seeds, float values, and blue percentages
Filtering: Applies your specified blue percentage range to find matching items
Results Display: Presents found items in an organized format

Troubleshooting
Common Issues
CSFloat data not loading:
Ensure the extension is installed and enabled
Wait longer for the page to fully load
Check if you're logged into Steam

Chrome profile issues:
The scanner will create a temporary profile if it can't access your main profile
Make sure Chrome is completely closed before running the scanner

No listings found:
Verify you're on the correct Steam Market page
Check if Steam is experiencing issues
Try reducing the page range and blue percentage range

Error Messages:
No listings found: The page didn't load properly or CSFloat data is missing
Profile copy failed: Using default Chrome profile instead
Navigation error: Check your internet connection and Steam's status

Legal Notice:
This tool is for educational and personal use only. Users are responsible for:
Complying with Steam's Terms of Service
Respecting rate limits and not overloading Steam's servers
Using the tool responsibly and ethically

The developers are not responsible for any consequences resulting from the use of this tool.

License
This project is licensed under the MIT License - see the LICENSE file for details.
Disclaimer
This project is not affiliated with Valve Corporation, Steam, or CSFloat. All trademarks are property of their respective owners.
