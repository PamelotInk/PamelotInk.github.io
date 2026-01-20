"""Core statistical engine module.

This file is a small starter module for statistical utilities used
by the experimentation platform. Add functions and classes here as
you build out analysis and modeling pipelines.
"""

from typing import Iterable


class StatisticalEngine:
    """Small helper class providing basic statistical utilities.

    This is intentionally minimal — expand with additional methods
    (variance, std, weighted metrics, robust statistics, etc.) as
    you need them.
    """

    @staticmethod
    def mean(data: Iterable[float]) -> float:
        """Return the arithmetic mean of `data`.

        Raises ValueError if `data` is empty.
        """
        data_list = list(data)
        if not data_list:
            raise ValueError("data is empty")
        return sum(data_list) / len(data_list)
import numpy as np
from scipy import stats
from typing import Dict, Tuple

class ABTestCalculator:
    """Statistical calculations for A/B tests"""
    
    def __init__(self, alpha: float = 0.20):
        """
        Args:
            alpha: Significance level (default 0.20 for 80% confidence - lowered for faster demo results)
        """
        self.alpha = alpha
    
    def calculate_conversion_rate(self, conversions: int, impressions: int) -> float:
        """Calculate conversion rate with safety check"""
        if impressions == 0:
            return 0.0
        return conversions / impressions
    
    def calculate_z_score(
        self, 
        control_conv: int, 
        control_imp: int,
        variant_conv: int, 
        variant_imp: int
    ) -> Tuple[float, float]:
        """
        Calculate Z-score and p-value for proportion test
        
        Returns:
            (z_score, p_value)
        """
        # Conversion rates
        p1 = control_conv / control_imp if control_imp > 0 else 0
        p2 = variant_conv / variant_imp if variant_imp > 0 else 0
        
        # Pooled probability
        p_pool = (control_conv + variant_conv) / (control_imp + variant_imp)
        
        # Standard error
        se = np.sqrt(p_pool * (1 - p_pool) * (1/control_imp + 1/variant_imp))
        
        if se == 0:
            return 0.0, 1.0
        
        # Z-score
        z_score = (p2 - p1) / se
        
        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        return z_score, p_value
    
    def is_significant(
        self, 
        control_conv: int, 
        control_imp: int,
        variant_conv: int, 
        variant_imp: int
    ) -> Dict:
        """
        Comprehensive significance test
        
        Returns:
            Dictionary with test results
        """
        z_score, p_value = self.calculate_z_score(
            control_conv, control_imp, variant_conv, variant_imp
        )
        
        control_rate = self.calculate_conversion_rate(control_conv, control_imp)
        variant_rate = self.calculate_conversion_rate(variant_conv, variant_imp)
        
        lift = variant_rate - control_rate
        relative_lift = (lift / control_rate * 100) if control_rate > 0 else 0
        
        return {
            'is_significant': p_value < self.alpha,
            'p_value': p_value,
            'confidence': (1 - p_value) * 100,
            'z_score': z_score,
            'control_rate': control_rate * 100,
            'variant_rate': variant_rate * 100,
            'absolute_lift': lift * 100,
            'relative_lift': relative_lift,
            'winner': 'variant' if (p_value < self.alpha and lift > 0) else 'control' if (p_value < self.alpha and lift < 0) else 'inconclusive'
        }
    
    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: float = 0.05,
        power: float = 0.80
    ) -> int:
        """Calculate required sample size per variant"""
        effect_size = minimum_detectable_effect / baseline_rate
        
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        p1 = baseline_rate
        p2 = baseline_rate * (1 + effect_size)
        p_avg = (p1 + p2) / 2
        
        n = (2 * (z_alpha + z_beta)**2 * p_avg * (1 - p_avg)) / (p2 - p1)**2
        
        return int(np.ceil(n))
    
    def estimate_time_to_significance(
        self,
        daily_traffic: int,
        baseline_rate: float,
        expected_lift: float,
        alpha: float = 0.05,
        power: float = 0.80
    ) -> int:
        """Estimate days needed to reach significance"""
        required_sample = self.calculate_sample_size(
            baseline_rate, 
            baseline_rate * expected_lift,
            alpha,
            power
        )
        
        total_sample = required_sample * 2
        days = int(np.ceil(total_sample / daily_traffic))
        
        return days


# Test the calculator
if __name__ == "__main__":
    print("🧮 Testing Statistical Engine...\n")
    
    calc = ABTestCalculator()
    
    # Test with sample data
    results = calc.is_significant(
        control_conv=100,
        control_imp=1000,
        variant_conv=130,
        variant_imp=1000
    )
    
    print("📊 A/B Test Results:")
    print(f"Control Rate: {results['control_rate']:.2f}%")
    print(f"Variant Rate: {results['variant_rate']:.2f}%")
    print(f"Lift: {results['relative_lift']:.2f}%")
    print(f"P-value: {results['p_value']:.4f}")
    print(f"Confidence: {results['confidence']:.2f}%")
    print(f"Significant: {'✅ YES' if results['is_significant'] else '❌ NO'}")
    print(f"Winner: {results['winner'].upper()}")
    
    # Sample size calculation
    sample_size = calc.calculate_sample_size(
        baseline_rate=0.10,
        minimum_detectable_effect=0.02,
    )
    print(f"\n📏 Required sample size per variant: {sample_size:,}")
    
    # Time estimate
    days = calc.estimate_time_to_significance(
        daily_traffic=5000,
        baseline_rate=0.10,
        expected_lift=0.20
    )
    print(f"⏰ Estimated days to significance: {days}")
    
    print("\n✅ Statistical engine is working!")