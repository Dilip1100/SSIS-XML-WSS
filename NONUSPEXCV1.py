import xml.etree.ElementTree as ET
import os

def extract_product_info_from_xml(folder_path):
    """
    Extract product or promotion information from XML files in the specified folder path.

    Args:
        folder_path (str): The path to the folder containing XML files.

    Returns:
        dict: A dictionary of extracted information, keyed by file name.
    """
    data_by_file = {}

    # Step 1: Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Process only XML files (check the file extension)
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Step 2: Parse the XML file and get the root element
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Step 3: Extract relevant data (product, promotion, etc.)
                file_data = []
                for element in root.iter():
                    if element.tag == 'product':  # Example: looking for <product> tags
                        file_data.append({'name': element.find('name').text,
                                          'description': element.find('description').text,
                                          'price': element.find('price').text})
                    elif element.tag == 'promotion':  # Example: looking for <promotion> tags
                        file_data.append({'promotion_name': element.find('promotion_name').text,
                                          'start_date': element.find('start_date').text,
                                          'end_date': element.find('end_date').text})

                # Store the extracted data by file
                data_by_file[filename] = file_data

            except ET.ParseError as e:
                print(f"Error parsing {file_path}: {e}")
            except Exception as e:
                print(f"Unexpected error processing {file_path}: {e}")

    return data_by_file

# Main function to execute the script
if __name__ == "__main__":
    # Set the input folder path (modify as needed)
    folder_path = r"C:\Users\dilip.srinivasan\Downloads\SRC_Output"

    # Extract product and promotion information from the XML files within the folder
    extracted_data = extract_product_info_from_xml(folder_path)

    # Print the results
    print("Extracted Information:")
    for file, data in extracted_data.items():
        print(f"{file}: {data}")
