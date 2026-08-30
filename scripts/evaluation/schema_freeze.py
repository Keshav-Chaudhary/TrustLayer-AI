import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(__file__)
FINAL_DATASET_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")
SCHEMA_CSV_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_dataset_schema.csv")
DICT_MD_PATH = os.path.join(SCRIPT_DIR, "../../research/reports/data_dictionary.md")

def freeze_schema():
    if not os.path.exists(FINAL_DATASET_PATH):
        raise FileNotFoundError(f"Could not find {FINAL_DATASET_PATH}")

    df = pd.read_csv(FINAL_DATASET_PATH)
    
    schema_data = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        schema_data.append({
            'Column Name': col,
            'Data Type': dtype,
            'Non-Null Count': non_null,
            'Description': 'TBD' # Needs manual refinement for final report
        })
        
    df_schema = pd.DataFrame(schema_data)
    
    os.makedirs(os.path.dirname(SCHEMA_CSV_PATH), exist_ok=True)
    df_schema.to_csv(SCHEMA_CSV_PATH, index=False)
    
    os.makedirs(os.path.dirname(DICT_MD_PATH), exist_ok=True)
    with open(DICT_MD_PATH, 'w') as f:
        f.write("# Final Hotel Dataset - Data Dictionary\n\n")
        f.write("| Column Name | Data Type | Description | Range/Values |\n")
        f.write("|-------------|-----------|-------------|--------------|\n")
        for col in df.columns:
            f.write(f"| `{col}` | `{df[col].dtype}` | [Description needed] | |\n")
            
    print(f"Schema frozen! Artifacts saved to:\n- {os.path.abspath(SCHEMA_CSV_PATH)}\n- {os.path.abspath(DICT_MD_PATH)}")

if __name__ == "__main__":
    freeze_schema()
