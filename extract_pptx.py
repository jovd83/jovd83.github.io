
import zipfile
import re
import os
import sys
import xml.etree.ElementTree as ET

def extract_text_from_pptx(pptx_path):
    text_content = []
    
    try:
        with zipfile.ZipFile(pptx_path, 'r') as pptx_zip:
            # Find all slide XML files
            slide_files = [f for f in pptx_zip.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            # Sort slides by number (slide1, slide2, ..., slide10, etc.)
            slide_files.sort(key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1)))
            
            for slide_file in slide_files:
                slide_num = re.search(r'slide(\d+)\.xml', slide_file).group(1)
                xml_content = pptx_zip.read(slide_file)
                root = ET.fromstring(xml_content)
                
                slide_text = []
                # Find all text elements (a:t) in the XML
                # The namespace map is complex in pptx, simpler to ignore namespaces in simple extraction or use wildcard
                # But lxml is not standard, so we use ElementTree.
                # ElementTree generic search
                
                for elem in root.iter():
                    if elem.tag.endswith('}t'): # Text tag in OpenXML
                        if elem.text:
                            slide_text.append(elem.text)
                            
                if slide_text:
                    text_content.append(f"--- Slide {slide_num} ---")
                    text_content.append("\n".join(slide_text))
                    text_content.append("\n")

    except Exception as e:
        return f"Error reading PPTX: {str(e)}"
        
    return "\n".join(text_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pptx.py <path_to_pptx>")
        sys.exit(1)
        
    pptx_path = sys.argv[1]
    if not os.path.exists(pptx_path):
        print(f"File not found: {pptx_path}")
        sys.exit(1)
        
    print(extract_text_from_pptx(pptx_path))
