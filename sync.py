import argparse
import os
import tempfile

def valid_directory(path):
  if not os.path.isdir(path):
    raise argparse.ArgumentTypeError(f"{path} is not a valid directory")
  return os.path.abspath(path)


parser = argparse.ArgumentParser()
parser.add_argument("dirs", nargs=2, type=valid_directory, help="path to the source and destination directories")
args = parser.parse_args()

if args.dirs[0] == args.dirs[1]:
  parser.error("The source and destination directory paths must be different")

try:
  with tempfile.TemporaryFile(dir=args.dirs[1]):
    pass
except(OSError, PermissionError):
  parser.error("The destionation directory is not writable")
