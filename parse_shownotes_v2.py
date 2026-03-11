import re
import os

BASE_DIR = r'c:\projects\antigravity_prj\jovd83_github_page'
MD_FILE = os.path.join(BASE_DIR, 'shownotes', 'GenZ_AILiteracy', 'shownotes.md')
HTML_FILE = os.path.join(BASE_DIR, 'shownotes', 'GenZ_AILiteracy', 'index.html')

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <link href="/vite.svg" rel="icon" type="image/svg+xml" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <link href="https://fonts.googleapis.com" rel="preconnect" />
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect" />
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&amp;family=Outfit:wght@500;700;800&amp;display=swap"
        rel="stylesheet" />
    <link href="/src/index.css" rel="stylesheet" />
    <link href="/src/App.css" rel="stylesheet" />
    <script src="/src/components/SiteHeader.js" type="module"></script>
    <title>JOVD | GenZ AI Literacy 101</title>
    <style>
        .main-title {
            text-align: center;
            margin-bottom: 2rem;
        }

        .item-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }

        .page-container {
            max-width: 95%;
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
            word-break: break-word;
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
            content: "\\2022";
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

        .video-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 1rem 0;
        }

        .video-card {
            display: block;
            text-decoration: none;
            color: var(--text-main);
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s;
            border: 1px solid var(--glass-border);
            width: 100%;
        }

        .video-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-primary);
        }

        .video-card img {
            width: 100%;
            height: auto;
            display: block;
            aspect-ratio: 16/9;
            object-fit: cover;
        }

        .video-card span {
            display: block;
            padding: 0.5rem;
            font-size: 0.9rem;
            line-height: 1.3;
        }

        .layout-wrapper {
            display: block;
            width: 100%;
        }

        .main-content {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }

        .intro-block {
            margin-bottom: 3rem;
        }

        .parts-list {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .back-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--accent-primary);
            color: #000;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s, transform 0.2s, background-color 0.2s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            text-decoration: none;
        }

        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }

        .back-to-top:hover {
            transform: translateY(-5px);
            background: var(--accent-secondary);
        }

        .section-details summary {
            cursor: pointer;
            outline: none;
            position: relative;
            color: var(--accent-primary);
            font-size: 1.8rem;
            font-family: 'Outfit', sans-serif;
            border-bottom: 1px solid var(--glass-border);
            padding-bottom: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .section-details summary .section-title {
            display: inline;
            border-bottom: none;
            padding-bottom: 0;
            margin-bottom: 0;
        }

        .section-details summary .part-img {
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            display: block;
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
            <div class="layout-wrapper">
                <main class="main-content">
                    <div class="intro-block">
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
                </main>
            </div>
        </div>
    </div>

    <a href="#" id="backToTop" class="back-to-top" title="Back to top">↑</a>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const backToTopButton = document.getElementById('backToTop');
            if (backToTopButton) {
                window.addEventListener('scroll', () => {
                    if (window.scrollY > 300) {
                        backToTopButton.classList.add('visible');
                    } else {
                        backToTopButton.classList.remove('visible');
                    }
                });

                backToTopButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                });
            }
        });
    </script>
</body>

