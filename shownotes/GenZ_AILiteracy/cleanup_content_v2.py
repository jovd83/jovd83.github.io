from bs4 import BeautifulSoup
import re

file_path = "index.html"

with open(file_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1. Remove <p> tag if followed by <ul class="links-list"> or <div class="video-grid">
# AND the text is very similar to the link/card text
patterns_to_check = soup.find_all("p")

for p in patterns_to_check:
    # Get next sibling element
    next_sibling = p.find_next_sibling()
    while next_sibling and next_sibling.name is None: 
        next_sibling = next_sibling.next_sibling
    
    if not next_sibling: continue

    p_text = p.get_text(strip=True).lower()
    match_found = False

    # Case A: Next is a list with potential link
    if next_sibling.name == "ul" and "links-list" in next_sibling.get("class", []):
        # Check first link
        a = next_sibling.find("a")
        if a:
            a_text = a.get_text(strip=True).lower()
            # Fuzzy match or containment
            # e.g. "Guardrails" vs "Ai Guardrails" -> p_text in a_text
            if p_text in a_text or a_text in p_text:
                match_found = True
    
    # Case B: Next is a video grid with card
    elif next_sibling.name == "div" and "video-grid" in next_sibling.get("class", []):
         a = next_sibling.find("a", class_="video-card")
         if a:
            a_text = a.find("span").get_text(strip=True).lower() if a.find("span") else ""
            if p_text in a_text or a_text in p_text:
                match_found = True

    if match_found:
        print(f"Removing redundant P: '{p.get_text(strip=True)}' before '{next_sibling.name}'")
        p.decompose()

# 2. Specific manual cleanup for "Grandma exploit" if fuzzy match misses it
# "The grandma exploit" vs "Ai Grandma Exploit Used To Fool The System"
# The fuzzy match above (p_text in a_text) should catch "grandma exploit" in "ai grandma exploit..." theoretically.
# But let's verify.
# p="The grandma exploit" -> "the grandma exploit"
# a="Ai Grandma Exploit Used To Fool The System" -> "ai grandma exploit used to fool the system"
# "the grandma exploit" is NOT in "ai grandma exploit..." because of "The" vs "Ai" intro.
# So we need token overlap logic.

def check_overlap(text1, text2):
    t1 = set(text1.split())
    t2 = set(text2.split())
    # If 70% of words in shorter string are in longer string
    intersection = t1.intersection(t2)
    min_len = min(len(t1), len(t2))
    if min_len == 0: return False
    return len(intersection) / min_len > 0.6

# Re-run for missed ones using overlap
patterns_to_check_2 = soup.find_all("p")
for p in patterns_to_check_2:
    if p.parent is None: continue # Already deleted

    next_sibling = p.find_next_sibling()
    while next_sibling and next_sibling.name is None: 
        next_sibling = next_sibling.next_sibling
    
    if not next_sibling: continue
    
    p_text = p.get_text(strip=True).lower()
    
    target_text = ""
    if next_sibling.name == "ul" and "links-list" in next_sibling.get("class", []):
        a = next_sibling.find("a")
        if a: target_text = a.get_text(strip=True).lower()
    elif next_sibling.name == "div" and "video-grid" in next_sibling.get("class", []):
         a = next_sibling.find("a", class_="video-card")
         if a and a.find("span"): target_text = a.find("span").get_text(strip=True).lower()
         
    if target_text and check_overlap(p_text, target_text):
        print(f"Removing redundant P (Overlap): '{p.get_text(strip=True)}'")
        p.decompose()

with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup.prettify()))
