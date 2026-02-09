from bs4 import BeautifulSoup
import re

file_path = "index.html"

with open(file_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1. Remove redundant headings (h3/h4) if followed by a video card with same title
headings = soup.find_all(["h3", "h4"])
for h in headings:
    # Get next sibling element (ignoring whitespace)
    next_sibling = h.find_next_sibling()
    while next_sibling and next_sibling.name is None: # Skip text nodes/comments
        next_sibling = next_sibling.next_sibling
    
    if next_sibling and next_sibling.name == "a" and "video-card" in next_sibling.get("class", []):
        # Compare text
        h_text = h.get_text(strip=True).lower()
        
        # Video card title is usually in a span
        span = next_sibling.find("span")
        if span:
            v_text = span.get_text(strip=True).lower()
            # Simple fuzzy match: if heading comprises most of video title or vice versa
            # Or strict match
            if h_text == v_text or h_text in v_text or v_text in h_text:
                print(f"Removing redundant heading: {h_text}")
                h.decompose()

# 2. Consolidate adjacent lists
lists = soup.find_all("ul", class_="links-list")
for ul in lists:
    if ul.parent is None: continue # Already processed/removed
    
    # Check next sibling
    next_sibling = ul.find_next_sibling()
    while next_sibling and next_sibling.name is None:
        next_sibling = next_sibling.next_sibling
        
    if next_sibling and next_sibling.name == "ul" and "links-list" in next_sibling.get("class", []):
        # Merge next_sibling content into ul
        print("Merging adjacent list")
        for li in next_sibling.find_all("li"):
            ul.append(li)
        next_sibling.decompose()
        # Process this ul again in next iteration? 
        # Actually simplest is to run this pass multiple times or handle recursive merge
        # But adjacent pairs logic handles A+B, then AB+C in next run if we loop carefully.
        # safe way: greedy merge current with all subsequent adjacent
        
        # Let's do a while loop for multiple adjacent
        current = ul
        while True:
            sib = current.find_next_sibling()
            while sib and sib.name is None: sib = sib.next_sibling
            if sib and sib.name == "ul" and "links-list" in sib.get("class", []):
                for li in sib.find_all("li"):
                    current.append(li)
                sib.decompose()
            else:
                break

# 3. Wrap video cards in video-grid and remove inline styles
# Find all video cards
video_cards = soup.find_all("a", class_="video-card")
for vc in video_cards:
    # Remove inline style
    if vc.has_attr("style"):
        del vc["style"]
    
    # Check if already in a grid?
    if vc.parent and "video-grid" in vc.parent.get("class", []):
        continue
        
    # Create or find grid
    # Logic: if previous sibling is a video grid, append to it. 
    # If duplicates/siblings are video cards, wrap them together.
    
    prev_sibling = vc.find_previous_sibling()
    while prev_sibling and prev_sibling.name is None: prev_sibling = prev_sibling.previous_sibling
    
    if prev_sibling and "video-grid" in prev_sibling.get("class", []):
        prev_sibling.append(vc)
    else:
        # Check if next sibling is video card? Or just wrap self and let next iteration join?
        # Better: create new grid, insert before vc, move vc inside.
        grid = soup.new_tag("div", attrs={"class": "video-grid"})
        vc.insert_before(grid)
        grid.append(vc)

# Save
with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup.prettify()))
