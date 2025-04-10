import os
import sys
import glob
import json

def replace_string_in_files(original, replacement):
    """
    Replaces all occurrences of 'original' with 'replacement' in all files
    in the current directory.
    
    Args:
        original (str): The string to be replaced
        replacement (str): The string to replace with
    
    Returns:
        tuple: (files_modified, total_replacements)
    """
    files_modified = 0
    total_replacements = 0
    
    # Get all files in the current directory
    files = glob.glob("*.*")
    
    print(f"Searching for '{original}' to replace with '{replacement}' in {len(files)} files...")
    
    for filename in files:
        try:
            # Skip this script itself
            if filename == os.path.basename(__file__):
                continue
                
            # Check if the file is a Jupyter notebook
            if filename.lower().endswith('.ipynb'):
                # Handle Jupyter notebook as JSON
                with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                    notebook_content = json.load(file)
                
                # Process each cell in the notebook
                replacements_in_notebook = 0
                
                # Function to replace strings in notebook cell content
                def replace_in_cell_content(content):
                    if isinstance(content, str):
                        return content.replace(original, replacement)
                    elif isinstance(content, list):
                        return [replace_in_cell_content(item) for item in content]
                    elif isinstance(content, dict):
                        return {k: replace_in_cell_content(v) for k, v in content.items()}
                    else:
                        return content
                
                # Apply replacements throughout the notebook structure
                modified_notebook = replace_in_cell_content(notebook_content)
                
                # Count replacements by comparing the stringified JSON
                original_json = json.dumps(notebook_content)
                modified_json = json.dumps(modified_notebook)
                occurrences = original_json.count(original)
                
                if occurrences > 0:
                    # Write the modified notebook
                    with open(filename, 'w', encoding='utf-8') as file:
                        json.dump(modified_notebook, file, indent=4)
                    
                    files_modified += 1
                    total_replacements += occurrences
                    print(f"  Modified: {filename} ({occurrences} replacements)")
            
            else:
                # Handle regular text files
                with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                # Count occurrences of the original string
                occurrences = content.count(original)
                
                if occurrences > 0:
                    # Replace the string
                    new_content = content.replace(original, replacement)
                    
                    # Write the modified content back to the file
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    files_modified += 1
                    total_replacements += occurrences
                    print(f"  Modified: {filename} ({occurrences} replacements)")
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
    
    return files_modified, total_replacements

def main():
    print("String Replacement Tool")
    print("======================")
    print("This tool will replace all occurrences of a string with another string")
    print("in all files in the current directory.")
    print()
    
    # Get the original and replacement strings from the user
    original = input("Enter the original string to find: ")
    if not original:
        print("Error: Original string cannot be empty.")
        return
        
    replacement = input("Enter the replacement string: ")
    
    # Confirm before proceeding
    print(f"\nReady to replace all '{original}' with '{replacement}'")
    confirmation = input("Do you want to continue? (y/n): ").lower()
    
    if confirmation != 'y':
        print("Operation cancelled.")
        return
    
    # Perform the replacement
    files_modified, total_replacements = replace_string_in_files(original, replacement)
    
    # Report results
    print("\nReplacement complete!")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")

if __name__ == "__main__":
    main()
