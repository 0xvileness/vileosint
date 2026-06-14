Vile OSINT Advanced Open Source Intelligence (OSINT) tool for email analysis, social media scraping, and phone number investigation.

Email Lookup:

Syntax Validation: Validates email format and structure

MX Record Check: Verifies domain mail exchange records

Disposable Email Detection: Identifies temporary email services

Breach Database Check: Searches HaveIBeenPwned for data breaches

Gravatar Profile Lookup: Checks for Gravatar profiles

GitHub Account Search: Finds GitHub users associated with email

Social Media Search: Generates search URLs across multiple platforms

Email Verification: Uses Hunter.io API for email validation

Pastebin Scanning: Checks for email exposure in public pastes

Name Extraction: Intelligently extracts names from email addresses

Social Deep Dive: Comprehensive social media analysis

Entity Relationship Graphing: visualizations


Phone Number OSINT:

Number Validation: Validates phone number format and existence

Carrier Identification: Identifies mobile network carriers

Geolocation: Determines approximate geographical location

Timezone Detection: Identifies relevant timezones

Google Dorking: Generates search queries for OSINT investigations

Also Including user name osint:

Installation Dependencies:

pip install requests dnspython pandas phonenumbers reportlab matplotlib networkx pillow beautifulsoup4 fake-useragent


API Keys Configuration

For full functionality, obtain and configure these API keys:
HaveIBeenPwned API

Visit https://haveibeenpwned.com/API/Key

Sign up for an API key And Configuration:

Add to script: HIBP_API_KEY = "your_api_key_here"

Hunter.io API

Visit https://hunter.io/api-keys

Create account and generate API key

Add to script: HUNTER_IO_API_KEY = "your_api_key_here"



