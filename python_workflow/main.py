#from build_AI import build_AI
from build_instrument_panel import build_instrument_panel

#filename = 'tracklog_test'
filename = 'tracklog.csv'

# write only the csv output file?
# True = only write the csv output file without overwriting the mp4 file
# False = write video mp4 file and csv file
logOnly = False

#build_AI(filename, logOnly)
build_instrument_panel(filename, logOnly)

# place AI on frame:
# scale 0.239, 0.239
# x, y  -100,  -405

# GSI_HI_ASI:
# scale 0.400, 0.400
# x, y  -569,  -687