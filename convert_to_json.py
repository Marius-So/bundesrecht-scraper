import glob
import xml.etree.ElementTree as ET
import json
from alive_progress import alive_bar
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))


def get_all_texts():
    return glob.glob(os.path.join(current_dir,'data/*/*.xml'))

# Function to convert XML element to dictionary
def xml_to_dict(element):
    data = {}
    for child in element:
        if child:
            if child.tag in data:
                if isinstance(data[child.tag], list):
                    data[child.tag].append(xml_to_dict(child))
                else:
                    data[child.tag] = [data[child.tag], xml_to_dict(child)]
            else:
                data[child.tag] = xml_to_dict(child)
        else:
            data[child.tag] = child.text
    return data

def convert_xml_to_json(xml_file):
    # Parse XML data from a file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Convert XML to dictionary
    xml_data = xml_to_dict(root)

    # Convert dictionary to JSON
    json_data = json.dumps(xml_data, indent=4, ensure_ascii=False).encode('utf-8')

    # Write JSON data to a file with UTF-8 encoding
    with open(xml_file.replace('xml', 'json'), 'wb') as f:
        f.write(json_data)

def update_all_texts():
    all_xmls = get_all_texts()
    print(all_xmls)
    with alive_bar(len(all_xmls)) as bar:
        for xml in all_xmls:
            convert_xml_to_json(xml)
            bar()

update_all_texts()
