from typing import List, Dict
import numpy as np

class MultipleTestingCorrection:
    @staticmethod
    def bonferroni(p_values: List[float], alpha: float = 0.05) -> Dict:
        """Bonferroni correction.
        Adjusts p-values by multiplying by the number of tests.
        """
        n = len(p_values)
        if n == 0:
            return {"p_values": [], "adjusted_p_values": [], "significant": [], "alpha": alpha}
            
        adjusted_p = [min(p * n, 1.0) for p in p_values]
        significant = [p < alpha for p in adjusted_p]
        return {
            "p_values": p_values,
            "adjusted_p_values": adjusted_p,
            "significant": significant,
            "alpha": alpha
        }
        
    @staticmethod
    def fdr(p_values: List[float], alpha: float = 0.05) -> Dict:
        """False Discovery Rate (Benjamini-Hochberg).
        Controls the expected proportion of false discoveries.
        """
        n = len(p_values)
        if n == 0:
            return {"p_values": [], "adjusted_p_values": [], "significant": [], "alpha": alpha}
            
        indexed_p = list(enumerate(p_values))
        indexed_p.sort(key=lambda x: x[1])
        
        adjusted_p = [0.0] * n
        prev_p = 1.0
        # BH procedure: p_adj = min(p_i * n / i, p_{i+1})
        for i in range(n - 1, -1, -1):
            idx, p = indexed_p[i]
            rank = i + 1
            adj = (p * n) / rank
            adj = min(adj, prev_p)
            adjusted_p[idx] = min(adj, 1.0)
            prev_p = adj
            
        significant = [p < alpha for p in adjusted_p]
        return {
            "p_values": p_values,
            "adjusted_p_values": adjusted_p,
            "significant": significant,
            "alpha": alpha
        }
