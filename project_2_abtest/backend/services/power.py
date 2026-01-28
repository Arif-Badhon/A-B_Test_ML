import numpy as np
from scipy import stats
from typing import List

class PowerAnalyzer:
    @staticmethod
    def sample_size(effect_size: float, alpha: float = 0.05, power: float = 0.8) -> int:
        """Calculate required sample size per group.
        Formula: n = 2 * ((z_alpha + z_beta) / effect_size)^2
        """
        if effect_size <= 0:
            return 0
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        n = 2 * ((z_alpha + z_beta) / effect_size)**2
        return int(np.ceil(n))
        
    @staticmethod
    def power(n: int, effect_size: float, alpha: float = 0.05) -> float:
        """Calculate statistical power given sample size.
        Using normal approximation.
        """
        if n <= 0 or effect_size <= 0:
            return 0.0
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        # Non-centrality parameter (approx)
        delta = effect_size * np.sqrt(n / 2)
        power = 1 - stats.norm.cdf(z_alpha - delta) + stats.norm.cdf(-z_alpha - delta)
        return float(power)
        
    @staticmethod
    def minimum_detectable_effect(n: int, power: float = 0.8, alpha: float = 0.05) -> float:
        """Calculate MDE given sample size and power."""
        if n <= 0:
            return 0.0
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        mde = (z_alpha + z_beta) * np.sqrt(2 / n)
        return float(mde)
        
    @staticmethod
    def power_curve(sample_sizes: List[int], effect_size: float, alpha: float = 0.05) -> List[float]:
        """Generate power curve data."""
        return [PowerAnalyzer.power(n, effect_size, alpha) for n in sample_sizes]
