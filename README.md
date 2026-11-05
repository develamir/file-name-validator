# File Name Validator

A command-line tool that validates file names against standard pattern templates using regular expressions.

## Features

- Validate individual filenames against a regex pattern
- List all valid files in a directory matching a pattern
- Format results for easy reading
- Works offline with no external dependencies

## Usage

```bash
python main.py <directory> <pattern>
```

### Examples

Validate all text files in the current directory:

```bash
python main.py . '^.*\\.txt$'
```

Validate date-stamped files:

```bash
python main.py . '^\\d{4}-\\d{2}-\\d{2}\\.txt$'
```

## Pattern Syntax

Use standard Python regex syntax. Common patterns include:

| Pattern | Description |
|---------|-------------|
| `^.*\\.txt$` | Any text file |
| `^\\d{4}-\\d{2}-\\d{2}$` | Date-only filename |
| `^\\d{4}-\\d{2}-\\d{2}_.*$` | Date-prefixed filename |

## Testing

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

## Requirements

- Python 3.6+
- Standard library only

## License

MIT
