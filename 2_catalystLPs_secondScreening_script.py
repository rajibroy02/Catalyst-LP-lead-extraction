import pandas as pd
import os

input_filename = "stage2_final_list.csv" # REPLACE with your actual file name if different
output_filename = "catalyst_lps_final_submission.csv"

# file path error checkpoint
if not os.path.exists(input_filename):
    print(f"ERROR: Could not find '{input_filename}' in this folder.")
else:
    df = pd.read_csv(input_filename)
    original_count = len(df)

    # filtering & clearning

    # Removes rows where First Name is "Our" (from "Our firm...")
    df = df[df['first_name'] != "Our"]

    # remove "former"
    df = df[~df['title'].str.contains("Former|fmr|Past", case=False, na=False)]

    # Removes rows with ";" (multiple companies) or "<" (formatting errors) or "/"
    df = df[~df['company_domain'].str.contains(";|/|<", na=False)]

    # remove academic/ non-SAAS roles
    df = df[~df['title'].str.contains("Faculty", case=False, na=False)]
    
    # E. drop empty domains
    df = df.dropna(subset=['company_domain'])

    df.to_csv(output_filename, index=False)
    removed_count = original_count - len(df)

    print(f"-" * 30)
    print(f"CLEANUP COMPLETE.")
    print(f"Original Rows: {original_count}")
    print(f"Rows Removed:  {removed_count} (Former employees, broken domains, garbage)")
    print(f"Final Count:   {len(df)}")
    print(f"-" * 30)
    print(f"Saved verified list to: {output_filename}")