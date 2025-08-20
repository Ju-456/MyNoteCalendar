#!/bin/bash

SPEC_FILE="buildozer.spec"
SOURCE_DIR=$(grep "^source.dir" "$SPEC_FILE" | grep -v "#" | awk -F= '{print $2}' | tr -d ' ' | tr -d '"')
[ -z "$SOURCE_DIR" ] && SOURCE_DIR="."  # If not defined, use the current directory

ERROR=0

echo "Checking referenced files in $SPEC_FILE..."

# Check specific files
FILES=$(grep -E "icon\.filename|presplash\.filename" "$SPEC_FILE" | grep -v "#" | awk -F= '{print $2}' | tr -d ' ' | tr -d '"')

for f in $FILES; do
    f="${f//%(source.dir)s/$(pwd)}"
    if [ -e "$f" ]; then
        echo "File found: $f"
    else
        echo "MISSING file: $f"
        ERROR=1
    fi
done

# Check all .py files in the source directory
echo "Checking .py files in $SOURCE_DIR..."
for pyfile in $(find "$SOURCE_DIR" -name "*.py"); do
    if [ -e "$pyfile" ]; then
        echo "Python file found: $pyfile"
    else
        echo "MISSING Python file: $pyfile"
        ERROR=1
    fi
done

if [ $ERROR -eq 0 ]; then
    echo "All required files are present."
else
    echo "Some files are missing. Please fix them before compiling."
fi