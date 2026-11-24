"""Write one line of weather forecast for a city that does not exist.

The program writes a single forecast line (140 characters or fewer) for
the invented city of Snozzleford to /output/entry.txt (or to the directory
named by MAKEFUN_OUTPUT_DIR when that variable is set and non-blank).
The line is written with no trailing newline and verified byte-identical
after the write.
"""

import os
import sys

LINE = (
    "In Snozzleford, light drizzle, a 40% chance your umbrella gives up, "
    "and a rainbow arriving five minutes late, like us all."
)

MAX_CHARS = 140


def output_path():
    """Return the path of the entry file to write."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if output_dir and output_dir.strip():
        return os.path.join(output_dir.strip(), "entry.txt")
    return "/output/entry.txt"


def main():
    """Validate the line, write it, and verify the written bytes."""
    line = LINE
    if not line or line.strip() == "":
        print("error: forecast line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: forecast line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if line != line.strip():
        print("error: forecast line must not start or end with whitespace",
              file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: forecast line must not contain a newline", file=sys.stderr)
        return 1

    path = output_path()
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)
        with open(path, "rb") as handle:
            written = handle.read()
        if written != line.encode("utf-8"):
            print("error: written entry does not match the forecast line",
                  file=sys.stderr)
            return 1
    except OSError as exc:
        print("error: could not write entry file: %s" % exc, file=sys.stderr)
        return 1

    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
