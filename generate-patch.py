import re
import sys

import requests

repo_full_name = "bhavyalatha26/hashmap-algorithm"
patch_file = "suggestion.patch"
comment_id = "2016754812"
git_token = "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"

# Fetch the comment details from github pr
response = requests.get(f"https://api.github.com/repos/{repo_full_name}/pulls/comments/{comment_id}", headers={
    "Authorization": f"Bearer {git_token}",
    "Accept": "application/vnd.github.v3+json"
})
comment_json = response.json()

# Extract the suggested code changes from commit suggestion (comment)
suggestion: str = comment_json.get("body", "")
suggested_lines: list[str] = []
pattern = r"```suggestion\r?\n(.*?)\r?\n?```"
match = re.search(pattern, suggestion, re.DOTALL)
if match:
    suggested_lines = str(match.group(1)).split("\n")
else:
    print("No suggestion block found.")
    sys.exit(0)

# Extract the change start line
line = comment_json.get("line", "")
# Extract the change file path
file_path = comment_json.get('path', '')

# Load the actual code in the file path (before changes)
with open(file_path, "r") as f:
    existing_file_content = [line.rstrip('\n') for line in f.readlines()]
    f.close()

# Collect the code diff from the suggested code changes
code_diff = []

# Prepend the previous 3 lines of code
prev_lines = existing_file_content[line-4:line-1]
prev_lines = list(map(lambda x:" " + x, prev_lines))
code_diff.extend(prev_lines)

# Add code diff to remove the start line
remove_line = "-" + existing_file_content[line - 1]  # get code at this line
code_diff.append(remove_line)

# Add code diff to add the new suggested lines of code
add_lines = list(map(lambda x:("+" + x).rstrip(), suggested_lines))
code_diff.extend(add_lines)

# Append the next 3 lines of code
next_lines = existing_file_content[line:line+3]
next_lines = list(map(lambda x:" " + x, next_lines))
code_diff.extend(next_lines)

# Prepare the line diff (@@ -x,y +x,z @@)
changed_lines_count = len(prev_lines) + len(next_lines)
line_diff = f"@@ -{line-len(prev_lines)},{changed_lines_count + 1} +{line-len(prev_lines)},{changed_lines_count + len(suggested_lines)} @@"

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
