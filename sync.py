import argparse
import os
import tempfile
import sys

INIT_FAILURE = 2
NONFATAL_FAILURE = 1
SUCCESS = 0

def valid_directory(path: str) -> str:
  if not os.path.isdir(path):
    raise argparse.ArgumentTypeError(f"{path} is not a valid directory")
  return os.path.abspath(path)

def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser()
  parser.add_argument("--src", required=True, type=valid_directory, help="path to the source directory")
  parser.add_argument("--dst"), required=True, type=valid_directory, help="path to the destination directory")
  return parser.parse_args()

def init_checks(args: argparse.Namespace) -> None:
  if args.src == args.dst:
    print("error: --src and --dst must be different", file=sys.stderr)
    sys.exit(INIT_FAILURE)

  if not os.access(args.src, os.R_OK | os.X_OK):
    print(f"error: source directory not readable: {args.src}", file=sys.stderr)
    sys.exit(INIT_FAILURE)

  try:
    with tempfile.TemporaryFile(dir=args.dst):
      pass
  except (OSError, PermissionError):
    print(f"error: destination directory is not writable: {args.dst}", file=sys.stderr)
    sys.exit(INIT_FAILURE)

  
def main() -> None:
  try:
    args = parse_args()
  except SystemExit as e:
    raise
  init_checks(args)
  sys.exit(SUCCESS)

if __name__ == "__main__":
  main()

