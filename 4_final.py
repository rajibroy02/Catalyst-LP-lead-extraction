import pandas as pd
import io
import os
#prev file
input_filename = "catalyst_lps_strict_final.csv"
output_filename = "catalyst_lps_ready_for_production.csv"

# defining blocklists
# title blocklist
BANNED_TITLE_KEYWORDS = [
    "fractional", "interim", "consultant", "coach", "advisor", 
    "principal", "principle", "faculty", "investor", "board member", "owner"
]

# domain blocklist
BANNED_DOMAIN_KEYWORDS = [
    "coaching", "consulting", "advisory", "associates", "venture", 
    "capital", "partners", "marketing", "agency", "recruiting", "search", "vc.", "vc"
]

if not os.path.exists(input_filename):
    print(f"ERROR: Could not find '{input_filename}'.")
    # Fallback to empty DF just to prevent crash
    df = pd.DataFrame(columns=['first_name', 'last_name', 'company_domain', 'title', 'source_of_truth'])
else:
    df = pd.read_csv(input_filename)

# filtering
original_count = len(df)

def contains_keyword(text, keywords):
    text = str(text).lower()
    return any(k in text for k in keywords)

# Filter 1: check titles
df_clean = df[~df['title'].apply(lambda x: contains_keyword(x, BANNED_TITLE_KEYWORDS))]

# Filter 2: check domains
df_clean = df_clean[~df['company_domain'].apply(lambda x: contains_keyword(x, BANNED_DOMAIN_KEYWORDS))]

# User Requests
# Add 'notes' column (Blank)
df_clean['notes'] = "" 

# drop full_names and keep first_name and last_name
if 'full_name' in df_clean.columns:
    df_clean = df_clean.drop(columns=['full_name'])

target_cols = ['first_name', 'last_name', 'company_domain', 'title', 'source_of_truth', 'notes']
available_cols = [c for c in target_cols if c in df_clean.columns]
df_clean = df_clean[available_cols]

df_clean.to_csv(output_filename, index=False)

removed_count = original_count - len(df_clean)

print(f"-" * 50)
print(f"INDUSTRIAL CLEANUP COMPLETE")
print(f"Input Rows:    {original_count}")
print(f"Rows Removed:  {removed_count}")
print(f"Final Count:   {len(df_clean)}")
print(f"-" * 50)
print(f"Adjustments:")
print(f" - Applied Title & Domain Blocklists")
print(f" - Removed 'full_name' column")
print(f" - Added blank 'notes' column")
print(f"-" * 50)
print(f"File Ready: {output_filename}")