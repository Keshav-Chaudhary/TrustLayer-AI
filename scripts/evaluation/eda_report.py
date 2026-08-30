import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(__file__)
HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")
EDA_MD_PATH = os.path.join(SCRIPT_DIR, "../../research/reports/eda_report.md")

def generate_eda():
    df_h = pd.read_csv(HOTELS_PATH)
    
    os.makedirs(os.path.dirname(EDA_MD_PATH), exist_ok=True)
    
    with open(EDA_MD_PATH, 'w') as f:
        f.write("# Exploratory Data Analysis (EDA)\n\n")
        
        f.write("## Hotel Distribution by Area\n")
        area_dist = df_h['area_cluster'].value_counts()
        for area, count in area_dist.items():
            f.write(f"- {area}: {count}\n")
            
        f.write("\n## Rating Distribution\n")
        f.write(f"- Mean Rating: {df_h['rating_score'].mean():.2f}\n")
        f.write(f"- Median Rating: {df_h['rating_score'].median():.2f}\n")
        f.write(f"- Min Rating: {df_h['rating_score'].min():.2f}\n")
        f.write(f"- Max Rating: {df_h['rating_score'].max():.2f}\n")
        
        f.write("\n## Sentiment Distribution\n")
        f.write(f"- Average Trust Score: {df_h['trust_score'].mean():.2f}\n")
        f.write(f"- Average Cleanliness Score: {df_h['cleanliness_score'].mean():.2f}\n")
        
    print(f"EDA report generated at {os.path.abspath(EDA_MD_PATH)}")

if __name__ == "__main__":
    generate_eda()
