import os
import re

def replace_space_with_hyphen(line):
    """Function to replace spaces with underscores in a string between two hashes

    Args:
        line (str): string to be processed

    Returns:
        str: processed string
    """
    pattern = r'(?<=##)[a-zA-Z ]+(?=[^#]*##)'
    return re.sub(pattern, lambda match: match.group().replace(' ', '-'), line)

def add_missing_space(line):
    """Function to add a space after a hash if it is missing

    Args:
        line (str): string to be processed

    Returns:
        str: processed string
    """
    pattern = r"##(?!\s)-"
    line = re.sub(pattern, "## -", line)
    return line

async def clean_file(file_path):
    """Function to clean a file in-place

    Args:
        file_path (str): path to the file to be cleaned
    """
    temp_file_path = file_path + ".tmp"

    with open(file_path, 'r') as original_file, open(temp_file_path, 'w') as temp_file:
        for line in original_file:
            line = replace_space_with_hyphen(line)
            line = add_missing_space(line)
            temp_file.write(line)

    # Replace the original file with the modified file
    os.replace(temp_file_path, file_path)
