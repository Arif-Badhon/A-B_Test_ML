import pytest
from ..services.correction import MultipleTestingCorrection

def test_bonferroni():
    p_values = [0.01, 0.04, 0.1]
    res = MultipleTestingCorrection.bonferroni(p_values, alpha=0.05)
    # 0.01 * 3 = 0.03 (< 0.05) -> Significant
    # 0.04 * 3 = 0.12 (> 0.05) -> Not Significant
    assert res["significant"][0] == True
    assert res["significant"][1] == False
    assert res["adjusted_p_values"][0] == pytest.approx(0.03)
    assert res["adjusted_p_values"][2] == pytest.approx(0.3)

def test_fdr():
    p_values = [0.01, 0.02, 0.08]
    res = MultipleTestingCorrection.fdr(p_values, alpha=0.05)
    # Hand-calculating BH for [0.01, 0.02, 0.08] with n=3
    # i=3: 0.08 * 3 / 3 = 0.08
    # i=2: 0.02 * 3 / 2 = 0.03
    # i=1: 0.01 * 3 / 1 = 0.03
    assert res["adjusted_p_values"][0] <= 0.05
    assert res["adjusted_p_values"][1] <= 0.05
    assert res["significant"][0] == True
    assert res["significant"][1] == True
    assert res["significant"][2] == False

def test_empty_correction():
    res = MultipleTestingCorrection.bonferroni([])
    assert res["p_values"] == []
    res_fdr = MultipleTestingCorrection.fdr([])
    assert res_fdr["p_values"] == []
