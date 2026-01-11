import pandas as pd
import os

def split_excel_to_csvs(excel_path, output_dir):
    try:
        # Load the Excel file
        xls = pd.ExcelFile(excel_path)
        
        # Iterate through each sheet
        for sheet_name in xls.sheet_names:
            # Read the sheet into a DataFrame (read everything as string to safeguard, header=None to manually find header)
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            
            # Find the header row
            header_idx = -1
            for i, row in df.iterrows():
                # Check if first column (or any) hints at a header
                first_val = str(row[0]).lower().strip()
                if first_val in ['title', 'name', 'tool', 'podcast']:
                    header_idx = i
                    break
            
            if header_idx != -1:
                # Set header from that row
                df.columns = df.iloc[header_idx]
                df = df[header_idx+1:]
            else:
                 # Fallback: assume row 0 is header (reload)
                 df = pd.read_excel(xls, sheet_name=sheet_name, header=0)

            # Clean sheet name for filename
            # 1. Lowercase and remove spaces/parens for initial cleanup
            base_name = sheet_name.lower().replace(" (2)", "").replace(" (3)", "").strip()
            
            # 2. Strict mapping to avoid partial matches (e.g. 'extra tools' matching 'tools')
            safe_name = base_name.replace(" ", "_")
            
            if base_name == "tools": safe_name = "tools"
            elif base_name == "extra tools" or base_name == "extartools": safe_name = "extra_tools"
            elif base_name == "prompt frameworks": safe_name = "prompt_frameworks"
            
            # Define the output CSV path
            output_csv_path = os.path.join(output_dir, f"{safe_name}.csv")

            # --- CUSTOM LOGIC: Only support libraries.csv regeneration if requested ---
            # Ideally controlled by args, but per user request, we enforce "libraries only" or handle libraries specifically
            is_libraries = (safe_name == "libraries")
            
            # NOTE: User asked to regenerate ONLY libraries.csv. 
            # We will skip all other sheets for this run to be safe.
            if not is_libraries:
                print(f"Skipping {sheet_name} (only regenerating Libraries)...")
                continue

            # Logic to handle missing image_url for Prompt Frameworks OR Libraries
            if safe_name == "prompt_frameworks" or safe_name == "libraries":
                # Ensure image_url column exists if not present
                if 'image_url' not in df.columns:
                     df['image_url'] = ""
                
                # Iterate and try to find matching image
                # Folder is libraries for libraries, prompt_frameworks for prompt_frameworks
                subfolder = "libraries" if safe_name == "libraries" else "prompt_frameworks"
                img_dir = os.path.join("public", "img", subfolder)
                
                for idx, row in df.iterrows():
                    # Only infer if empty
                    if pd.isna(row.get('image_url')) or str(row.get('image_url')) == "" or str(row.get('image_url')).lower() == 'nan':
                        title = str(row.get('Name') or row.get('Title') or "").strip()
                        if title:
                            safe_title = title.lower()
                            # Replace specific chars with underscores
                            for char in " .()-":
                                safe_title = safe_title.replace(char, "_")
                            
                            candidates = []
                            candidates.append(safe_title) # Raw replacement
                            
                            cand1 = safe_title
                            while "__" in cand1: cand1 = cand1.replace("__", "_")
                            if cand1 not in candidates: candidates.append(cand1)
                            
                            cand2 = cand1.strip("_")
                            if cand2 not in candidates: candidates.append(cand2)
                            
                            found = False
                            for cand in candidates:
                                img_filename = f"{cand}.png"
                                full_img_path = os.path.join(img_dir, img_filename)
                                if os.path.exists(full_img_path):
                                    img_path_rel = f"/img/{subfolder}/{img_filename}"
                                    df.at[idx, 'image_url'] = img_path_rel
                                    found = True
                                    break
                            
                            if not found:
                                print(f"Warning: Could not find image for '{title}' in {subfolder} (tried: {[c + '.png' for c in candidates]})")
            
            # Global cleanup: Replace old repo path with root path in all string columns
            # Using regex=True with a string pattern to match substrings
            df = df.replace(to_replace=r'/jovd83_github_page/', value='/', regex=True)
            
            # Double check specifically for image_url column if it exists
            if 'image_url' in df.columns:
                df['image_url'] = df['image_url'].astype(str).str.replace('/jovd83_github_page/', '/', regex=False)

            # Export to CSV
            df.to_csv(output_csv_path, index=False)
            print(f"Exported {sheet_name} to {output_csv_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    excel_file = os.path.join("public", "data", "all_the_lists.xlsx")
    output_directory = os.path.join("public", "data")
    
    # Ensure output directory exists (though it should already)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    split_excel_to_csvs(excel_file, output_directory)
