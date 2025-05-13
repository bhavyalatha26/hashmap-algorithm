import argparse
import base64
import json
import os
from itertools import groupby
from operator import itemgetter

PATCH_FOLDER = os.getcwd() + "/patches"


def generate_patch_file_name(path_to_file: str) -> str:
    return path_to_file.replace('/', '_').replace('.', '_')


def generate_patch_file(suggestion: str, line: int, file_path: str, append: bool = False) -> str:
    """
    Generates the patch file based on the code suggestions provided
    :param suggestion: The actual code suggestion
    :param line: Start line of the change
    :param file_path: The path to which these changes need to be applied
    :param append: Determines whether the content need to written or appended to the file
    :return: Path of the patch file
    """
    suggested_lines = suggestion.split("\n")
    suggested_lines = list(map(lambda x: str(x).strip("\r"), suggested_lines))

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
    if append:
        patch = "\n".join([line_diff, code_diff])
    else:
        patch = "\n".join([f"--- a/{file_path}", f"+++ b/{file_path}", line_diff, code_diff])

    # Save the patch file
    patch_file = f"{PATCH_FOLDER}/{generate_patch_file_name(path_to_file=file_path)}.patch"
    with open(patch_file, "a") as f:
        f.write(patch)
        f.write("\n")
        f.close()

    return patch_file


def main():
    """This is the main function of the script."""

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="A git patch generator script to generate patch files for given github code suggestion comments")

    # Add named arguments (options)
    parser.add_argument("-c", "--comments", type=str, help="Base 64 encoded list of github comments")

    # Parse the arguments
    args = parser.parse_args()

    # Decode the received commit suggestions (list of dict)
    decoded_bytes = base64.b64decode(args.comments.encode('utf-8'))
    decoded_comments = json.loads(decoded_bytes.decode('utf-8'))

    # Group the suggestions by the file names
    grouped_data = {}
    for key, group in groupby(decoded_comments, key=itemgetter('path')):
        grouped_data[key] = list(group)

    # Create the patch parent folder (all patch files will be saved to this)
    os.makedirs(PATCH_FOLDER, exist_ok=True)

    # For each file and the list of commit suggestions for it
    for path, comments in grouped_data.items():
        # Sort the suggestion by line number first
        sorted_comments = sorted(comments, key=itemgetter('line'))
        print(f"Generating patch for file - {path}")
        # Generate the patch file for all suggestions of that file
        append = False
        for comment in sorted_comments:
            patch_file_path = generate_patch_file(
                suggestion=comment.get("body", ""), line=int(comment.get("line", "0")), file_path=path,
                append=append
            )
            append = True
            print(f"Code diff {'appended' if append else 'added'} to patch file - {patch_file_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise Exception(f"Error while generating patch scripts : \n{e}")
