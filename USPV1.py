import xml.etree.ElementTree as ET
import os
import re
from collections import defaultdict

def find_sql_in_xml(folder_path):
    """
    Find SQL or stored procedure references in XML files in the specified folder path.
    
    Args:
        folder_path (str): The path to the folder containing XML files.

    Returns:
        tuple: A set of all SQL-related content and a dictionary of content by file.
    """
    sql_in_files = defaultdict(set)

    # Define a basic regex to capture potential SQL-like content
    # Look for SQL queries that might mention stored procedure names
    sql_regex = r'\b(?:EXEC|SP_)\s*(?:\[[^\]]+\]\.)?\[([^\]]+)\]'

    # Step 1: Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Step 2: Process only XML files (check the file extension)
        if filename.endswith('.xml'):
            # Construct the full path to the XML file
            file_path = os.path.join(folder_path, filename)
            try:
                # Step 3: Parse the XML file and get the root element
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Step 4: Iterate through each element in the XML to search for SQL content
                for element in root.iter():
                    # Extract the text from the XML element
                    text = element.text
                    if text:
                        # Debugging: Print the raw text to understand its structure
                        print(f"Checking text from {filename}: {text[:100]}...")  # Print first 100 chars for brevity

                        # Step 5: Use regex to find stored procedure calls (EXEC statements)
                        procs = re.findall(sql_regex, text, re.IGNORECASE)
                        
                        # Debugging: Print the matched procedures
                        if procs:
                            print(f"Found SQL: {procs}")
                        
                        # Add matched SQL-like content to the dictionary
                        for proc in procs:
                            sql_in_files[filename].add(proc)

            except ET.ParseError as e:
                # Handle XML parsing errors
                print(f"Error parsing {file_path}: {e}")
            except Exception as e:
                # Handle any unexpected errors during processing
                print(f"Unexpected error processing {file_path}: {e}")

    # Step 6: Combine all SQL-related content found in the folder
    all_sql = set()
    for sql in sql_in_files.values():
        all_sql.update(sql)

    # Return the aggregated list of SQL content and the content found by file
    return all_sql, sql_in_files

# Main function to execute the script
if __name__ == "__main__":
    # Set the input folder path (modify as needed)
    folder_path = r"C:\Users\dilip.srinivasan\Downloads\SRC_Output"

    # Find SQL or stored procedure content in the XML files within the folder
    all_sql, sql_by_file = find_sql_in_xml(folder_path)

    # Print the results
    print("All SQL/Stored Procedure References:")
    print(all_sql)
    print("\nSQL by File:")
    for file, sql in sql_by_file.items():
        print(f"{file}: {sql}")