</html>
"""

def get_youtube_id(url):
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def parse_markdown_to_html(md_content):
    lines = md_content.split('\n')
    content_html = []
    current_part_html = []
    
    first_part = True
    intro_lines = []
    
    def flush_video_grid(items):
        if not items: return []
        grid_items = []
        for item in items:
            if 'video-card' in item:
                # Extract the card content from the individual grid wrappers if they exist
                # Or just use the card as is if we changed how we generate them
                # For now, we'll just assume they are raw card HTML
                grid_items.append(item)
        if grid_items:
            return ['<div class="video-grid">'] + grid_items + ['</div>']
        return []

    def flush_part():
        nonlocal current_part_html
        if current_part_html:
            content_html.append('<div class="section-block">')
            content_html.append('    <details class="section-details">')
            
            # Find the summary
            summary = None
            other_items = []
            for item in current_part_html:
                if '<summary>' in item:
                    summary = item
                else:
                    other_items.append(item)
            
            if summary:
                content_html.append(summary)
            
            # Handle video grid grouping
            video_buffer = []
            for item in other_items:
                if 'video-card' in item:
                    video_buffer.append(item)
                else:
                    if video_buffer:
                        content_html.extend(flush_video_grid(video_buffer))
                        video_buffer = []
                    content_html.append(item)
            if video_buffer:
                content_html.extend(flush_video_grid(video_buffer))
            
            content_html.append('    </details>')
            content_html.append('</div>')
            current_part_html = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('image:'):
            continue
            
        if i < 3 and ('Ai Literacy 101' in line or line.lower() == 'shownotes'):
            continue
            
        if line.lower().startswith('# part'):
            if first_part:
                if intro_lines:
                    # Group intro videos too
                    v_buf = []
                    for il in intro_lines:
                        if 'video-card' in il: v_buf.append(il)
                        else:
                            if v_buf:
                                content_html.extend(flush_video_grid(v_buf))
                                v_buf = []
                            content_html.append(il)
                    if v_buf: content_html.extend(flush_video_grid(v_buf))
                    intro_lines = []
                content_html.append('</div> <!-- end intro-block -->')
                content_html.append('<div class="parts-list">')
                first_part = False
            else:
                flush_part()
            
            title = line.lstrip('#').strip()
            part_map = {
                'part i': 'PartI.png', 'part 1': 'PartI.png',
                'part ii': 'PartII.png', 'part 2': 'PartII.png',
                'part iii': 'PartIII.png', 'part 3': 'PartIII.png',
                'part iv': 'PartIV.png', 'part 4': 'PartIV.png',
                'part v': 'partV.png', 'part 5': 'partV.png',
                'part vi': 'PartVI.png', 'part 6': 'PartVI.png',
                'part vii': 'PartVII.png', 'part 7': 'PartVII.png',
            }
            
            img_file = "banner.png"
            sorted_keys = sorted(part_map.keys(), key=len, reverse=True)
            for k in sorted_keys:
                if k in title.lower():
                    img_file = part_map[k]
                    break
            
            summary_html = f'''        <summary>
            <h2 class="section-title">{title}</h2>
            <img src="./{img_file}" alt="{title}" class="part-img">
        </summary>'''
            current_part_html.append(summary_html)
            
        elif line.startswith('##'):
             title = line.lstrip('#').strip()
             current_part_html.append(f'<h3 class="subsection-title">{title}</h3>')
             
        elif '[' in line and '](' in line:
            try:
                # Match [text](url) non-greedily
                match = re.search(r'\[(.*?)\]\((.*?)\)', line)
                if match:
                    text = match.group(1)
                    url = match.group(2)
                    
                    # Clean up prefix/suffix
                    # Find where [text](url) starts and ends in the line
                    link_start = line.find('[' + text + '](' + url + ')')
                    if link_start == -1: # Fallback if text or url had special chars
                        link_start = line.find('[')
                    
                    prefix = line[:link_start].strip('*').strip('•').strip().strip(':').strip()
                    suffix = line[line.find(')', link_start)+1:].strip().strip(':').strip()
                    
                    full_display = text
                    if prefix: full_display = f"{prefix} {full_display}"
                    if suffix: full_display = f"{full_display} : {suffix}"

                    yt_id = get_youtube_id(url)
                    if yt_id:
                        card_html = f'''
                        <a href="{url}" target="_blank" class="video-card">
                            <img src="https://img.youtube.com/vi/{yt_id}/mqdefault.jpg" alt="{text}">
                            <span>{full_display}</span>
                        </a>'''
                        if first_part: intro_lines.append(card_html)
                        else: current_part_html.append(card_html)
                    else:
                        item_html = f'<ul class="links-list"><li><a href="{url}" target="_blank">{full_display}</a></li></ul>'
                        if first_part: intro_lines.append(item_html)
                        else: current_part_html.append(item_html)
                else:
                    if first_part: intro_lines.append(f'<p>{line}</p>')
                    else: current_part_html.append(f'<p>{line}</p>')
            except:
                if first_part: intro_lines.append(f'<p>{line}</p>')
                else: current_part_html.append(f'<p>{line}</p>')

        elif line.startswith('#'):
             title = line.lstrip('#').strip()
             if first_part: intro_lines.append(f'<h2 class="section-title">{title}</h2>')
             else: current_part_html.append(f'<h2 class="section-title">{title}</h2>')
        else:
            if first_part: intro_lines.append(f'<p>{line}</p>')
            else: current_part_html.append(f'<p>{line}</p>')
                
    flush_part() 
    content_html.append('</div> <!-- end parts-list -->')
    return '\n'.join(content_html)

# Generate
with open(MD_FILE, 'r', encoding='utf-8') as f:
    md_content = f.read()

body_content = parse_markdown_to_html(md_content)
full_html = HTML_HEADER + body_content + HTML_FOOTER

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("HTML Generated Successfully")
