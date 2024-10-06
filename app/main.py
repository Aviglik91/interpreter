import sys

try:
    from app.tokenizer import Scanner
except ImportError:
    from tokenizer import Scanner


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    try:
        with open(filename) as file:
            file_contents = file.read()
    except IOError as e:
        print(f"Error reading file {filename}: {e}", file=sys.stderr)
        exit(1)
    # Uncomment this block to pass the first stage
    if file_contents:
        scanner = Scanner(file_contents)
        scanner.scanTokens()
        scanner.print()

        exit(scanner.status_code)
    else:
        print(
            "EOF  null"
        )  # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
