import re
import os

BASE_DIR = r'c:\projects\antigravity_prj\jovd83_github_page'
MD_FILE = os.path.join(BASE_DIR, 'shownotes', 'GenZ_AILiteracy', 'shownotes.md')
HTML_FILE = os.path.join(BASE_DIR, 'shownotes', 'GenZ_AILiteracy', 'index.html')

HTML_HEADER = """<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/src/index.css" />
    <link rel="stylesheet" href="/src/App.css" />
    <script type="module" src="/src/components/SiteHeader.js"></script>
    <title>JOVD | GenZ AI Literacy 101</title>
    <style>
        .page-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
            text-align: left;
        }
        .banner-img {
            width: 100%;
            border-radius: var(--radius-md);
            border: 1px solid var(--glass-border);
            margin-bottom: 2rem;
        }
        .section-block {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-md);
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .part-img {
            width: 100%;
            max-height: 300px;
            object-fit: cover;
            border-radius: var(--radius-sm);
            margin-bottom: 1rem;
        }
        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            color: var(--accent-primary);
            margin-bottom: 0.5rem;
            border-bottom: 1px solid var(--glass-border);
            padding-bottom: 0.5rem;
        }
        .subsection-title {
             font-family: 'Outfit', sans-serif;
             font-size: 1.3rem;
             color: var(--text-main);
             margin-top: 1.5rem;
             margin-bottom: 0.5rem;
        }
        .links-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .links-list li {
            margin-bottom: 0.5rem;
            padding-left: 1rem;
            position: relative;
        }
        .links-list li::before {
            content: "•";
            color: var(--accent-secondary);
            position: absolute;
            left: 0;
        }
        .links-list a {
            color: var(--text-main);
            text-decoration: none;
            border-bottom: 1px solid var(--accent-secondary);
            transition: all 0.2s;
        }
        .links-list a:hover {
            color: var(--accent-primary);
            border-bottom-color: var(--accent-primary);
        }
        
        /* YouTube Card Styles */
        .video-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        .video-card {
            display: block;
            text-decoration: none;
            color: var(--text-main);
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s;
            border: 1px solid var(--glass-border);
        }
        .video-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-primary);
        }
        .video-card img {
            width: 100%;
            height: auto;
            display: block;
        }
        .video-card span {
            display: block;
            padding: 0.5rem;
            font-size: 0.9rem;
            line-height: 1.3;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="hero">
            <site-header></site-header>
        </header>

        <div class="page-container">
            <h1 class="main-title">GenZ AI Literacy 101</h1>
            
            <img src="./banner.png" alt="GenZ AI Literacy Banner" class="banner-img">
            
            <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
                Welcome to the shownotes for the GenZ AI Literacy 101 talk. 
                Here you will find all the resources, links, and references mentioned during the presentation.
            </p>
"""

HTML_FOOTER = """
            <div class="section-block">
                 <h2 class="section-title">My AI Radar</h2>
                 <p>My AI toolkit: Podcasts, newsletters, blogs, youtube-channels, courses, tools, benchmarks, libraries and frameworks.</p>
                 <ul class="links-list">
                    <li><a href="http://ai.jochimvandorpe.be" target="_blank">http://ai.jochimvandorpe.be</a></li>
                 </ul>
            </div>

            <a href="/shownotes.html" class="back-link">← Back to Shownotes</a>
        </div>
    </div>
</body>
</html>
"""

def get_youtube_id(url):
    # Regex to capture video ID from various YT url formats
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def parse_md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    content_html = []
    
    current_part_html = []
    in_video_grid = False
    
    def flush_part():
        nonlocal current_part_html
        if current_part_html:
            content_html.append('<div class="section-block">')
            content_html.extend(current_part_html)
            content_html.append('</div>')
            current_part_html = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect Part Headers (# Part X)
        if line.lower().startswith('# part'):
            flush_part()
            
            title = line.lstrip('#').strip()
            # Try to extract number for image mapping
            # Mapping based on strict file list provided earlier
            part_map = {
                'part i': 'PartI.png', 'part 1': 'PartI.png',
                'part ii': 'PartII.png', 'part 2': 'PartII.png',
                'part iii': 'PartIII.png', 'part 3': 'PartIII.png',
                'part iv': 'PartIV.png', 'part 4': 'PartIV.png',
                'part v': 'partV.png', 'part 5': 'partV.png', # Note lowercase p in file
                'part vi': 'PartVI.png', 'part 6': 'PartVI.png',
                'part vii': 'PartVII.png', 'part 7': 'PartVII.png',
            }
            
            img_file = "banner.png" # Default fallback
            for k, v in part_map.items():
                if k in title.lower():
                    img_file = v
                    break
            
            current_part_html.append(f'<h2 class="section-title">{title}</h2>')
            current_part_html.append(f'<img src="./{img_file}" alt="{title}" class="part-img">')
            
        # Detect Subheaders (## Title)
        elif line.startswith('##'):
             title = line.lstrip('#').strip()
             current_part_html.append(f'<h3 class="subsection-title">{title}</h3>')
             
        # Detect Links
        elif 'http' in line:
            # Extract URL
            url_match = re.search(r'(https?://[^\s]+)', line)
            if url_match:
                url = url_match.group(1)
                text = line.replace(url, '').strip().strip('*').strip('•').strip(':').strip()
                if not text:
                    text = "Link" # Fallback if no text
                if len(text) > 100: # If text is essentially the whole paragraph, just truncate or use it
                     pass

                # Check for YouTube
                yt_id = get_youtube_id(url)
                if yt_id:
                     # If previous element was not a video grid, start one?
                     # Ideally we group consecutive videos. Simple approach: just render as card.
                     # But flex/grid is better.
                     # Let's clean up logic: just append the card, css handles flow? 
                     # Better to wrap in a container if possible, but line-by-line parsing makes it hard.
                     # We'll just dump the card.
                     card_html = f'''
                    <a href="{url}" target="_blank" class="video-card" style="display:inline-block; width: 220px; vertical-align: top; margin-right: 10px; margin-bottom: 10px;">
                        <img src="https://img.youtube.com/vi/{yt_id}/mqdefault.jpg" alt="{text}">
                        <span>{text}</span>
                    </a>'''
                     current_part_html.append(card_html)
                else:
                    item_html = f'<ul class="links-list"><li><a href="{url}" target="_blank">{text}</a></li></ul>'
                    current_part_html.append(item_html)
            else:
                 current_part_html.append(f'<p>{line}</p>')
        else:
            # Regular text
            if len(line) > 3 and not line.startswith('image:'):
                current_part_html.append(f'<p>{line}</p>')
                
    flush_part() # Flush last part
    return '\n'.join(content_html)

# Generate
body_content = parse_md_to_html(MD_FILE)
full_html = HTML_HEADER + body_content + HTML_FOOTER

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("HTML Generated Successfully")
