import re
import requests
import dns.resolver
import hashlib
import logging
import threading
import pandas as pd
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import time
import webbrowser
import random
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
from collections import defaultdict
import socket
import whois
from datetime import datetime
import concurrent.futures
from bs4 import BeautifulSoup
import fake_useragent

# Color codes for terminal output
NEON_GREEN = '\033[92m'
NEON_RED = '\033[91m'
NEON_BLUE = '\033[94m'
NEON_CYAN = '\033[96m'
NEON_YELLOW = '\033[93m'
NEON_WHITE = '\033[97m'
NEON_MAGENTA = '\033[95m'
NEON_BOLD_RED = '\033[1;91m'
NEON_BOLD_GREEN = '\033[1;92m'
NEON_BOLD_CYAN = '\033[1;96m'
NEON_BOLD_YELLOW = '\033[1;93m'
NEON_BOLD_WHITE = '\033[1;97m'
NEON_RESET = '\033[0m'

# API Keys (Replace with your own)
HIBP_API_KEY = ""  # HaveIBeenPwned API key
HUNTER_IO_API_KEY = ""  # Hunter.io API key
GOOGLE_CSE_ID = ""  # Google Custom Search Engine ID
GOOGLE_API_KEY = ""  # Google API key

# Configuration
THREADS = 5
TIMEOUT = 15
USER_AGENT = fake_useragent.UserAgent().random

# 1. Welcome Logo and Description -----------------------------------------------

def print_welcome():
    logo = f"""{NEON_GREEN}
 ██▒   █▓ ██▓ ██▓    ▓█████     ▒█████    ██████  ██▓ ███▄    █ ▄▄▄█████▓
▓██░   █▒▓██▒▓██▒    ▓█   ▀    ▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
 ▓██  █▒░▒██▒▒██░    ▒███      ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
  ▒██ █░░░██░▒██░    ▒▓█  ▄    ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
   ▒▀█░  ░██░░██████▒░▒████▒   ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
   ░ ▐░  ░▓  ░ ▒░▓  ░░░ ▒░ ░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
   ░ ░░   ▒ ░░ ░ ▒  ░ ░ ░  ░     ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
     ░░   ▒ ░  ░ ░      ░      ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      
      ░   ░      ░  ░   ░  ░       ░ ░        ░   ░           ░          
     ░                                                                   
                                                                                                        
{NEON_RESET}"""

    print(logo)
    
    # Hacker-style intro text
    hacker_text = [
        f"{NEON_GREEN}INITIALIZING CYBER INTEL PLATFORM{NEON_RESET}",
        f"{NEON_GREEN}LOADING EXPLOIT MODULES{NEON_RESET}",
        f"{NEON_GREEN}CONNECTING TO DARKNET NODES{NEON_RESET}",
        f"{NEON_GREEN}ACCESSING CLEARNET DATABASES{NEON_RESET}",
        f"{NEON_GREEN}LOADING ENTITY RELATIONSHIP ENGINE{NEON_RESET}",
        f"{NEON_GREEN}INITIALIZING SOCIAL MEDIA SCRAPER MODULE{NEON_RESET}",
        f"{NEON_GREEN}MALTEGO COMPETITION MODE: ACTIVATED{NEON_RESET}"
    ]
    
    for text in hacker_text:
        print(text)
        time.sleep(0.3)
    
    print()  # Gap space
    description = f"{NEON_CYAN}[CYBER-INTEL] Advanced OSINT tool with Social Media Username Graphing and Entity Relationship Mapping{NEON_RESET}"
    print(description)
    print()  # Blank line after description before the prompt

# 2. Logging Setup -------------------------------------------------------------

logging.basicConfig(
    filename='cyber_intel.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.INFO
)

# 3. Core Utility Functions ----------------------------------------------------

