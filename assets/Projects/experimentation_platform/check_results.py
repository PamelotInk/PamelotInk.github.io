"""
Automated results checker - writes significant results to a file.
No email password needed!
"""

from datetime import datetime
import json

from core.data_manager import ExperimentDataManager
from core.statistical_engine import ABTestCalculator


def check_and_save_results():
    """Check experiments and save significant results to a file"""
    dm = ExperimentDataManager()
    calc = ABTestCalculator()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🔍 Checking experiments at {timestamp}")
    
    active_exps = dm.get_active_experiments()
    
    if len(active_exps) == 0:
        print("No active experiments found.")
        return
    
    results = {
        'timestamp': timestamp,
        'significant_experiments': []
    }
    
    for idx, exp in active_exps.iterrows():
        results_df = dm.get_experiment_results(exp['experiment_id'])
        
        if len(results_df) >= 2 and results_df['total_impressions'].sum() > 0:
            control = results_df[results_df['variant_name'] == 'control'].iloc[0]
            variant = results_df[results_df['variant_name'] != 'control'].iloc[0]
            
            if control['total_impressions'] > 0 and variant['total_impressions'] > 0:
                stats = calc.is_significant(
                    control_conv=int(control['total_conversions']),
                    control_imp=int(control['total_impressions']),
                    variant_conv=int(variant['total_conversions']),
                    variant_imp=int(variant['total_impressions'])
                )
                
                if stats['is_significant']:
                    result = {
                        'experiment_name': exp['experiment_name'],
                        'experiment_id': exp['experiment_id'],
                        'control_rate': f"{stats['control_rate']:.2f}%",
                        'variant_rate': f"{stats['variant_rate']:.2f}%",
                        'lift': f"{stats['relative_lift']:.1f}%",
                        'confidence': f"{stats['confidence']:.1f}%",
                        'winner': stats['winner'],
                        'control_impressions': int(control['total_impressions']),
                        'control_conversions': int(control['total_conversions']),
                        'variant_impressions': int(variant['total_impressions']),
                        'variant_conversions': int(variant['total_conversions']),
                        'recommendation': '🚀 Ship the variant!' if stats['winner'] == 'variant' else '⚠️ Keep current version'
                    }
                    results['significant_experiments'].append(result)
                    print(f"✅ {exp['experiment_name']}: Significant result found!")
    
    # Save to file
    if results['significant_experiments']:
        # JSON format
        with open('experiment_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        # Human-readable format
        with open('experiment_results.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"🎯 EXPERIMENT RESULTS - {timestamp}\n")
            f.write("=" * 70 + "\n\n")
            
            for exp in results['significant_experiments']:
                f.write(f"📊 {exp['experiment_name']}\n")
                f.write("-" * 70 + "\n")
                f.write(f"Status: {'✅ WINNER DETECTED!' if exp['winner'] == 'variant' else '📊 Significant Result'}\n\n")
                
                f.write("METRICS:\n")
                f.write(f"  Control Rate:     {exp['control_rate']}\n")
                f.write(f"  Variant Rate:     {exp['variant_rate']}\n")
                f.write(f"  Lift:             {exp['lift']}\n")
                f.write(f"  Confidence:       {exp['confidence']}\n\n")
                
                f.write("SAMPLE SIZE:\n")
                f.write(f"  Control: {exp['control_impressions']:,} impressions, {exp['control_conversions']:,} conversions\n")
                f.write(f"  Variant: {exp['variant_impressions']:,} impressions, {exp['variant_conversions']:,} conversions\n\n")
                
                f.write(f"RECOMMENDATION: {exp['recommendation']}\n")
                f.write("=" * 70 + "\n\n")
        
        print(f"\n💾 Results saved to:")
        print(f"   - experiment_results.txt (readable)")
        print(f"   - experiment_results.json (data)")
        print(f"\n🎉 Found {len(results['significant_experiments'])} significant result(s)!")
    else:
        print("No significant results yet. Keep running experiments!")
        
        # Still write a file to show it's checking
        with open('experiment_results.txt', 'w', encoding='utf-8') as f:
            f.write(f"Last checked: {timestamp}\n")
            f.write("No significant results yet.\n")


if __name__ == "__main__":
    print("📊 Experiment Results Checker")
    print("=" * 70)
    
    check_and_save_results()
    
    print("\n✅ Check complete!")
    print("View results in: experiment_results.txt")
