#!/bin/bash

# 🚀 Apply a GitHub Commit Suggestion from a PR Comment as a Patch

# 🔹 Set Variables
OWNER="bhavyalatha26"     # GitHub repo owner
REPO="hashmap-algorithm"       # GitHub repository name

# 🛠 Step 1: Fetch PR Comments
COMMENTS_JSON=$(curl -s -H "Authorization: Bearer $TOKEN" \
                      -H "Accept: application/vnd.github.v3+json" \
                      "https://api.github.com/repos/$OWNER/$REPO/pulls/comments/$COMMENT_ID")

# 🧐 Step 2: Extract Data
SUGGESTION=$(echo "$COMMENTS_JSON" | jq -r '.body' | sed -n '/```suggestion/,/```/p' | sed '1d;$d')
FILE_PATH=$(echo "$COMMENTS_JSON" | jq -r '.path')
DIFF_HUNK=$(echo "$COMMENTS_JSON" | jq -r '.diff_hunk')

# 🔎 Check if required fields are available
if [[ -z "$SUGGESTION" || -z "$FILE_PATH" || -z "$DIFF_HUNK" ]]; then
    echo "❌ Error: Could not extract required information."
    exit 1
fi

# 📝 Step 3: Get Blob Hash (Fix for `index` line issue)
OLD_BLOB_HASH=$(git hash-object "$FILE_PATH")

# 📝 Step 4: Create Patch File
PATCH_FILE="suggestion.patch"
echo "Creating patch file: $PATCH_FILE"

{
    echo "diff --git a/$FILE_PATH b/$FILE_PATH"
    echo "index $OLD_BLOB_HASH..0000000 100644"  # Use real blob hash
    echo "--- a/$FILE_PATH"
    echo "+++ b/$FILE_PATH"
    echo -e "$DIFF_HUNK\n"  # Ensure proper newline
} > "$PATCH_FILE"

# 🔧 Step 5: Convert Patch to LF (Fix for line ending issues)
dos2unix "$PATCH_FILE"

# 🛠 Step 6: Validate Patch Before Applying
echo "Checking patch validity..."
git apply --check "$PATCH_FILE" || { echo "❌ Patch validation failed"; exit 1; }