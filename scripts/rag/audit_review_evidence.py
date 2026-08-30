import os
import json
import glob
import numpy as np
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
RAG_DIR = os.path.join(DATA_DIR, 'rag')
REPORT_PATH = os.path.join(SCRIPT_DIR, '../../research/reports/review_evidence_coverage.md')

def main():
    print(f"Auditing JSON documents in {RAG_DIR}...")
    json_files = glob.glob(os.path.join(RAG_DIR, '*.json'))
    
    total_hotels = len(json_files)
    
    metrics = {
        'pos_snip_1': 0, 'neg_snip_1': 0, 'pos_snip_3': 0, 'neg_snip_3': 0,
        'pos_theme_2': 0, 'neg_theme_2': 0, 'pos_theme_3': 0, 'neg_theme_3': 0,
        'zero_reviews': 0,
        'rich': 0, 'moderate': 0, 'sparse': 0, 'no_evidence': 0
    }
    
    review_counts = []
    
    pos_theme_freq = defaultdict(int)
    pos_theme_hotels = defaultdict(int)
    neg_theme_freq = defaultdict(int)
    neg_theme_hotels = defaultdict(int)
    
    for fpath in json_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            doc = json.load(f)
            
        pos_snips = len(doc['review_evidence']['positive_snippets'])
        neg_snips = len(doc['review_evidence']['negative_snippets'])
        tot_snips = pos_snips + neg_snips
        
        pos_themes = doc['positive_themes']
        neg_themes = doc['negative_themes']
        num_pos_themes = len(pos_themes)
        num_neg_themes = len(neg_themes)
        tot_themes = num_pos_themes + num_neg_themes
        
        # Snippet logic
        if pos_snips >= 1: metrics['pos_snip_1'] += 1
        if neg_snips >= 1: metrics['neg_snip_1'] += 1
        if pos_snips >= 3: metrics['pos_snip_3'] += 1
        if neg_snips >= 3: metrics['neg_snip_3'] += 1
        
        # Theme logic
        if num_pos_themes >= 2: metrics['pos_theme_2'] += 1
        if num_neg_themes >= 2: metrics['neg_theme_2'] += 1
        if num_pos_themes >= 3: metrics['pos_theme_3'] += 1
        if num_neg_themes >= 3: metrics['neg_theme_3'] += 1
        
        # Review count
        rc_str = doc.get('review_summary', '0')
        rc = int(rc_str.split(' ')[2]) if 'Based on' in rc_str else 0
        review_counts.append(rc)
        if rc == 0: metrics['zero_reviews'] += 1
        
        # Theme freq
        for t, count in pos_themes.items():
            pos_theme_freq[t] += count
            pos_theme_hotels[t] += 1
            
        for t, count in neg_themes.items():
            neg_theme_freq[t] += count
            neg_theme_hotels[t] += 1
            
        # Sparsity
        if pos_snips >= 3 and neg_snips >= 2 and tot_themes >= 3:
            metrics['rich'] += 1
        elif tot_snips >= 2 and tot_themes >= 2:
            metrics['moderate'] += 1
        elif tot_snips == 0 and tot_themes == 0:
            metrics['no_evidence'] += 1
        else:
            metrics['sparse'] += 1

    rc_arr = np.array(review_counts)
    
    def pct(val): return (val / total_hotels * 100) if total_hotels else 0
    
    # Gates
    g_pos_snip_1 = pct(metrics['pos_snip_1']) >= 85
    g_neg_snip_1 = pct(metrics['neg_snip_1']) >= 60
    g_pos_theme_2 = pct(metrics['pos_theme_2']) >= 70
    g_rich_mod = pct(metrics['rich'] + metrics['moderate']) >= 70
    
    all_gates_pass = all([g_pos_snip_1, g_neg_snip_1, g_pos_theme_2, g_rich_mod])
    
    report = f"""# Stage C.1: Review Evidence Coverage Audit

## 1. Review Snippet Coverage
- Hotels with >=1 positive snippet: {metrics['pos_snip_1']} ({pct(metrics['pos_snip_1']):.2f}%)
- Hotels with >=1 negative snippet: {metrics['neg_snip_1']} ({pct(metrics['neg_snip_1']):.2f}%)
- Hotels with >=3 positive snippets: {metrics['pos_snip_3']} ({pct(metrics['pos_snip_3']):.2f}%)
- Hotels with >=3 negative snippets: {metrics['neg_snip_3']} ({pct(metrics['neg_snip_3']):.2f}%)

## 2. Theme Coverage
- Hotels with >=2 positive themes: {metrics['pos_theme_2']} ({pct(metrics['pos_theme_2']):.2f}%)
- Hotels with >=2 negative themes: {metrics['neg_theme_2']} ({pct(metrics['neg_theme_2']):.2f}%)
- Hotels with >=3 positive themes: {metrics['pos_theme_3']} ({pct(metrics['pos_theme_3']):.2f}%)
- Hotels with >=3 negative themes: {metrics['neg_theme_3']} ({pct(metrics['neg_theme_3']):.2f}%)

## 3. Review Density
- Mean review count per hotel: {np.mean(rc_arr):.2f}
- Median review count per hotel: {np.median(rc_arr):.2f}
- P5: {np.percentile(rc_arr, 5):.2f}
- P50: {np.percentile(rc_arr, 50):.2f}
- P95: {np.percentile(rc_arr, 95):.2f}
- Hotels with zero reviews: {metrics['zero_reviews']} ({pct(metrics['zero_reviews']):.2f}%)

## 4. Theme Frequency Analysis

### Top 20 Positive Themes
| Theme | Frequency | Hotels Covered |
|---|---|---|
"""
    for t in sorted(pos_theme_freq, key=pos_theme_freq.get, reverse=True)[:20]:
        report += f"| {t} | {pos_theme_freq[t]} | {pos_theme_hotels[t]} |\n"
        
    report += "\n### Top 20 Negative Themes\n"
    report += "| Theme | Frequency | Hotels Covered |\n|---|---|---|\n"
    for t in sorted(neg_theme_freq, key=neg_theme_freq.get, reverse=True)[:20]:
        report += f"| {t} | {neg_theme_freq[t]} | {neg_theme_hotels[t]} |\n"
        
    report += f"""
## 5. Evidence Sparsity Analysis
- Rich Evidence: {metrics['rich']} ({pct(metrics['rich']):.2f}%)
- Moderate Evidence: {metrics['moderate']} ({pct(metrics['moderate']):.2f}%)
- Sparse Evidence: {metrics['sparse']} ({pct(metrics['sparse']):.2f}%)
- No Evidence: {metrics['no_evidence']} ({pct(metrics['no_evidence']):.2f}%)

## 6. Success Gates

| Gate | Target | Actual | Status |
|---|---|---|---|
| >=1 positive snippet | >=85% | {pct(metrics['pos_snip_1']):.2f}% | {"PASS" if g_pos_snip_1 else "FAIL"} |
| >=1 negative snippet | >=60% | {pct(metrics['neg_snip_1']):.2f}% | {"PASS" if g_neg_snip_1 else "FAIL"} |
| >=2 positive themes | >=70% | {pct(metrics['pos_theme_2']):.2f}% | {"PASS" if g_pos_theme_2 else "FAIL"} |
| Rich + Moderate Evidence | >=70% | {pct(metrics['rich'] + metrics['moderate']):.2f}% | {"PASS" if g_rich_mod else "FAIL"} |
"""
    if not all_gates_pass:
        report += """
## 7. Remediation Section
**Root Causes for Failure:**
The success gates failed due to insufficient review volume and thematic extraction capabilities in our heuristic script.
The `reviews_raw.csv` dataset is highly sparse.

**Recommended Document-Generation Fixes:**
1. **Relax Keyword Extraction**: Expand the `extract_themes()` keyword dictionaries to capture more variations of positive/negative sentiment to increase theme coverage.
2. **Explicit Evidence Exposure**: Preserve fidelity by accurately exposing 'evidence_level' in the metadata and adjusting prompt templates to handle sparse/no evidence safely. Do not invent reviews.
"""
    
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
