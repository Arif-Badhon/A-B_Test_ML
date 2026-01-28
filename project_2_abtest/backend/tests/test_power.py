import pytest
from services.power import PowerAnalyzer

def test_sample_size_calculation():
    n = PowerAnalyzer.sample_size(effect_size=0.5, alpha=0.05, power=0.8)
    assert n > 0
    assert isinstance(n, int)

def test_power_calculation():
    p = PowerAnalyzer.power(n=100, effect_size=0.5, alpha=0.05)
    assert 0 <= p <= 1

def test_mde_calculation():
    mde = PowerAnalyzer.minimum_detectable_effect(n=100, power=0.8, alpha=0.05)
    assert mde > 0

def test_power_curve():
    sizes = [10, 50, 100]
    curve = PowerAnalyzer.power_curve(sizes, effect_size=0.5)
    assert len(curve) == 3
    assert all(0 <= p <= 1 for p in curve)
