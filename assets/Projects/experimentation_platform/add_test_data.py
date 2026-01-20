from core.data_manager import ExperimentDataManager
from datetime import date
from random import randint

dm = ExperimentDataManager()

# Add data to experiment 1
print("Adding test data...")

for i in range(10):
    # Control variant
    dm.log_metrics(
        experiment_id=1,
        variant_name='control',
        date_val=date.today(),
        impressions=1000,
        conversions=randint(90, 110),  # ~10% conversion
        revenue=randint(900, 1100)
    )
    
    # Variant A - performing better
    dm.log_metrics(
        experiment_id=1,
        variant_name='variant_a',
        date_val=date.today(),
        impressions=1000,
        conversions=randint(110, 130),  # ~12% conversion
        revenue=randint(1100, 1300)
    )

print("✅ Test data added!")