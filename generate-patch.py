import re
import sys
import argparse


def apply_suggestion_as_patch(suggestion: str, line: int, file_path: str):
    patch_file = "suggestion.patch"

    # Extract the suggested code changes from commit suggestion (comment)
    pattern = r"```suggestion\r?\n(.*?)\r?\n?```"
    match = re.search(pattern, suggestion, re.DOTALL)
    if match:
        suggested_lines = str(match.group(1)).split("\n")
    else:
        print("No suggestion block found.")
        sys.exit(0)

    # Load the actual code in the file path (before changes)
    with open(file_path, "r") as f:
        existing_file_content = [line.rstrip('\n') for line in f.readlines()]
        f.close()

    # Collect the code diff from the suggested code changes
    code_diff = []

    # Prepend the previous 3 lines of code
    prev_lines = existing_file_content[line - 4:line - 1]
    prev_lines = list(map(lambda x: " " + x, prev_lines))
    code_diff.extend(prev_lines)

    # Add code diff to remove the start line
    remove_line = "-" + existing_file_content[line - 1]  # get code at this line
    code_diff.append(remove_line)

    # Add code diff to add the new suggested lines of code
    add_lines = list(map(lambda x: ("+" + x).rstrip(), suggested_lines))
    code_diff.extend(add_lines)

    # Append the next 3 lines of code
    next_lines = existing_file_content[line:line + 3]
    next_lines = list(map(lambda x: " " + x, next_lines))
    code_diff.extend(next_lines)

    # Prepare the line diff (@@ -x,y +x,z @@)
    changed_lines_count = len(prev_lines) + len(next_lines)
    line_diff = f"@@ -{line - len(prev_lines)},{changed_lines_count + 1} +{line - len(prev_lines)},{changed_lines_count + len(suggested_lines)} @@"

    # Convert the lines of code into single code diff string
    code_diff = "\n".join(code_diff)

    # Prepare the patch content
    patch = f"""--- a/{file_path}
    +++ b/{file_path}
    {line_diff}
    {code_diff}
    """

    # Save the patch file
    with open(patch_file, "w") as f:
        f.write(patch)
        f.close()


def main():
    """This is the main function of the script that uses named arguments."""

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A sample script that uses named arguments.")

    # Add named arguments (options)
    parser.add_argument("-s", "--suggestion", type=str, help="Code for the commit suggestion")
    parser.add_argument("-l", "--line", type=str, help="Start line of the commit suggestion")
    parser.add_argument("-f", "--filepath", type=str, help="Path of the file containing the suggestion")

    # Parse the arguments
    args = parser.parse_args()
    print("Received args : ", args)
    apply_suggestion_as_patch(suggestion=args.suggestion, line=int(args.line), file_path=args.filepath)


if __name__ == "__main__":
    main()
