# Analyze profiling data from main.py

import pstats
from pstats import SortKey

p = pstats.Stats('profile_results')
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(20)
