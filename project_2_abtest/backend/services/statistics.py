import numpy as np
from scipy import stats
from typing import List, Dict, Tuple

def cohens_d(group1: List[float], group2: List[float]) -> float:
    """Calculate Cohen's d effect size."""
    if len(group1) < 2 or len(group2) < 2:
        return 0.0
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return 0.0
        
    # Cohen's d
    d = (np.mean(group2) - np.mean(group1)) / pooled_std
    return float(d)

def calculate_ci(group1: List[float], group2: List[float], alpha: float = 0.05) -> Tuple[float, float]:
    """95% confidence interval for the difference of means (treatment - control)."""
    n1, n2 = len(group1), len(group2)
    m1, m2 = np.mean(group1), np.mean(group2)
    v1, v2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    # Standard error of the difference
    se = np.sqrt(v1/n1 + v2/n2)
    
    if se == 0:
        return 0.0, 0.0

    # Degrees of freedom (Welch-Satterthwaite)
    num = (v1/n1 + v2/n2)**2
    den = ((v1/n1)**2 / (n1-1)) + ((v2/n2)**2 / (n2-1))
    df = num / den
    
    # Critical t-value
    t_crit = stats.t.ppf(1 - alpha/2, df)
    
    diff = m2 - m1
    lower = diff - t_crit * se
    upper = diff + t_crit * se
    
    return float(lower), float(upper)

def welch_ttest(control: List[float], treatment: List[float]) -> Dict:
    """Welch's t-test (unequal variance)."""
    if not control or not treatment:
        raise ValueError("Groups cannot be empty")
        
    t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=False)
    d = cohens_d(control, treatment)
    ci_lower, ci_upper = calculate_ci(control, treatment)
    
    conclusion = "Significant" if p_val < 0.05 else "Not Significant"
    
    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "effect_size": d,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "conclusion": conclusion
    }

def mannwhitneyu_test(group1: List[float], group2: List[float]) -> Dict:
    """Mann-Whitney U test."""
    u_stat, p_val = stats.mannwhitneyu(group1, group2)
    conclusion = "Significant" if p_val < 0.05 else "Not Significant"
    return {
        "statistic": float(u_stat),
        "p_value": float(p_val),
        "conclusion": conclusion
    }

def chisquare_test(observed: List[int], expected: List[int] = None) -> Dict:
    """Chi-square test."""
    chi_stat, p_val = stats.chisquare(observed, f_exp=expected)
    conclusion = "Significant" if p_val < 0.05 else "Not Significant"
    return {
        "statistic": float(chi_stat),
        "p_value": float(p_val),
        "conclusion": conclusion
    }

def summary_statistics(data: List[float]) -> Dict:
    """Mean, std, min, max, count."""
    return {
        "mean": float(np.mean(data)),
        "std": float(np.std(data, ddof=1)) if len(data) > 1 else 0.0,
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "count": len(data)
    }
