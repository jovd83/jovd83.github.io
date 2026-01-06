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

            # Logic to handle missing image_url for Prompt Frameworks
            if safe_name == "prompt_frameworks":
                # Ensure image_url column exists if not present
                if 'image_url' not in df.columns:
                     df['image_url'] = ""
                
                # Iterate and try to find matching image
                img_dir = os.path.join("public", "img", "prompt_frameworks")
                for idx, row in df.iterrows():
                    if pd.isna(row.get('image_url')) or str(row.get('image_url')) == "":
                        title = str(row.get('Name') or row.get('Title') or "").strip()
                        if title:
                            
                            safe_title = title.lower()
                            # Replace specific chars with underscores
                            for char in " .()-":
                                safe_title = safe_title.replace(char, "_")
                            
                            # Deduplicate underscores BUT be careful not to over-clean if files rely on it?
                            # Actually, looking at `c_r_a_f_t_.png`, it corresponds to "C.R.A.F.T."
                            # "C." -> "c_"
                            # "R." -> "r_"
                            # "A." -> "a_"
                            # "F." -> "f_"
                            # "T." -> "t_"
                            # So "c_r_a_f_t_" is exactly what direct replacement gives.
                            
                            # "Few-Shot Prompting" -> "few_shot_prompting" (no trailing underscore)
                            # Checks:
                            # 1. Direct replacement (no strip)
                            # 2. Strip underscores
                            
                            candidates = []
                            candidates.append(safe_title) # Raw replacement (might have double underscores)
                            
                            cand1 = safe_title
                            while "__" in cand1: cand1 = cand1.replace("__", "_")
                            if cand1 not in candidates: candidates.append(cand1)
                            
                            cand2 = cand1.strip("_")
                            if cand2 not in candidates: candidates.append(cand2)
                            
                            img_path_rel = ""
                            found = False
                            
                            for cand in candidates:
                                img_filename = f"{cand}.png"
                                full_img_path = os.path.join(img_dir, img_filename)
                                if os.path.exists(full_img_path):
                                    img_path_rel = f"/jovd83_github_page/img/prompt_frameworks/{img_filename}"
                                    df.at[idx, 'image_url'] = img_path_rel
                                    found = True
                                    break
                            
                            if not found:
                                print(f"Warning: Could not find image for '{title}' (tried: {[c + '.png' for c in candidates]})")
            
            # Export to CSV
            df.to_csv(output_csv_path, index=False)
            print(f"Exported {sheet_name} to {output_csv_path}")
            
            # Export to CSV
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    excel_file = os.path.join("public", "data", "all_the_lists.xlsx")
    output_directory = os.path.join("public", "data")
    
    # Ensure output directory exists (though it should already)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    split_excel_to_csvs(excel_file, output_directory)