def validate_email_syntax(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    valid = re.match(pattern, email) is not None
    logging.info(f"Syntax validation for {email}: {valid}")
    return valid

def has_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        has_mx = bool(records)
        logging.info(f"MX record check for {domain}: {has_mx}")
        return has_mx
    except Exception as e:
        logging.error(f"MX record check failed for {domain}: {e}")
        return False

def is_disposable(email):
    disposable_domains = [
        'mailinator.com', '10minutemail.com', 'guerrillamail.com', 'throwawaymail.com',
        'tempmail.com', 'yopmail.com', 'fakeinbox.com', 'temp-mail.org', 'disposable.com',
        'trashmail.com', 'sharklasers.com', 'grr.la', 'guerrillamail.biz'
    ]
    domain = email.split('@')[1].lower()
    disposable = domain in disposable_domains
    logging.info(f"Disposable email check for {email}: {disposable}")
    return disposable

def gravatar_profile(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/{email_hash}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Gravatar profile found for {email}")
            
            # Get the actual profile image
            image_url = f"https://www.gravatar.com/avatar/{email_hash}?s=256&d=404"
            image_response = requests.get(image_url, timeout=10)
            if image_response.status_code == 200:
                # Save the image to a temporary file
                image_path = f"gravatar_{email_hash}.jpg"
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                data['image_path'] = image_path
                
            return data
        logging.info(f"No Gravatar profile for {email}")
    except Exception as e:
        logging.error(f"Gravatar request failed for {email}: {e}")
    return None

def github_search(email):
    url = f"https://api.github.com/search/users?q={email}+in:email"
    headers = {'Accept': 'application/vnd.github.v3+json', 'User-Agent': USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.ok:
            data = response.json()
            users = data.get("items", [])
            
            # Enrich with more details for each user
            enriched_users = []
            for user in users[:3]:  # Limit to top 3 to avoid rate limiting
                user_url = user.get('url')
                if user_url:
                    try:
                        user_response = requests.get(user_url, headers=headers, timeout=10)
                        if user_response.ok:
                            user_details = user_response.json()
                            user.update(user_details)
                            
                            # Try to get avatar image
                            avatar_url = user_details.get('avatar_url')
                            if avatar_url:
                                avatar_response = requests.get(avatar_url, timeout=10)
                                if avatar_response.status_code == 200:
                                    avatar_path = f"github_{user_details.get('login', 'user')}.jpg"
                                    with open(avatar_path, 'wb') as f:
                                        f.write(avatar_response.content)
                                    user['avatar_path'] = avatar_path
                    except Exception as e:
                        logging.error(f"Failed to get GitHub user details: {e}")
                
                enriched_users.append(user)
            
            logging.info(f"GitHub search results for {email}: {len(users)} users found")
            return enriched_users
    except Exception as e:
        logging.error(f"GitHub search failed for {email}: {e}")
    return []

def hibp_breach(email):
    if not HIBP_API_KEY:
        logging.warning("HIBP API key not set, skipping breach check")
        return []
        
    headers = {"User-Agent": "CyberIntelTool", "hibp-api-key": HIBP_API_KEY}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            breaches = response.json()
            logging.info(f"Breach found for {email}: {len(breaches)} breaches")
            return breaches
        if response.status_code == 404:
            logging.info(f"No breach found for {email}")
            return []
        else:
            logging.warning(f"HIBP unexpected status for {email}: {response.status_code}")
    except Exception as e:
        logging.error(f"HIBP check failed for {email}: {e}")
    return []

def google_dorking_email(email):
    dorks = {
        "Exact Email": f'"{email}"',
        "Email User Name": email.split('@')[0],
        "Email Domain": email.split('@')[1],
        "Email in URLs": f'inurl:{email}',
        "Email in Text": f'intext:"{email}"',
        "Email on Social Sites": f'site:linkedin.com OR site:facebook.com OR site:twitter.com "{email}"',
    }
    base_url = "https://www.google.com/search?q="
    results = {name: base_url + requests.utils.quote(query) for name, query in dorks.items()}
    logging.info(f"Google dork URLs generated for {email}")
    return results

def google_dorking_phone(phone_number):
    dorks = {
        "Exact Phone Number": f'"{phone_number}"',
        "Phone without Formatting": f'"{re.sub(r"[^0-9]", "", phone_number)}"',
        "Phone in Text": f'intext:"{phone_number}"',
        "Phone on Social Sites": f'site:facebook.com OR site:twitter.com "{phone_number}"',
    }
    base_url = "https://www.google.com/search?q="
    results = {name: base_url + requests.utils.quote(query) for name, query in dorks.items()}
    logging.info(f"Google dork URLs generated for phone: {phone_number}")
    return results

def social_media_search(email):
    username = email.split('@')[0]
    results = {
        "Twitter Search": f"https://twitter.com/search?q={email}",
        "Instagram Profile": f"https://www.instagram.com/{username}/",
        "LinkedIn Search": f"https://www.linkedin.com/search/results/all/?keywords={email}",
        "Facebook Search": f"https://www.facebook.com/search/top?q={email}",
        "Medium Profile": f"https://medium.com/@{username}",
        "Telegram Profile": f"https://t.me/{username}",
        "Reddit Search": f"https://www.reddit.com/search/?q={email}"
    }
    logging.info(f"Social media search URLs created for {email}")
    return results

def manual_lookup_portals(email):
    results = {
        "ReverseContact": f"https://www.reversecontact.com/",
        "Epieos": f"https://epieos.com/",
        "Email Checker": f"https://email-checker.net/check",
        "IntelX": f"https://intelx.io/",
        "DeHashed": f"https://www.dehashed.com/",
        "Spytox": f"https://www.spytox.com/people-search",
    }
    logging.info(f"Manual lookup portals created for {email}")
    return results

def extract_name_from_email(email):
    """
    Extract potential names from email addresses with various patterns
    """
    # Extract the username part (before the @)
    username = email.split('@')[0].lower()
    
    # First, remove any numbers from the username
    username_no_numbers = re.sub(r'\d+', '', username)
    
    # If removing numbers leaves nothing, use the original username
    if not username_no_numbers:
        username_no_numbers = username
    
    # Common Nigerian names for better pattern recognition
    nigerian_first_names = ['chisom', 'chukwu', 'nnamdi', 'obinna', 'chika', 'uche', 'nneka', 
                           'chinwe', 'ifeoma', 'adanna', 'amarachi', 'chinelo', 'ekene', 'emeka',
                           'obinna', 'onyeka', 'tochukwu', 'uzoma', 'nkechi', 'ngozi', 'chiamaka',
                           'ada', 'amara', 'chioma', 'ebuka', 'ifeanyi', 'kene', 'nkiru', 'obinna',
                           'onyinye', 'uchechi', 'zainab', 'ahmed', 'musa', 'fatima', 'aminu']
    
    nigerian_last_names = ['ofonagoro', 'okoro', 'nwosu', 'okeke', 'onyema', 'nwachukwu', 'nwafor',
                          'okonkwo', 'nwankwo', 'nwabueze', 'nwadike', 'nwosu', 'okoli', 'okoro',
                          'nwakuche', 'nwabudike', 'nwabueze', 'nwadike', 'nwakanma', 'nwankwo',
                          'adebayo', 'suleiman', 'abdullahi', 'ogunleye', 'balogun', 'salami', 'mustapha']
    
    # Try to detect name patterns by checking for common Nigerian names
    for first_name in nigerian_first_names:
        if first_name in username_no_numbers:
            # Look for a potential last name
            remaining = username_no_numbers.replace(first_name, '')
            for last_name in nigerian_last_names:
                if last_name in remaining:
                    return f"{last_name.title()} {first_name.title()}"
    
    # Try the reverse (last name first)
    for last_name in nigerian_last_names:
        if last_name in username_no_numbers:
            # Look for a potential first name
            remaining = username_no_numbers.replace(last_name, '')
            for first_name in nigerian_first_names:
                if first_name in remaining:
                    return f"{last_name.title()} {first_name.title()}"
    
    # Common patterns for email usernames
    patterns = [
        # First.Last pattern (john.doe)
        (r'^([a-z]+)\.([a-z]+)$', lambda m: f"{m.group(1).title()} {m.group(2).title()}"),
        # FirstLast pattern (johndoe)
        (r'^([a-z]{3,})([a-z]{3,})$', lambda m: f"{m.group(1).title()} {m.group(2).title()}"),
        # FLast pattern (jdoe)
        (r'^([a-z])([a-z]+)$', lambda m: f"{m.group(1).upper()}. {m.group(2).title()}"),
        # FirstL pattern (johnd)
        (r'^([a-z]+)([a-z])$', lambda m: f"{m.group(1).title()} {m.group(2).upper()}."),
        # First_Middle_Last pattern (john.a.doe)
        (r'^([a-z]+)\.([a-z])\.([a-z]+)$', lambda m: f"{m.group(1).title()} {m.group(2).upper()}. {m.group(3).title()}"),
    ]
    
    # Try each pattern to extract a name from the username without numbers
    for pattern, formatter in patterns:
        match = re.match(pattern, username_no_numbers)
        if match:
            return formatter(match)
    
    # If no pattern matches, try to split by common separators
    separators = ['.', '_', '-']
    for sep in separators:
        if sep in username_no_numbers:
            parts = username_no_numbers.split(sep)
            if len(parts) >= 2:
                # Filter out numeric parts and very short parts
                name_parts = [p.title() for p in parts if p.isalpha() and len(p) > 2]
                if len(name_parts) >= 2:
                    return " ".join(name_parts)
    
    # Special handling for Nigerian names like "ofonagorochisom"
    # Look for common Nigerian name patterns
    nigerian_patterns = [
        (r'^(ofonagoro)(chisom)$', lambda m: f"{m.group(1).title()} {m.group(2).title()}"),
        (r'^(chukwu)(emeka)$', lambda m: f"{m.group(1).title()} {m.group(2).title()}"),
        (r'^(nnamdi)(chukwu)$', lambda m: f"{m.group(1).title()} {m.group(2).title()}"),
        (r'^(obinna)(chika)$', lambda m: f"{m.group(1).title()} {m.group(2).title()}"),
    ]
    
    for pattern, formatter in nigerian_patterns:
        match = re.match(pattern, username_no_numbers)
        if match:
            return formatter(match)
    
    # If all else fails, try to split at natural language boundaries
    # Look for places where a lowercase letter is followed by an uppercase letter
    split_pattern = r'([a-z])([A-Z])'
    split_name = re.sub(split_pattern, r'\1 \2', username_no_numbers.title())
    
    # If splitting produced multiple words, use that
    if ' ' in split_name:
        return split_name
    
    # If we still have nothing, return the username without numbers as is (capitalized)
    if username_no_numbers and username_no_numbers != username:
        return username_no_numbers.title()
    
    # If we still have nothing, return the original username (capitalized)
    return username.title()

def social_deep_dive(email):
    """
    Perform a deep dive social media search by extracting names from email
    and searching across multiple platforms
    """
    print(f"\n{NEON_BOLD_CYAN}---[ SOCIAL DEEP DIVE ]---{NEON_RESET}")
    
    # Extract potential name from email
    extracted_name = extract_name_from_email(email)
    print(f"{NEON_GREEN}Extracted Name: {NEON_YELLOW}{extracted_name}{NEON_RESET}")
    
    # Social media platforms to search (Sherlock-style)
    social_platforms = {
        "Twitter": f"https://twitter.com/search?q={extracted_name.replace(' ', '+')}+OR+{email}",
        "Instagram": f"https://www.instagram.com/web/search/topsearch/?query={extracted_name.replace(' ', '+')}",
        "Facebook": f"https://www.facebook.com/search/top/?q={extracted_name.replace(' ', '+')}+OR+{email}",
        "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={extracted_name.replace(' ', '+')}+OR+{email}",
        "YouTube": f"https://www.youtube.com/results?search_query={extracted_name.replace(' ', '+')}",
        "Reddit": f"https://www.reddit.com/search/?q={extracted_name.replace(' ', '+')}+OR+{email}",
        "Pinterest": f"https://www.pinterest.com/search/pins/?q={extracted_name.replace(' ', '+')}",
        "TikTok": f"https://www.tiktok.com/search?q={extracted_name.replace(' ', '+')}",
        "GitHub": f"https://github.com/search?q={extracted_name.replace(' ', '+')}+OR+{email}&type=users",
        "GitLab": f"https://gitlab.com/search?search={extracted_name.replace(' ', '+')}+OR+{email}",
        "Medium": f"https://medium.com/search?q={extracted_name.replace(' ', '+')}+OR+{email}",
        "Quora": f"https://www.quora.com/search?q={extracted_name.replace(' ', '+')}+OR+{email}",
        "Vimeo": f"https://vimeo.com/search?q={extracted_name.replace(' ', '+')}",
        "Flickr": f"https://www.flickr.com/search/?text={extracted_name.replace(' ', '+')}",
        "Dribbble": f"https://dribbble.com/search/{extracted_name.replace(' ', '+')}",
        "Behance": f"https://www.behance.net/search/users?search={extracted_name.replace(' ', '+')}",
        "Goodreads": f"https://www.goodreads.com/search?q={extracted_name.replace(' ', '+')}",
        "ResearchGate": f"https://www.researchgate.net/search/search.html?query={extracted_name.replace(' ', '+')}",
        "Keybase": f"https://keybase.io/search?q={extracted_name.replace(' ', '+')}+OR+{email}",
        "About.me": f"https://about.me/search?q={extracted_name.replace(' ', '+')}",
        "AngelList": f"https://angel.co/search?q={extracted_name.replace(' ', '+')}",
    }
    
    # Also search with the email itself
    email_search = {
        "Email on Twitter": f"https://twitter.com/search?q={email}",
        "Email on Facebook": f"https://www.facebook.com/search/top/?q={email}",
        "Email on LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={email}",
        "Email on Instagram": f"https://www.instagram.com/web/search/topsearch/?query={email}",
    }
    
    # Combine both searches
    all_searches = {**social_platforms, **email_search}
    
    logging.info(f"Social deep dive for {email}: Extracted name '{extracted_name}'")
    return {
        "extracted_name": extracted_name,
        "social_searches": all_searches
    }

def email_reputation(email):
    # Expanded blacklist for more comprehensive checking
    blacklist = [
        'spamdomain.com', 'blacklisted.com', 'fakeinbox.com', 'tempmail.com',
        'throwawaymail.com', 'guerrillamail.com', 'mailinator.com', 'yopmail.com',
        '10minutemail.com', 'trashmail.com', 'disposable.com', 'sharklasers.com',
        'grr.la', 'guerrillamail.biz', 'temp-mail.org', 'fakeinbox.com'
    ]
    domain = email.split('@')[1].lower()
    reputation = "Blacklisted" if domain in blacklist else "Clean"
    logging.info(f"Email reputation check for {email}: {reputation}")
    return reputation

def hunter_io_verification(email):
    if not HUNTER_IO_API_KEY or HUNTER_IO_API_KEY == "YOUR_HUNTER_IO_API_KEY":
        return {"error": "Hunter.io API key not configured"}
    
    try:
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_IO_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            logging.info(f"Hunter.io verification for {email}: {data.get('result', 'Unknown')}")
            return data
        else:
            logging.error(f"Hunter.io API error: {response.status_code}")
            return {"error": f"API returned status {response.status_code}"}
    except Exception as e:
        logging.error(f"Hunter.io request failed: {e}")
        return {"error": str(e)}

def check_pastebin(email):
    try:
        # Using alternative approach since the scrape.pastebin.com API is often blocked
        # We'll use a Google search approach instead
        google_url = f"https://www.google.com/search?q=site:pastebin.com+{email}"
        response = requests.get(google_url, timeout=10, headers={'User-Agent': USER_AGENT})
        hits = []
        
        if response.status_code == 200:
            # Simple check for pastebin links in the Google results
            pastebin_links = re.findall(r'https?://pastebin\.com/[a-zA-Z0-9]+', response.text)
            for link in set(pastebin_links):  # Remove duplicates
                hits.append(link)
                
        return hits
    except Exception as e:
        logging.error(f"Pastebin check failed: {e}")
    return []

def validate_phone_number(phone_number):
    try:
        parsed = phonenumbers.parse(phone_number, None)
        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)
        
        if not possible:
            return {"error": "Number is not possible"}
        
        # Get location with better error handling
        try:
            location = geocoder.description_for_number(parsed, "en")
            if not location:
                location = "Unknown"
        except:
            location = "Unknown"
            
        # Get carrier with better error handling
        try:
            carrier_name = carrier.name_for_number(parsed, 'en')
            if not carrier_name:
                carrier_name = "Unknown"
        except:
            carrier_name = "Unknown"
            
        result = {
            "valid": valid,
            "international_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "national_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            "location": location,
            "carrier": carrier_name,
            "timezone": timezone.time_zones_for_number(parsed)
        }
        
        return result
    except Exception as e:
        return {"error": str(e)}

def generate_pdf_report(target, data_summary, filename="report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, f"CYBER INTEL REPORT for {target}")
    y -= 30

    c.setFont("Helvetica", 12)
    for section, content in data_summary.items():
        if isinstance(content, list):
            c.drawString(margin, y, f"{section}:")
            y -= 18
            for item in content:
                line = str(item)
                c.drawString(margin+20, y, line[:90])
                y -= 14
                if y < margin:
                    c.showPage()
                    y = height - margin
        elif isinstance(content, dict):
            c.drawString(margin, y, f"{section}:")
            y -= 18
            for k, v in content.items():
                line = f"{k}: {v}"
                c.drawString(margin+20, y, line[:90])
                y -= 14
                if y < margin:
                    c.showPage()
                    y = height - margin
        else:
            c.drawString(margin, y, f"{section}: {content}")
            y -= 20
            if y < margin:
                c.showPage()
                y = height - margin

    c.save()
    logging.info(f"PDF report generated: {filename}")

def print_hacker_style(text):
    """Print text with hacker-style typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

def generate_profile_image(name, image_path):
    """Generate a profile image with initials for entities without images"""
    # Create a blank image with a background color
    img_size = (200, 200)
    background_color = (random.randint(0, 100), random.randint(0, 100), random.randint(100, 255))
    image = Image.new('RGB', img_size, background_color)
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use a nice font
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Get initials from name
    initials = ''.join([word[0].upper() for word in name.split()[:2]])
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((img_size[0] - text_width) // 2, (img_size[1] - text_height) // 2)
    
    # Draw the text
    draw.text(position, initials, fill=(255, 255, 255), font=font)
    
    # Save the image
    image.save(image_path)
    return image_path

def generate_entity_graph(email, results):
    """
    Generate a SpiderFoot-like graph showing different entities associated with an email address
    with profile images for each entity
    """
    print(f"\n{NEON_BOLD_CYAN}---[ ENTITY RELATIONSHIP GRAPH ]---{NEON_RESET}")
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add the main email node
    G.add_node(email, type='email', color='red', size=3000, image=None)
    
    # Extract entities from different sources
    entities = []
    image_files = []
    
    # Extract from breaches
    if results.get('breaches'):
        for breach in results['breaches']:
            breach_name = breach['Name']
            # Generate a profile image for the breach
            breach_image_path = f"breach_{breach_name}.jpg"
            generate_profile_image(breach_name, breach_image_path)
            
            G.add_node(breach_name, type='breach', color='orange', size=1500, image=breach_image_path)
            G.add_edge(email, breach_name, relationship='breached_in', weight=2)
            entities.append({
                'name': breach_name,
                'type': 'Data Breach',
                'description': f"Email found in {breach_name} breach ({breach.get('BreachDate', 'Unknown date')})",
                'relationship': 'Breached In',
                'image_path': breach_image_path
            })
            image_files.append(breach_image_path)
    
    # Extract from GitHub
    if results.get('github'):
        for user in results['github']:
            username = user.get('login', 'Unknown')
            user_image_path = user.get('avatar_path')
            
            # If no avatar, generate one with initials
            if not user_image_path:
                user_real_name = user.get('name', username)
                user_image_path = f"github_{username}.jpg"
                generate_profile_image(user_real_name, user_image_path)
            
            G.add_node(username, type='github', color='purple', size=1200, image=user_image_path)
            G.add_edge(email, username, relationship='github_account', weight=3)
            entities.append({
                'name': username,
                'type': 'GitHub Account',
                'description': f"GitHub user associated with this email. Name: {user.get('name', 'N/A')}, Followers: {user.get('followers', 0)}",
                'relationship': 'GitHub Account',
                'image_path': user_image_path
            })
            image_files.append(user_image_path)
    
    # Extract from social deep dive
    if results.get('social_deep_dive'):
        extracted_name = results['social_deep_dive'].get('extracted_name')
        if extracted_name and extracted_name != email.split('@')[0].title():
            # Generate profile image for the extracted name
            name_image_path = f"person_{extracted_name.replace(' ', '_')}.jpg"
            generate_profile_image(extracted_name, name_image_path)
            
            G.add_node(extracted_name, type='person', color='blue', size=2000, image=name_image_path)
            G.add_edge(email, extracted_name, relationship='potential_owner', weight=5)
            entities.append({
                'name': extracted_name,
                'type': 'Potential Person',
                'description': f"Name extracted from email pattern analysis. This is likely the person associated with this email.",
                'relationship': 'Potential Owner',
                'image_path': name_image_path
            })
            image_files.append(name_image_path)
    
    # Extract from pastebin
    if results.get('pastebin'):
        for i, paste in enumerate(results['pastebin']):
            paste_id = f"Pastebin_{i+1}"
            # Generate profile image for pastebin
            paste_image_path = f"pastebin_{i+1}.jpg"
            generate_profile_image(f"Paste {i+1}", paste_image_path)
            
            G.add_node(paste_id, type='pastebin', color='yellow', size=1000, image=paste_image_path)
            G.add_edge(email, paste_id, relationship='found_in_paste', weight=1)
            entities.append({
                'name': paste_id,
                'type': 'Pastebin Content',
                'description': f"Email found in pastebin content: {paste}",
                'relationship': 'Found In Paste',
                'image_path': paste_image_path
            })
            image_files.append(paste_image_path)
    
    # Extract from Gravatar
    if results.get('gravatar'):
        gravatar_data = results.get('gravatar', {})
        gravatar_image_path = gravatar_data.get('image_path')
        
        if gravatar_image_path:
            G.add_node("Gravatar", type='gravatar', color='green', size=1200, image=gravatar_image_path)
            G.add_edge(email, "Gravatar", relationship='has_gravatar', weight=4)
            entities.append({
                'name': "Gravatar",
                'type': 'Gravatar Profile',
                'description': f"Email has a Gravatar profile associated with it.",
                'relationship': 'Has Gravatar',
                'image_path': gravatar_image_path
            })
            image_files.append(gravatar_image_path)
    
    # Create the graph visualization with images
    plt.figure(figsize=(16, 12))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=3, iterations=100, scale=2)
    
    # Draw edges first
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, alpha=0.6, width=1.5)
    
    # Draw nodes with images
    ax = plt.gca()
    for node in G.nodes():
        image_path = G.nodes[node].get('image')
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                
                # Create circular mask for the image
                mask = Image.new('L', (80, 80), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 80, 80), fill=255)
                
                # Apply mask
                img.putalpha(mask)
                
                imagebox = OffsetImage(img, zoom=0.4)
                ab = AnnotationBbox(imagebox, pos[node], frameon=False, pad=0)
                ax.add_artist(ab)
            except Exception as e:
                logging.error(f"Failed to process image {image_path}: {e}")
                # Draw a circle as fallback
                color = G.nodes[node].get('color', 'gray')
                nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=color, 
                                      node_size=2000, alpha=0.8)
        else:
            # Draw a circle for nodes without images
            color = G.nodes[node].get('color', 'gray')
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=color, 
                                  node_size=2000, alpha=0.8)
    
    # Draw labels
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7, font_weight='bold')
    
    plt.title(f"Entity Relationship Graph for {email}", fontsize=16, fontweight='bold')
    plt.axis('off')
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Email'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Person'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Data Breach'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10, label='GitHub'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Gravatar'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='Pastebin'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
    
    # Save the graph
    graph_filename = f"entity_graph_{email.replace('@', '_at_')}.png"
    plt.tight_layout()
    plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"{NEON_GREEN}Entity relationship graph saved as: {NEON_YELLOW}{graph_filename}{NEON_RESET}")
    
    # Display entity intelligence
    print(f"\n{NEON_BOLD_CYAN}ENTITY INTELLIGENCE SUMMARY:{NEON_RESET}")
    for i, entity in enumerate(entities, 1):
        print(f"{NEON_GREEN}{i}. {NEON_YELLOW}{entity['name']} ({entity['type']}){NEON_RESET}")
        print(f"   {NEON_WHITE}Relationship: {entity['relationship']}{NEON_RESET}")
        print(f"   {NEON_WHITE}Description: {entity['description']}{NEON_RESET}")
        print()
    
    return graph_filename, entities, image_files

def social_media_scraper(username):
    """
    Scrape social media platforms for a given username and generate a relationship graph
    """
    print(f"\n{NEON_BOLD_CYAN}---[ SOCIAL MEDIA USERNAME SCRAPER ]---{NEON_RESET}")
    print(f"{NEON_GREEN}Searching for username: {NEON_YELLOW}{username}{NEON_RESET}")
    
    # Social media platforms to check
    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "GitHub": f"https://github.com/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Telegram": f"https://t.me/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "Dribbble": f"https://dribbble.com/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Keybase": f"https://keybase.io/{username}",
        "About.me": f"https://about.me/{username}",
    }
    
    results = {
        "username": username,
        "platforms": {},
        "profile_images": {}
    }
    
    # Check each platform
    found_count = 0
    for platform, url in platforms.items():
        try:
            response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                # Check if page contains username or similar indicators
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Simple check for presence of username in page
                if username.lower() in response.text.lower() or \
                   (soup.title and username.lower() in soup.title.text.lower()):
                    
                    results["platforms"][platform] = {
                        "url": url,
                        "status": "Found",
                        "title": soup.title.text if soup.title else "No title"
                    }
                    found_count += 1
                    
                    print(f"{NEON_GREEN}[FOUND] {NEON_YELLOW}{platform}: {NEON_WHITE}{url}{NEON_RESET}")
                    
                    # Try to find profile image
                    try:
                        # Common meta tags for profile images
                        meta_image = soup.find("meta", property="og:image")
                        if meta_image and meta_image.get("content"):
                            img_url = meta_image.get("content")
                            img_response = requests.get(img_url, timeout=10)
                            if img_response.status_code == 200:
                                img_path = f"{platform}_{username}.jpg"
                                with open(img_path, 'wb') as f:
                                    f.write(img_response.content)
                                results["profile_images"][platform] = img_path
                                print(f"{NEON_GREEN}  Profile image saved: {NEON_WHITE}{img_path}{NEON_RESET}")
                    except Exception as e:
                        logging.error(f"Failed to get profile image from {platform}: {e}")
                
                else:
                    results["platforms"][platform] = {
                        "url": url,
                        "status": "Not found",
                        "title": soup.title.text if soup.title else "No title"
                    }
            else:
                results["platforms"][platform] = {
                    "url": url,
                    "status": "Not found",
                    "title": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            logging.error(f"Error checking {platform}: {e}")
            results["platforms"][platform] = {
                "url": url,
                "status": "Error",
                "title": str(e)
            }
    
    print(f"{NEON_GREEN}Found {NEON_YELLOW}{found_count}{NEON_GREEN} platforms with username {NEON_YELLOW}{username}{NEON_RESET}")
    
    # Generate social media graph
    if found_count > 0:
        graph_filename = generate_social_media_graph(username, results)
        results["graph_filename"] = graph_filename
    
    return results

def generate_social_media_graph(username, results):
    """
    Generate a graph showing social media connections for a username
    """
    print(f"{NEON_GREEN}Generating social media relationship graph...{NEON_RESET}")
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add the main username node
    G.add_node(username, type='username', color='red', size=3000)
    
    # Add platform nodes
    entities = []
    image_files = []
    
    for platform, data in results["platforms"].items():
        if data["status"] == "Found":
            # Check if we have a profile image for this platform
            image_path = results["profile_images"].get(platform)
            
            # If no image, generate one with platform initials
            if not image_path:
                image_path = f"{platform}_{username}.jpg"
                generate_profile_image(platform, image_path)
            
            # Add platform node
            G.add_node(platform, type='platform', color='blue', size=1500, image=image_path)
            G.add_edge(username, platform, relationship='has_account', weight=3)
            
            entities.append({
                'name': platform,
                'type': 'Social Platform',
                'description': f"Username found on {platform}",
                'relationship': 'Has Account',
                'image_path': image_path,
                'url': data["url"]
            })
            image_files.append(image_path)
    
    # Create the graph visualization with images
    plt.figure(figsize=(14, 10))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=2, iterations=50, scale=2)
    
    # Draw edges first
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, alpha=0.6, width=1.5)
    
    # Draw nodes with images
    ax = plt.gca()
    for node in G.nodes():
        if node == username:
            # Draw main username node as a circle
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='red', 
                                  node_size=3000, alpha=0.8)
        else:
            # Draw platform nodes with images
            image_path = G.nodes[node].get('image')
            if image_path and os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.resize((70, 70), Image.Resampling.LANCZOS)
                    
                    # Create circular mask for the image
                    mask = Image.new('L', (70, 70), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, 70, 70), fill=255)
                    
                    # Apply mask
                    img.putalpha(mask)
                    
                    imagebox = OffsetImage(img, zoom=0.35)
                    ab = AnnotationBbox(imagebox, pos[node], frameon=False, pad=0)
                    ax.add_artist(ab)
                except Exception as e:
                    logging.error(f"Failed to process image {image_path}: {e}")
                    # Draw a circle as fallback
                    color = G.nodes[node].get('color', 'gray')
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=color, 
                                          node_size=1500, alpha=0.8)
    
    # Draw labels
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7, font_weight='bold')
    
    plt.title(f"Social Media Graph for username: {username}", fontsize=16, fontweight='bold')
    plt.axis('off')
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Username'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Social Platform'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
    
    # Save the graph
    graph_filename = f"social_media_graph_{username}.png"
    plt.tight_layout()
    plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"{NEON_GREEN}Social media graph saved as: {NEON_YELLOW}{graph_filename}{NEON_RESET}")
    
    # Display platform intelligence
    print(f"\n{NEON_BOLD_CYAN}SOCIAL MEDIA INTELLIGENCE SUMMARY:{NEON_RESET}")
    for i, entity in enumerate(entities, 1):
        print(f"{NEON_GREEN}{i}. {NEON_YELLOW}{entity['name']}{NEON_RESET}")
        print(f"   {NEON_WHITE}URL: {NEON_CYAN}{entity['url']}{NEON_RESET}")
        print(f"   {NEON_WHITE}Relationship: {entity['relationship']}{NEON_RESET}")
        print()
    
    return graph_filename

def email_analysis(email):
    print(f"\n{NEON_BOLD_CYAN}---[ EMAIL BREACH & SOURCE ANALYSIS ]---{NEON_RESET}")
    
    # Basic validation
    if not validate_email_syntax(email):
        print(f"{NEON_BOLD_RED}[ERROR] Invalid email format.{NEON_RESET}")
        return None
    
    domain = email.split("@")[1]
    if not has_mx_record(domain):
        print(f"{NEON_YELLOW}[WARNING] Domain has no valid MX records.{NEON_RESET}")
    
    # Disposable check
    if is_disposable(email):
        print(f"{NEON_YELLOW}[WARNING] Disposable email detected.{NEON_RESET}")
    else:
        print(f"{NEON_GREEN}[OK] Email appears non-disposable.{NEON_RESET}")
    
    results = {}
    
    # HIBP breach check
    print(f"{NEON_CYAN}Checking breach databases...{NEON_RESET}")
    breaches = hibp_breach(email)
    results['breaches'] = breaches
    if breaches:
        print(f"{NEON_GREEN}[FOUND] {NEON_YELLOW}{len(breaches)} breaches detected:{NEON_RESET}")
        for breach in breaches[:3]:  # Show top 3
            print(f"{NEON_GREEN}  - {NEON_YELLOW}{breach['Name']} ({breach['BreachDate']}){NEON_RESET}")
        if len(breaches) > 3:
            print(f"{NEON_GREEN}  - ... and {NEON_YELLOW}{len(breaches)-3} more{NEON_RESET}")
    else:
        print(f"{NEON_GREEN}[CLEAN] {NEON_YELLOW}No breaches found.{NEON_RESET}")
    
    # Pastebin check
    print(f"{NEON_CYAN}Scanning paste sites...{NEON_RESET}")
    pastebin_hits = check_pastebin(email)
    results['pastebin'] = pastebin_hits
    if pastebin_hits:
        print(f"{NEON_GREEN}[FOUND] {NEON_YELLOW}{len(pastebin_hits)} paste(s) containing email:{NEON_RESET}")
        for hit in pastebin_hits[:3]:  # Show top 3
            print(f"{NEON_GREEN}  - {NEON_WHITE}{hit}{NEON_RESET}")
    else:
        print(f"{NEON_GREEN}[CLEAN] {NEON_YELLOW}Not found in recent pastes.{NEON_RESET}")
    
    # Hunter.io verification
    print(f"{NEON_CYAN}Running email verification...{NEON_RESET}")
    hunter_data = hunter_io_verification(email)
    results['hunter'] = hunter_data
    if 'error' not in hunter_data:
        print(f"{NEON_GREEN}Status: {NEON_Yellow}{hunter_data.get('status', 'Unknown')}{NEON_RESET}")
        print(f"{NEON_GREEN}Result: {NEON_YELLOW}{hunter_data.get('result', 'Unknown')}{NEON_RESET}")
        print(f"{NEON_GREEN}Disposable: {NEON_YELLOW}{hunter_data.get('disposable', 'Unknown')}{NEON_RESET}")
    else:
        print(f"{NEON_YELLOW}[INFO] Hunter.io: {hunter_data['error']}{NEON_RESET}")
    
    # Gravatar check
    print(f"{NEON_CYAN}Checking Gravatar...{NEON_RESET}")
    gravatar = gravatar_profile(email)
    results['gravatar'] = gravatar
    if gravatar:
        print(f"{NEON_GREEN}[FOUND] {NEON_YELLOW}Gravatar profile exists.{NEON_RESET}")
        if gravatar.get('image_path'):
            print(f"{NEON_GREEN}  Profile image saved.{NEON_RESET}")
    else:
        print(f"{NEON_GREEN}[CLEAN] {NEON_YELLOW}No Gravatar profile.{NEON_RESET}")
    
    # GitHub search
    print(f"{NEON_CYAN}Searching GitHub...{NEON_RESET}")
    github_users = github_search(email)
    results['github'] = github_users
    if github_users:
        print(f"{NEON_GREEN}[FOUND] {NEON_YELLOW}{len(github_users)} GitHub user(s):{NEON_RESET}")
        for user in github_users[:3]:  # Show top 3
            print(f"{NEON_GREEN}  - {NEON_WHITE}{user.get('login')} ({user.get('html_url')}){NEON_RESET}")
            if user.get('avatar_path'):
                print(f"{NEON_GREEN}  Avatar image saved.{NEON_RESET}")
    else:
        print(f"{NEON_GREEN}[CLEAN] {NEON_YELLOW}No GitHub users with this email.{NEON_RESET}")
    
    # Social media
    social_urls = social_media_search(email)
    results['social_media'] = social_urls
    
    # Manual lookup portals
    manual_portals = manual_lookup_portals(email)
    results['manual_portals'] = manual_portals
    
    # Social deep dive
    social_dive = social_deep_dive(email)
    results['social_deep_dive'] = social_dive
    
    # Email reputation
    reputation = email_reputation(email)
    results['reputation'] = reputation
    
    # Google dorking
    google_links = google_dorking_email(email)
    results['google_dorks'] = google_links
    
    # Generate entity relationship graph
    graph_filename, entities, image_files = generate_entity_graph(email, results)
    results['entity_graph'] = graph_filename
    results['entities'] = entities
    results['image_files'] = image_files
    
    return results

def phone_analysis(phone_number):
    print(f"\n{NEON_BOLD_CYAN}---[ PHONE NUMBER ANALYSIS ]---{NEON_RESET}")
    
    # Basic validation
    phone_data = validate_phone_number(phone_number)
    if 'error' in phone_data:
        print(f"{NEON_BOLD_RED}[ERROR] {phone_data['error']}{NEON_RESET}")
        return None
    
    results = {'validation': phone_data}
    
    print(f"{NEON_GREEN}Valid Number: {NEON_YELLOW}{phone_data['valid']}{NEON_RESET}")
    print(f"{NEON_GREEN}International Format: {NEON_YELLOW}{phone_data['international_format']}{NEON_RESET}")
    print(f"{NEON_GREEN}National Format: {NEON_YELLOW}{phone_data['national_format']}{NEON_RESET}")
    print(f"{NEON_GREEN}Location: {NEON_YELLOW}{phone_data['location']}{NEON_RESET}")
    print(f"{NEON_GREEN}Carrier: {NEON_YELLOW}{phone_data['carrier']}{NEON_RESET}")
    print(f"{NEON_GREEN}Timezone: {NEON_YELLOW}{', '.join(phone_data['timezone'])}{NEON_RESET}")
    
    # Google dorking
    google_links = google_dorking_phone(phone_number)
    results['google_dorks'] = google_links
    
    return results

def print_results(target, results, target_type="email"):
    print(f"\n{NEON_BOLD_CYAN}---[ OSINT RESULTS FOR {target.upper()} ]---{NEON_RESET}")
    
    if target_type == "email":
        # Breaches
        if results.get('breaches'):
            print(f"\n{NEON_BOLD_CYAN}BREACHES FOUND:{NEON_RESET}")
            for breach in results['breaches']:
                print(f"{NEON_GREEN}  - {NEON_YELLOW}{breach['Name']} ({breach['BreachDate']}) - {breach['Description']}{NEON_RESET}")
        
        # Pastebin
        if results.get('pastebin'):
            print(f"\n{NEON_BOLD_CYAN}PASTE SITE MATCHES:{NEON_RESET}")
            for paste in results['pastebin']:
                print(f"{NEON_GREEN}  - {NEON_WHITE}{paste}{NEON_RESET}")
        
        # Hunter.io data
        if results.get('hunter') and 'error' not in results['hunter']:
            hunter = results['hunter']
            print(f"\n{NEON_BOLD_CYAN}EMAIL VERIFICATION:{NEON_RESET}")
            print(f"{NEON_GREEN}  Status: {NEON_YELLOW}{hunter.get('status')}{NEON_RESET}")
            print(f"{NEON_GREEN}  Result: {NEON_YELLOW}{hunter.get('result')}{NEON_RESET}")
            print(f"{NEON_GREEN}  Score: {NEON_YELLOW}{hunter.get('score')}{NEON_RESET}")
            print(f"{NEON_GREEN}  Disposable: {NEON_YELLOW}{hunter.get('disposable')}{NEON_RESET}")
            print(f"{NEON_GREEN}  MX Records: {NEON_YELLOW}{'Present' if hunter.get('mx_records') else 'Missing'}{NEON_RESET}")
            print(f"{NEON_GREEN}  SMTP Check: {NEON_YELLOW}{hunter.get('smtp_server')}{NEON_RESET}")
        
        # Gravatar
        print(f"\n{NEON_BOLD_CYAN}GRAVATAR:{NEON_RESET}")
        print(f"{NEON_GREEN}  Found: {NEON_YELLOW}{results.get('gravatar') is not None}{NEON_RESET}")
        if results.get('gravatar') and results['gravatar'].get('image_path'):
            print(f"{NEON_GREEN}  Image: {NEON_YELLOW}{results['gravatar']['image_path']}{NEON_RESET}")
        
        # GitHub
        if results.get('github'):
            print(f"\n{NEON_BOLD_CYAN}GITHUB USERS:{NEON_RESET}")
            for user in results['github']:
                print(f"{NEON_GREEN}  - {NEON_WHITE}{user.get('login')} ({user.get('html_url')}){NEON_RESET}")
                if user.get('avatar_path'):
                    print(f"{NEON_GREEN}    Avatar: {NEON_YELLOW}{user['avatar_path']}{NEON_RESET}")
        
        # Reputation
        print(f"\n{NEON_BOLD_CYAN}REPUTATION:{NEON_RESET}")
        print(f"{NEON_GREEN}  Status: {NEON_YELLOW}{results.get('reputation')}{NEON_RESET}")
    
    elif target_type == "phone":
        # Phone validation data
        if results.get('validation'):
            validation = results['validation']
            print(f"\n{NEON_BOLD_CYAN}PHONE VALIDATION:{NEON_RESET}")
            print(f"{NEON_GREEN}  Valid: {NEON_YELLOW}{validation.get('valid')}{NEON_RESET}")
            print(f"{NEON_GREEN}  International Format: {NEON_YELLOW}{validation.get('international_format')}{NEON_RESET}")
            print(f"{NEON_GREEN}  National Format: {NEON_YELLOW}{validation.get('national_format')}{NEON_RESET}")
            print(f"{NEON_GREEN}  Location: {NEON_YELLOW}{validation.get('location')}{NEON_RESET}")
            print(f"{NEON_GREEN}  Carrier: {NEON_YELLOW}{validation.get('carrier')}{NEON_RESET}")
            print(f"{NEON_GREEN}  Timezone: {NEON_YELLOW}{', '.join(validation.get('timezone', []))}{NEON_RESET}")
    
    elif target_type == "username":
        # Social media results
        if results.get('platforms'):
            print(f"\n{NEON_BOLD_CYAN}SOCIAL MEDIA PLATFORMS FOUND:{NEON_RESET}")
            for platform, data in results['platforms'].items():
                if data['status'] == 'Found':
                    print(f"{NEON_GREEN}  - {NEON_YELLOW}{platform}: {NEON_WHITE}{data['url']}{NEON_RESET}")
                    if data.get('title'):
                        print(f"     Title: {NEON_CYAN}{data['title']}{NEON_RESET}")
    
    # Google dorking suggestions for both email and phone
    if results.get('google_dorks'):
        print(f"\n{NEON_BOLD_YELLOW}GOOGLE DORKING SUGGESTIONS:{NEON_RESET}")
        for name, url in results['google_dorks'].items():
            print(f"{NEON_GREEN}  {name}: {NEON_WHITE}{url}{NEON_RESET}")
    
    # Social media URLs for email
    if target_type == "email" and results.get('social_media'):
        print(f"\n{NEON_BOLD_YELLOW}SOCIAL MEDIA SEARCH URLs:{NEON_RESET}")
        for platform, url in results['social_media'].items():
            print(f"{NEON_GREEN}  {platform}: {NEON_WHITE}{url}{NEON_RESET}")
    
    # Manual lookup portals for email
    if target_type == "email" and results.get('manual_portals'):
        print(f"\n{NEON_BOLD_YELLOW}MANUAL LOOKUP PORTALS:{NEON_RESET}")
        for platform, url in results['manual_portals'].items():
            print(f"{NEON_GREEN}  {platform}: {NEON_WHITE}{url}{NEON_RESET}")
    
    # Social deep dive for email
    if target_type == "email" and results.get('social_deep_dive'):
        social_dive = results['social_deep_dive']
        print(f"\n{NEON_BOLD_YELLOW}SOCIAL DEEP DIVE:{NEON_RESET}")
        print(f"{NEON_GREEN}  Extracted Name: {NEON_YELLOW}{social_dive['extracted_name']}{NEON_RESET}")
        
        # Show top 10 social media searches
        print(f"{NEON_GREEN}  Social Media Searches:{NEON_RESET}")
        count = 0
        for platform, url in social_dive['social_searches'].items():
            if count < 10:  # Show only top 10 to avoid overwhelming output
                print(f"{NEON_GREEN}    {platform}: {NEON_WHITE}{url}{NEON_RESET}")
                count += 1
        if len(social_dive['social_searches']) > 10:
            print(f"{NEON_GREEN}    ... and {NEON_YELLOW}{len(social_dive['social_searches']) - 10}{NEON_GREEN} more platforms{NEON_RESET}")
    
    # Entity relationship graph for email
    if target_type == "email" and results.get('entity_graph'):
        print(f"\n{NEON_BOLD_YELLOW}ENTITY RELATIONSHIP GRAPH:{NEON_RESET}")
        print(f"{NEON_GREEN}  Graph saved as: {NEON_WHITE}{results['entity_graph']}{NEON_RESET}")
        
        # Show entity intelligence
        if results.get('entities'):
            print(f"\n{NEON_BOLD_YELLOW}ENTITY INTELLIGENCE:{NEON_RESET}")
            for entity in results['entities']:
                print(f"{NEON_GREEN}  - {NEON_YELLOW}{entity['name']} ({entity['type']}){NEON_RESET}")
                print(f"{NEON_GREEN}    Relationship: {NEON_WHITE}{entity['relationship']}{NEON_RESET}")
                if entity.get('image_path'):
                    print(f"{NEON_GREEN}    Image: {NEON_WHITE}{entity['image_path']}{NEON_RESET}")
    
    # Social media graph for username
    if target_type == "username" and results.get('graph_filename'):
        print(f"\n{NEON_BOLD_YELLOW}SOCIAL MEDIA GRAPH:{NEON_RESET}")
        print(f"{NEON_GREEN}  Graph saved as: {NEON_WHITE}{results['graph_filename']}{NEON_RESET}")
        
        # Ask if user wants to open the graph
        choice = input(f"\n{NEON_BLUE}Open social media graph? (y/n): {NEON_RESET}").strip().lower()
        if choice == 'y' or choice == 'yes':
            webbrowser.open(results['graph_filename'])
            print(f"{NEON_GREEN}Opening social media graph...{NEON_RESET}")

def open_manual_portals(email):
    """Ask user if they want to open manual lookup portals in browser"""
    print(f"\n{NEON_BOLD_YELLOW}OPEN MANUAL LOOKUP PORTALS IN BROWSER?{NEON_RESET}")
    choice = input(f"{NEON_GREEN}Open manual lookup portals for {NEON_YELLOW}{email}{NEON_GREEN}? (y/n): {NEON_RESET}").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        portals = manual_lookup_portals(email)
        print(f"{NEON_GREEN}Opening manual lookup portals...{NEON_RESET}")
        
        for platform, url in portals.items():
            print(f"{NEON_GREEN}  Opening {NEON_YELLOW}{platform}{NEON_GREEN}...{NEON_RESET}")
            webbrowser.open(url)
            time.sleep(1)  # Small delay to avoid overwhelming the browser
        
        print(f"{NEON_GREEN}All manual lookup portals opened!{NEON_RESET}")
    else:
        print(f"{NEON_YELLOW}Skipping manual lookup portals.{NEON_RESET}")

def open_social_deep_dive(email, social_dive):
    """Ask user if they want to open social deep dive searches in browser"""
    print(f"\n{NEON_BOLD_YELLOW}OPEN SOCIAL DEEP DIVE IN BROWSER?{NEON_RESET}")
    choice = input(f"{NEON_GREEN}Open social deep dive searches for {NEON_YELLOW}{social_dive['extracted_name']}{NEON_GREEN}? (y/n): {NEON_RESET}").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        print(f"{NEON_GREEN}Opening social deep dive searches...{NEON_RESET}")
        
        count = 0
        for platform, url in social_dive['social_searches'].items():
            if count < 8:  # Open only top 8 to avoid overwhelming the browser
                print(f"{NEON_GREEN}  Opening {NEON_YELLOW}{platform}{NEON_GREEN}...{NEON_RESET}")
                webbrowser.open(url)
                time.sleep(1)  # Small delay to avoid overwhelming the browser
                count += 1
        
        print(f"{NEON_GREEN}Top social deep dive searches opened!{NEON_RESET}")
    else:
        print(f"{NEON_YELLOW}Skipping social deep dive.{NEON_RESET}")

def save_reports(target, results, target_type="email"):
    if target_type == "email":
        csv_filename = f"cyber_intel_report_{target.replace('@', '_at_')}.csv"
        pdf_filename = f"cyber_intel_report_{target.replace('@', '_at_')}.pdf"
        
        # Prepare data for CSV
        data_summary = {
            "Email": target,
            "Disposable": "Yes" if is_disposable(target) else "No",
            "Gravatar Found": "Yes" if results.get('gravatar') else "No",
            "GitHub Users": ", ".join([user.get("login", "") for user in results.get('github', [])]) or "None",
            "Data Breaches": len(results.get('breaches', [])),
            "Pastebin Hits": len(results.get('pastebin', [])),
            "Email Reputation": results.get('reputation', 'Unknown'),
            "Social Media URLs": "\n".join([f"{k}: {v}" for k, v in results.get('social_media', {}).items()]),
            "Manual Lookup Portals": "\n".join([f"{k}: {v}" for k, v in results.get('manual_portals', {}).items()]),
            "Social Deep Dive - Extracted Name": results.get('social_deep_dive', {}).get('extracted_name', 'None'),
            "Social Deep Dive - Top Platforms": "\n".join([f"{k}: {v}" for k, v in list(results.get('social_deep_dive', {}).get('social_searches', {}).items())[:5]]),
            "Google Dork URLs": "\n".join([f"{k}: {v}" for k, v in results.get('google_dorks', {}).items()]),
            "Entity Graph": results.get('entity_graph', 'Not generated'),
            "Entities Found": len(results.get('entities', []))
        }
        
        # Add Hunter.io data if available
        if results.get('hunter') and 'error' not in results['hunter']:
            hunter = results['hunter']
            data_summary["Hunter Status"] = hunter.get('status', 'Unknown')
            data_summary["Hunter Result"] = hunter.get('result', 'Unknown')
            data_summary["Hunter Score"] = hunter.get('score', 'N/A')
            data_summary["Disposable"] = "Yes" if hunter.get('disposable') else "No"
        
    elif target_type == "phone":
        csv_filename = f"cyber_intel_report_phone_{re.sub(r'[^0-9]', '', target)}.csv"
        pdf_filename = f"cyber_intel_report_phone_{re.sub(r'[^0-9]', '', target)}.pdf"
        
        # Prepare data for CSV
        validation = results.get('validation', {})
        data_summary = {
            "Phone Number": target,
            "Valid": validation.get('valid', False),
            "International Format": validation.get('international_format', ''),
            "National Format": validation.get('national_format', ''),
            "Location": validation.get('location', ''),
            "Carrier": validation.get('carrier', ''),
            "Timezone": ", ".join(validation.get('timezone', [])),
            "Google Dork URLs": "\n".join([f"{k}: {v}" for k, v in results.get('google_dorks', {}).items()])
        }
    
    elif target_type == "username":
        csv_filename = f"cyber_intel_report_username_{target}.csv"
        pdf_filename = f"cyber_intel_report_username_{target}.pdf"
        
        # Prepare data for CSV
        platforms_found = {k: v for k, v in results.get('platforms', {}).items() if v.get('status') == 'Found'}
        
        data_summary = {
            "Username": target,
            "Platforms Found": len(platforms_found),
            "Platform Details": "\n".join([f"{k}: {v.get('url', 'N/A')}" for k, v in platforms_found.items()]),
            "Graph File": results.get('graph_filename', 'Not generated')
        }
    
    # Save CSV
    pd.DataFrame([data_summary]).to_csv(csv_filename, index=False)
    
    # Save PDF
    generate_pdf_report(target, data_summary, pdf_filename)
    
    print(f"\n{NEON_BOLD_YELLOW}REPORTS SAVED:{NEON_RESET}")
    print(f"{NEON_GREEN}  CSV: {NEON_WHITE}{csv_filename}{NEON_RESET}")
    print(f"{NEON_GREEN}  PDF: {NEON_WHITE}{pdf_filename}{NEON_RESET}")

def cleanup_files(image_files):
    """Clean up temporary image files"""
    for file_path in image_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logging.error(f"Failed to delete file {file_path}: {e}")

# 4. Main Program --------------------------------------------------------------

def main():
    print_welcome()
    
    print(f"{NEON_BOLD_CYAN}Select analysis type:{NEON_RESET}")
    print(f"{NEON_GREEN}  1. Email Analysis{NEON_RESET}")
    print(f"{NEON_GREEN}  2. Social Media Scraper (Username){NEON_RESET}")
    print(f"{NEON_GREEN}  3. Phone Number Analysis{NEON_RESET}")
    
    choice = input(f"\n{NEON_BLUE}Enter your choice (1, 2, or 3): {NEON_RESET}").strip()
    
    image_files = []
    
    try:
        if choice == "1":
            target = input(f"{NEON_BLUE}Enter email address: {NEON_RESET}").strip()
            results = email_analysis(target)
            if results:
                print_results(target, results, "email")
                # Ask if user wants to open manual lookup portals
                open_manual_portals(target)
                # Ask if user wants to open social deep dive
                if results.get('social_deep_dive'):
                    open_social_deep_dive(target, results['social_deep_dive'])
                save_reports(target, results, "email")
                # Store image files for cleanup
                image_files = results.get('image_files', [])
        
        elif choice == "2":
            target = input(f"{NEON_BLUE}Enter username to search: {NEON_RESET}").strip()
            results = social_media_scraper(target)
            if results:
                print_results(target, results, "username")
                save_reports(target, results, "username")
                # Store image files for cleanup
                image_files = list(results.get('profile_images', {}).values())
        
        elif choice == "3":
            target = input(f"{NEON_BLUE}Enter phone number (with country code): {NEON_RESET}").strip()
            results = phone_analysis(target)
            if results:
                print_results(target, results, "phone")
                save_reports(target, results, "phone")
        
        else:
            print(f"{NEON_RED}Invalid choice. Exiting.{NEON_RESET}")
    
    except KeyboardInterrupt:
        print(f"\n{NEON_RED}Operation cancelled by user.{NEON_RESET}")
    except Exception as e:
        print(f"\n{NEON_RED}An error occurred: {e}{NEON_RESET}")
        logging.error(f"Error in main: {e}")
    finally:
        # Clean up temporary files
        if image_files:
            cleanup_files(image_files)

if __name__ == "__main__":
    main()
