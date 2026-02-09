
from bs4 import BeautifulSoup
import re
import os

HTML_FILE = 'shownotes/GenZ_AILiteracy/index.html'

def clean_slug(url):
    # Remove trailing slash
    if url.endswith('/'):
        url = url[:-1]
    
    # Get last part
    parts = url.split('/')
    slug = parts[-1]
    
    # If slug is query string (e.g. ?v=...), try previous part?
    # actually for standard URLs usually last part is good.
    # for youtube, slug is 'watch?v=...' or similar.
    
    # Clean up
    # Replace - _ + with space
    text = re.sub(r'[-_+]', ' ', slug)
    
    # Remove file extension if present (e.g. .html, .php)
    if '.' in text:
        text = text.rsplit('.', 1)[0]
        
    # Title Case
    # Split by camelCase if needed? simpler is just built-in title()
    return text.title()

def enrich_html():
    if not os.path.exists(HTML_FILE):
        print(f"File not found: {HTML_FILE}")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find all 'a' tags
    links = soup.find_all('a')
    
    count = 0
    for link in links:
        # Check text content. 
        # For video cards, the text is in a span
        span = link.find('span')
        if span:
            current_text = span.get_text().strip()
        else:
            current_text = link.get_text().strip()
            
        if current_text.lower() == 'link':
            href = link.get('href', '')
            if not href:
                continue
                
            new_text = ""
            
            # Logic for YouTube
            if 'youtube.com' in href or 'youtu.be' in href:
                # Look for preceding paragraph
                prev = link.find_previous_sibling()
                # Skip string nodes
                while prev and isinstance(prev, str):
                     prev = prev.find_previous_sibling()
                
                if prev and prev.name == 'p':
                    # Use paragraph text
                    new_text = prev.get_text().strip()
                    # Clean up leading '* ' if present
                    if new_text.startswith('* '):
                        new_text = new_text[2:]
                else:
                    new_text = "Watch Video"
            else:
                # Logic for other URLs: use slug
                new_text = clean_slug(href)
                # Fallback if slug is empty or weird
                if len(new_text) < 3:
                     # Try domain or second to last part?
                     new_text = "Read Article"

            # Check for bad slugs like "Index.Php" or "Watch"
            if new_text.lower() in ['index', 'watch', 'default']:
                 new_text = "Read Article"

            # Apply new text
            if span:
                span.string = new_text
                # Also update img alt if generic
                img = link.find('img')
                if img and img.get('alt') == 'Link':
                    img['alt'] = new_text
            else:
                link.string = new_text
                
            print(f"Updated: {href[:40]}... -> {new_text}")
            count += 1
            
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
        
    print(f"Total links updated: {count}")

if __name__ == "__main__":
    enrich_html()
