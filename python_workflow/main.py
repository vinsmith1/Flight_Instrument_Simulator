# main.py
# Feb 9, 2025
# Vincent Smith
#
# This script is the main entry point for the instrument panel animation project.
# It reads a tracklog file, processes the data, calculates frames, and renders the output.
# The script processes command line arguments and calls the animate_instrument_panel function.

#import sys
import argparse
from animate_instrument_panel import animate_instrument_panel

parser = argparse.ArgumentParser(description='Animate the instrument panel of an aircraft based on a tracklog file.')
parser.add_argument('tracklog_filename', type=str, help='Full path to the tracklog file')
parser.add_argument('frame_rate', default=30, type=int, help='Frame rate for the animation')
parser.add_argument('output_image_folder', default="output", type=str, help='Output folder for rendered images')
parser.add_argument('--logging', default=False, action='store_true', help='Enable logging')
args = parser.parse_args()

#if len(sys.argv) < 4:
#    print("Usage: python main.py <tracklog_filename> <frame_rate> <output_image_folder>")
#    input("Press Enter to exit...")
#    sys.exit(1)

#tracklog_filename = sys.argv[1]
#frame_rate = int(sys.argv[2])
#output_image_folder = sys.argv[3]

animate_instrument_panel(args.tracklog_filename, args.frame_rate, args.output_image_folder, args.logging)
