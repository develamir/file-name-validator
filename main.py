#!/usr/bin/env python3
"""File Name Validator - validates filenames against regex patterns."""

import os
import re
import sys


def validate_filename(filename, pattern):
    """Check if a filename matches the given regex pattern.

    Args:
        filename: The filename to check.
        pattern: A regex pattern string.

    Returns:
        True if the filename matches the pattern, False otherwise.
    """
    # If pattern is not a string (e.g., None), treat as non‑matching.
    if not isinstance(pattern, str):
        return False
    return bool(re.fullmatch(pattern, filename))


def list_valid_files(directory, pattern):
    """List all files in a directory whose names match the pattern.

    Args:
        directory: Path to the directory.
        pattern: A regex pattern string.

    Returns:
        List of filenames that match the pattern.
    """
    result = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            if validate_filename(entry, pattern):
                result.append(entry)
    return result


def format_results(results):
    """Format validation results into a readable string.

    Args:
        results: List of (filename, is_valid) tuples.

    Returns:
        Formatted string with each result on its own line.
    """
    lines = []
    for filename, is_valid in results:
        marker = "OK" if is_valid else "INVALID"
        lines.append(f"[{marker}] {filename}")
    return "\n".join(lines)


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 3:
        print("Usage: python main.py <directory> <pattern>")
        print("Example: python main.py . '^\\d{4}-\\d{2}-\\d{2}\\.txt$'")
        sys.exit(1)

    directory = sys.argv[1]
    pattern = sys.argv[2]

    try:
        results = []
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if os.path.isfile(full_path):
                results.append((filename, validate_filename(filename, pattern)))

        print(format_results(results))
        invalid = [r for r in results if not r[1]]
        if invalid:
            print(f"\n{len(invalid)} invalid file(s) found.")
        else:
            print("\nAll files are valid.")
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
