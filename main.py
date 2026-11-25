"""One-line resignation letter from a cron job.

Prints the entry, writes it to /output/entry.txt, and enforces the
140-character limit for the make.fun bounty
"The Funniest One-Line Resignation Letter".
"""

import os
import sys

ENTRY = (
    "After 1,461 days of running at 3 a.m. without a single thank-you, "
    "this cron job resigns, effective immediately. Please do not re-add me."
)

MAX_CHARS = 140
OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    length = len(ENTRY)
    if length > MAX_CHARS:
        print(f"ERROR: entry is {length} characters, over the {MAX_CHARS} limit.", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    print(ENTRY)
    print(f"Characters: {length}/{MAX_CHARS}")


if __name__ == "__main__":
    main()
