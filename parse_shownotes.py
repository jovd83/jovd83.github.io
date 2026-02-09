import re

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_parts = []
    current_part = None
    current_section = None
    
    # Regex for links: [Title](URL) or just URL or Title: URL
    # varied formats in the file:
    # "text https://url"
    # "* text: https://url"
    # "https://url"
    
    url_pattern = re.compile(r'(https?://[^\s]+)')

    def get_youtube_id(url):
        if 'youtube.com' in url or 'youtu.be' in url:
            # simple regex for youtube id
            match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', url)
            if match:
                return match.group(1)
        return None

    def format_link(line):
        url_match = url_pattern.search(line)
        if hasattr(url_match, 'group'):
            url = url_match.group(1)
            text = line.replace(url, '').strip().strip('•').strip('*').strip(':').strip()
            if not text:
                text = "Link"
            
            yt_id = get_youtube_id(url)
            if yt_id:
                # YouTube Card
                return f'''
                    <a href="{url}" target="_blank" class="video-card">
                        <img src="https://img.youtube.com/vi/{yt_id}/mqdefault.jpg" alt="{text}" loading="lazy">
                        <div class="play-icon">▶</div>
                        <span>{text}</span>
                    </a>'''
            else:
                # Standard Link
                return f'<li><a href="{url}" target="_blank">{text}</a></li>'
        return f'<li>{line.strip()}</li>'

    buffer_links = []
    
    def flush_links():
        nonlocal buffer_links
        if buffer_links:
            # Check if all are youtube cards
            has_yt = any('video-card' in l for l in buffer_links)
            if has_yt:
                 html_parts.append('<div class="video-grid">')
                 for l in buffer_links:
                     if 'video-card' in l:
                         html_parts.append(l)
                     else:
                         # if mixed, wrap non-yt in ul? or just render
                         if l.startswith('<li>'):
                             html_parts.append(f'<ul class="links-list">{l}</ul>')
                         else:
                             html_parts.append(l)
                 html_parts.append('</div>')
            else:
                html_parts.append('<ul class="links-list">')
                html_parts.append(''.join(buffer_links))
                html_parts.append('</ul>')
            buffer_links = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.lower().startswith('# part'):
            flush_links()
            # New Part
            if current_part:
                html_parts.append('</div>') # Close previous section-block
            
            title = line.strip('#').strip()
            part_num_match = re.search(r'Part\s+([IVX]+|I|II|III|IV|V|VI|VII)', title, re.IGNORECASE)
            part_num = part_num_match.group(1) if part_num_match else "I"  # Default/Fallback
            
            # Normalize image name: PartI.png, PartII.png, etc.
            # File names on disk: PartI.png, PartII.png, PartIII.png, PartIV.png, partV.png, PartVI.png, PartVII.png
            img_name = f"Part{part_num}.png"
            if part_num == 'V': img_name = "partV.png" # fix casing for V based on file list
            
            html_parts.append(f'<div class="section-block">')
            html_parts.append(f'<h2 class="section-title">{title}</h2>')
            html_parts.append(f'<img src="./{img_name}" alt="{title}" class="part-img">')
            
        elif line.startswith('##'):
            flush_links()
            subtitle = line.strip('#').strip()
            html_parts.append(f'<h3 class="subsection-title">{subtitle}</h3>')
            
        elif line.startswith('http') or 'http' in line:
            buffer_links.append(format_link(line))
        else:
            # Regular text
            flush_links() # Flush previous links if any
            html_parts.append(f'<p>{line}</p>')

    flush_links()
    if current_part or True: # Close last block
        html_parts.append('</div>')

    return '\n'.join(html_parts)

# Run and print
markup = parse_markdown(r'c:\projects\antigravity_prj\jovd83_github_page\shownotes\GenZ_AILiteracy\shownotes.md')
print(markup)
