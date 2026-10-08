"""Log Parsing Helper.

Usage:
    python log_parser.py [-i INPUT] [-o OUTPUT]
"""

import argparse
import json
import re
import sys
from pathlib import Path

LOG_RE = re.compile(r'^\[(?P<ts>.*?)\]\s+(?P<lvl>\w+):\s+(?P<msg>.*)$')


def parse_line(line: str):
    """Parse a log line into a dict or return None if it doesn't match."""
    m = LOG_RE.match(line.rstrip())
    return m.groupdict() if m else None


def main():
    parser = argparse.ArgumentParser(description="Parse logs into JSON.")
    parser.add_argument("-i", "--input", type=Path, help="Input file (default: stdin)")
    parser.add_argument("-o", "--output", type=Path, help="Output file (default: stdout)")
    args = parser.parse_args()

    infile = args.input.open() if args.input else sys.stdin
    outfile = args.output.open("w") if args.output else sys.stdout

    for line in infile:
        parsed = parse_line(line)
        if parsed:
            json.dump(parsed, outfile)
            outfile.write("\n")
    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()