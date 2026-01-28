import pytest
import numpy as np
from services.statistics import welch_ttest, cohens_d, calculate_ci, mannwhitneyu_test, chisquare_test, summary_statistics

def test_welch_ttest_significant():
    control = [1.0, 1.2, 1.1, 1.3, 1.0] * 10
    treatment = [2.0, 2.2, 2.1, 2.3, 2.0] * 10
    result = welch_ttest(control, treatment)
    assert result["p_value"] < 0.05
    assert result["conclusion"] == "Significant"

def test_welch_ttest_not_significant():
    control = [1.0, 1.1, 1.0, 1.1, 1.0] * 10
    treatment = [1.0, 1.1, 1.0, 1.2, 1.0] * 10
    result = welch_ttest(control, treatment)
    assert result["p_value"] > 0.05
    assert result["conclusion"] == "Not Significant"

def test_cohens_d_calculation():
    group1 = [1, 2, 3, 4, 5]
    group2 = [6, 7, 8, 9, 10]
    d = cohens_d(group1, group2)
    assert d > 0
    assert isinstance(d, float)

def test_confidence_interval():
    control = [10, 12, 11]
    treatment = [15, 17, 16]
    lower, upper = calculate_ci(control, treatment)
    assert lower < upper

def test_mannwhitneyu():
    group1 = [1, 2, 3, 4, 5]
    group2 = [10, 11, 12, 13, 14]
    result = mannwhitneyu_test(group1, group2)
    assert result["p_value"] < 0.05

def test_chisquare():
    observed = [10, 20]
    expected = [15, 15]
    result = chisquare_test(observed, expected)
    assert "p_value" in result

def test_summary_statistics():
    data = [1, 2, 3, 4, 5]
    stats = summary_statistics(data)
    assert stats["mean"] == 3.0
    assert stats["count"] == 5
