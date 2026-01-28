import pandas as pd
import os

input_filename = "catalyst_lps_final_submission.csv"  # current file with 176 rows
output_filename = "catalyst_lps_strict_final.csv"     # The new, perfect file to submit

# Check if file exists to prevent errors
if not os.path.exists(input_filename):
    print(f"ERROR: Could not find '{input_filename}'. Make sure it is in this folder.")
else:
    df = pd.read_csv(input_filename)
    original_count = len(df)

    # more refining 
    def is_valid_senior_role(title):
        title = str(title).lower()
        disqualifiers = [
            "former", "fmr", "past",       # Not current
            "head of",                     # Not SVP+
            "director",                    # Includes "Senior Director" -> Remove
            "consultant", "coach",         # Not operating roles
            "faculty", "advisor", "owner"  # Not SaaS leadership
        ]
        
        if any(bad_word in title for bad_word in disqualifiers):
            return False

        # strict VP check
        if "vice president" in title:                 # "Vice President" alone is often too junior. We want SVP/EVP. 
            if "senior" not in title and "executive" not in title and "svp" not in title and "evp" not in title:  # Keep ONLY if it says "Senior" or "Executive"
                return False 

        # must match atleast one
        allowed = [
            'svp', 'evp', 'senior vice president', 'executive vice president', 
            'chief', 'cmo', 'cro', 'ceo', 'coo', 'cto', 'president', 'founder'
        ]
        
        return any(role in title for role in allowed)

    # filtering
    df_clean = df[df['title'].apply(is_valid_senior_role)]
    df_clean.to_csv(output_filename, index=False)
    
    removed_count = original_count - len(df_clean)
    print(f"-" * 40)
    print(f"STRICT CLEANUP COMPLETE.")
    print(f"Input Rows:      {original_count}")
    print(f"Rows Removed:    {removed_count} (Directors, Heads of, standard VPs)")
    print(f"Final Count:     {len(df_clean)}")
    print(f"-" * 40)
    print(f"READY TO SUBMIT: {output_filename}")