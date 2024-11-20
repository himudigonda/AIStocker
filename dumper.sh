#!/bin/bash

# Function to print file content with relative path
print_file_content() {
    local file_path=$1
    echo "$file_path"
    cat "$file_path"
    echo "-----"
}

# Iterate over all files in the workspace
find . -type f ! -path "./.git/*" ! -name "dumper.sh" | while read -r file; do
    print_file_content "$file"
done
