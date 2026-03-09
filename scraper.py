import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_url(url, cookies_str=None):
    """
    Scrape content from a given URL using headless Chrome browser.
    
    Features:
    - Renders JavaScript and dynamic content (unlike simple HTTP requests)
    - Bypasses basic anti-bot detection (headless mode, user-agent spoofing)
    - Handles Cloudflare protection through CDP commands
    - Extracts text content and structures it as sentence blocks
    - Detects Facebook login walls and returns appropriate error messages
    
    Args:
        url (str): Target URL to scrape (Facebook posts, news articles, blogs, etc.)
        cookies_str (str, optional): Facebook cookies for accessing private content
                                     Format: "c_user=...; xs=..."
    
    Returns:
        dict: Contains:
            - 'success' (bool): Whether scraping succeeded
            - 'data' (list): Extracted text blocks as list of dicts:
                - 'text' (str): Sentence/paragraph content
                - 'source' (str): Domain name
                - 'time' (str): Extraction time label
            - 'message' (str): Status message (success or error description)
    
    Raises:
        Catches all exceptions and returns error dict instead of raising
    """
    domain = urlparse(url).netloc
    
    # Configure Selenium Headless Mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Masking as a regular browser
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        # Auto-manage ChromeDriver installation via webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands to prevent Cloudflare/bot detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })

        # Set page load timeout
        driver.set_page_load_timeout(30)
        driver.get(url)
        
        # Wait for body to be loaded and any dynamic content to settle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Simulate gentle scrolling to trigger lazy loading if any
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(1.5)

        # Get full rendered HTML source
        page_source = driver.page_source
        
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Check if the page successfully loaded content or hit a hard login wall
        page_text = soup.get_text().lower()
        if 'facebook.com' in domain and 'log in' in page_text and len(page_source) < 50000:
            return {
                'success': False,
                'data': [],
                'message': (
                    f"Facebook Login Wall detected. Could not scrape private/locked "
                    f"post on {domain}."
                )
            }
            
        # Clean up script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        extracted_text = ""
        # Broad scrape: look for structured content blocks
        for tag in soup.find_all(['p', 'span', 'article', 'div']):
            text = tag.get_text(separator=' ').strip()
            # Simple heuristic: ignore tiny menu texts, focus on sentences
            if len(text.split()) > 6 and len(text) > 30:  
                extracted_text += text + ". "

        # Clean up excessive newlines/spaces
        extracted_text = re.sub(r'\s+', ' ', extracted_text)

        if len(extracted_text) < 50:
            return {
                'success': False,
                'data': [],
                'message': (
                    f"Could not find meaningful text content on {domain}. "
                    f"Page might be entirely images or heavily protected."
                )
            }

        # Sentence/Block tokenization to create 'comments' array
        # Regex splits by sentence endings, keeping paragraphs that are decently long
        raw_sentences = [
            s.strip() for s in re.split(r'(?<=[.!?])\s+', extracted_text)
            if len(s.strip()) > 15
        ]
        
        # Deduping text blocks natively while preserving order
        seen = set()
        sentences = []
        for s in raw_sentences:
            if s not in seen:
                seen.add(s)
                sentences.append(s)
                
        # Limit extraction count so UI doesn't crash on huge articles
        sentences = sentences[:30]
        
        results = []
        for s in sentences:
            results.append({
                'text': s,
                'source': domain,
                'time': 'Vừa xong (Live)'
            })

        return {
            'success': True,
            'data': results,
            'message': (
                f"Successfully rendered JS and extracted {len(results)} text nodes "
                f"via Headless WebScraper."
            )
        }

    except Exception as e:
        return {
            'success': False,
            'data': [],
            'message': f"Lỗi cào dữ liệu nâng cao (Selenium): {str(e)}"
        }
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
