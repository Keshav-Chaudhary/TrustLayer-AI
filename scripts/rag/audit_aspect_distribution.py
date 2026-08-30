import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
HOTELS_PATH = os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv')
REPORT_PATH = os.path.join(SCRIPT_DIR, '../../research/reports/aspect_distribution_audit.md')

def get_stats(series):
    series = series.dropna()
    return {
        'mean': np.mean(series),
        'std': np.std(series),
        'min': np.min(series),
        'max': np.max(series),
        'p5': np.percentile(series, 5),
        'p50': np.median(series),
        'p95': np.percentile(series, 95)
    }

def main():
    print("Loading data...")
    df_hotels = pd.read_csv(HOTELS_PATH)
    
    aspects = [
        'cleanliness_score',
        'service_score',
        'location_score',
        'value_for_money_score',
        'staff_behavior_score'
    ]
    
    other_signals = [
        'trust_score',
        'rating_score',
        'sentiment_score'
    ]
    
    report_content = "# Aspect Distribution Audit\n\n## 1. Aspect Scores Analysis\n\n"
    report_content += "| Feature | Mean | Std Dev | Min | Max | P5 | P50 (Median) | P95 | Status |\n"
    report_content += "|---|---|---|---|---|---|---|---|---|\n"
    
    recommendations = []
    
    for aspect in aspects:
        stats = get_stats(df_hotels[aspect])
        status = "Pass (>= 0.05)" if stats['std'] >= 0.05 else "Fail (< 0.05)"
        rec = "Retrieval + Explanation" if stats['std'] >= 0.05 else "Explanation-only"
        recommendations.append(f"- **{aspect}**: Std={stats['std']:.4f} -> Recommendation: **{rec}**")
        
        report_content += f"| {aspect} | {stats['mean']:.4f} | {stats['std']:.4f} | {stats['min']:.4f} | {stats['max']:.4f} | {stats['p5']:.4f} | {stats['p50']:.4f} | {stats['p95']:.4f} | {status} |\n"
        
    report_content += "\n## 2. Recommendation Signals Analysis\n\n"
    report_content += "| Feature | Mean | Std Dev | Min | Max | P5 | P50 (Median) | P95 |\n"
    report_content += "|---|---|---|---|---|---|---|---|\n"
    
    for sig in other_signals:
        stats = get_stats(df_hotels[sig])
        report_content += f"| {sig} | {stats['mean']:.4f} | {stats['std']:.4f} | {stats['min']:.4f} | {stats['max']:.4f} | {stats['p5']:.4f} | {stats['p50']:.4f} | {stats['p95']:.4f} |\n"
        
    report_content += "\n## 3. Final Recommendation\n\n"
    for r in recommendations:
        report_content += r + "\n"
        
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"Report successfully generated at {REPORT_PATH}")

if __name__ == "__main__":
    main()
