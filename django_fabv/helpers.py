"""
fabv specific help functions whose output can be fed into statistics.py
"""
from models import Experiment


def get_data(pk):
    experiment = Experiment.objects.select_related(depth=1).\
      get(pk=pk)
    alternatives = experiment.test_set
    if alternatives.count() != 2:
        raise ValueError("For now, fabv only works with 2 alternatives.")
    # 1. Collect all viewers of this Experiment
    # 2. Count hits on the goal page (once)
    # 3. Save in alternatives named tuple
    # 4. Use the statistics module
