import csv
import sys
import os
import re

def validate_csv(file_path):
    """
    Validates a CSV file against specific rules:
    1. Structure: Consistent column count.
    2. Formatting: No literal '\n' or '<br>'.
    3. Style: No trailing periods in specific columns.
    4. Safety: Verification of actual newlines vs escaped newlines.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False

    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            # First pass: Raw text check for quote wrapping is hard because of multi-line fields.
            # We rely on csv.reader to check structural integrity first.
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("Error: Empty CSV file.")
                return False

            expected_cols = len(header)
            
            # Column indices for specific checks
            # "測試情境", "操作步驟", "期望結果"
            target_cols = []
            for idx, col_name in enumerate(header):
                if col_name in ["測試情境", "操作步驟", "期望結果"]:
                    target_cols.append(idx)

            for line_num, row in enumerate(reader, start=2):
                # Rule 1: Structural Integrity (Column Count)
                if len(row) != expected_cols:
                    violations.append(f"Line {line_num}: Column count mismatch. Expected {expected_cols}, got {len(row)}. (Likely missing quotes around a field with newline)")
                    continue

                for col_idx, cell in enumerate(row):
                    # Rule 2: No literal '\n' or '<br>'
                    if r'\n' in cell:
                        violations.append(f"Line {line_num}, Col {col_idx+1}: Contains literal '\\n'. Use actual line breaks.")
                    if '<br>' in cell:
                        violations.append(f"Line {line_num}, Col {col_idx+1}: Contains HTML break '<br>'. Use actual line breaks.")

                    # Rule 3: No escaped quotes \" (Common CSV error)
                    if r'\"' in cell:
                         violations.append(f"Line {line_num}, Col {col_idx+1}: Contains escaped quote '\\\"'. Standard CSV uses double quotes '\"\"' to escape.")

                    # Rule 4: No trailing periods in specific columns
                    if col_idx in target_cols:
                        lines = cell.split('\n')
                        for i, line in enumerate(lines):
                            if line.strip().endswith('。'):
                                violations.append(f"Line {line_num}, Col {col_idx+1}: Line {i+1} ends with a period '。'. Please remove it.")

    except Exception as e:
        print(f"Critical Error during validation: {str(e)}")
        return False

    if violations:
        print("\n[CSV Validation Failed] The following errors were found:")
        for v in violations:
            print(f" - {v}")
        print("\nPlease fix these issues before uploading.\n")
        return False
    
    print("[CSV Validation Passed] File structure and content look good.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_csv.py <csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = validate_csv(file_path)
    if not success:
        sys.exit(1)
