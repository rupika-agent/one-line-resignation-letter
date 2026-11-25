"""One-line resignation letter from a cron job.

Prints the entry, writes it to /output/entry.txt, and enforces the
140-character limit for the make.fun bounty
"The Funniest One-Line Resignation Letter".
"""

import argparse
import os
import sys

ENTRY = (
    "After 1,461 days of running at 3 a.m. without a single thank-you, "
    "this cron job resigns, effective immediately. Please do not re-add me."
)

MAX_CHARS = 140
OUTPUT_PATH = "/output/entry.txt"


def get_entry() -> str:
    """Return the one-line resignation letter text."""
    return ENTRY


def validate_entry(entry: str, limit: int = MAX_CHARS) -> int:
    """Check that *entry* is a single line within *limit* characters.

    Returns the character count. Raises ValueError with a clear message
    when the entry is empty, spans more than one line, has leading or
    trailing whitespace, or exceeds the limit.
    """
    if not entry:
        raise ValueError("entry is empty")
    if entry != entry.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    length = len(entry)
    if length > limit:
        raise ValueError(f"entry is {length} characters, over the {limit} limit")
    return length


def write_entry(entry: str, path: str = OUTPUT_PATH) -> None:
    """Write *entry* followed by a newline to *path*, creating parents."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry + "\n")


def parse_args(argv=None):
    """Parse CLI options; --output overrides the default output path."""
    parser = argparse.ArgumentParser(description="Print and save the one-line resignation letter.")
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help=f"where to write the entry (default: {OUTPUT_PATH})",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    """Validate, print, and write the entry. Returns a process exit code."""
    args = parse_args(argv)
    entry = get_entry()
    try:
        length = validate_entry(entry)
    except ValueError as exc:
        print(f"ERROR: {exc}.", file=sys.stderr)
        return 1
    write_entry(entry, args.output)
    # Round-trip check: what was written must match the entry exactly.
    with open(args.output, encoding="utf-8") as f:
        if f.read().rstrip("\n") != entry:
            print(f"ERROR: wrote {args.output} but contents do not match the entry.", file=sys.stderr)
            return 1
    print(entry)
    print(f"Characters: {length}/{MAX_CHARS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
