#!/bin/bash

# Script to Apply a Commit Suggestion from a GitHub PR Comment as a Patch

# Step 1: Fetch PR comments using GitHub API
COMMENTS_JSON=$(curl -s -H "Authorization: Bearer $TOKEN" \
                      -H "Accept: application/vnd.github.v3+json" \
                      "https://api.github.com/repos/$REPO/pulls/$PR_NUMBER/comments")

# Step 2: Extract Data (Modify grep patterns for specific comment filtering)
COMMENT_ID=$(echo "$COMMENTS_JSON" | jq -r '.[0].id') # Get first comment ID
SUGGESTION=$(echo "$COMMENTS_JSON" | jq -r '.[0].body' | sed -n '/```suggestion/,/```/p' | sed '1d;$d') # Extract suggestion
FILE_PATH=$(echo "$COMMENTS_JSON" | jq -r '.[0].path')  # Extract file path
LINE_NUMBER=$(echo "$COMMENTS_JSON" | jq -r '.[0].position') # Extract line number
OLD_COMMIT_ID=$(echo "$COMMENTS_JSON" | jq -r '.[0].original_commit_id') # Old commit ID
NEW_COMMIT_ID=$(echo "$COMMENTS_JSON" | jq -r '.[0].commit_id') # New commit ID
DIFF_HUNK=$(echo "$COMMENTS_JSON" | jq -r '.[0].diff_hunk') # Extract Git diff hunk

# 🔎 Check if required fields are available
if [[ -z "$SUGGESTION" || -z "$FILE_PATH" || -z "$LINE_NUMBER" ]]; then
    echo "Error: Could not extract required information."
    exit 1
fi

# Step 3: Create Patch File
PATCH_FILE="suggestion.patch"
echo "Creating patch file: $PATCH_FILE"

cat <<EOF > $PATCH_FILE
diff --git a/$FILE_PATH b/$FILE_PATH
index $OLD_COMMIT_ID..$NEW_COMMIT_ID 100644
--- a/$FILE_PATH
+++ b/$FILE_PATH
@@ -$LINE_NUMBER,1 +$LINE_NUMBER,1 @@
$DIFF_HUNK
EOF

# Step 4: Apply Patch
echo "Applying patch..."
git apply $PATCH_FILE

# Step 5: Commit Changes
echo "Verifying applied changes..."
git diff

echo "Committing the applied suggestion..."
git add "$FILE_PATH"
git commit -m "Applied GitHub commit suggestion from PR #$PR_NUMBER"

echo "Patch applied and committed successfully!"
