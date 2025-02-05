import cProfile
from animate_instrument_panel import animate_instrument_panel

cProfile.run('animate_instrument_panel("tracklog_test.csv")', 'profile_results')
