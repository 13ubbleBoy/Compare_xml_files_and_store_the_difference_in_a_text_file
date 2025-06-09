import xml.etree.ElementTree as ET
import os
from datetime import datetime

def compare_elements(elem1, elem2, path=""):
    diffs = []
    current_path = f"{path}/{elem1.tag}" if path else elem1.tag

    # 1. Tag mismatch (log and continue)
    if elem1.tag != elem2.tag:
        diffs.append(f"Tag mismatch at {current_path}: '{elem1.tag}' != '{elem2.tag}'")

    # 2. Text content mismatch
    text1 = (elem1.text or '').strip()
    text2 = (elem2.text or '').strip()
    if text1 != text2:
        diffs.append(f"Text mismatch at {current_path}: '{text1}' != '{text2}'")

    # 3. Attribute comparison
    attribs1 = elem1.attrib
    attribs2 = elem2.attrib

    keys1 = set(attribs1.keys())
    keys2 = set(attribs2.keys())

    # Extra attributes in file1
    for key in keys1 - keys2:
        diffs.append(f"Extra attribute in file1 at {current_path}: '{key}' = '{attribs1[key]}'")

    # Extra attributes in file2
    for key in keys2 - keys1:
        diffs.append(f"Extra attribute in file2 at {current_path}: '{key}' = '{attribs2[key]}'")

    # Attributes present in both - check value mismatch
    for key in keys1 & keys2:
        if attribs1[key] != attribs2[key]:
            diffs.append(
                f"Attribute value mismatch at {current_path} for '{key}': '{attribs1[key]}' != '{attribs2[key]}'"
            )

    # 4. Child elements comparison
    children1 = list(elem1)
    children2 = list(elem2)

    if len(children1) != len(children2):
        diffs.append(f"Children count mismatch at {current_path}: {len(children1)} != {len(children2)}")

    for i, (child1, child2) in enumerate(zip(children1, children2)):
        child_path = f"{current_path}[{i}]"
        diffs.extend(compare_elements(child1, child2, child_path))

    # If one has more children than the other
    if len(children1) > len(children2):
        for extra in children1[len(children2):]:
            diffs.append(f"Extra child in file1 at {current_path}: <{extra.tag}>")
    elif len(children2) > len(children1):
        for extra in children2[len(children1):]:
            diffs.append(f"Extra child in file2 at {current_path}: <{extra.tag}>")

    return diffs

def compare_xml_files(file1, file2, output_file):
    output_lines = []
    try:
        tree1 = ET.parse(file1)
        tree2 = ET.parse(file2)
        root1 = tree1.getroot()
        root2 = tree2.getroot()

        differences = compare_elements(root1, root2)

        output_lines.append(f"Comparison Report: {datetime.now()}")
        output_lines.append(f"File 1: {file1}")
        output_lines.append(f"File 2: {file2}\n")

        if differences:
            output_lines.append("Differences found:")
            for diff in differences:
                print("🔸", diff)
                output_lines.append(f"🔸 {diff}")
        else:
            print(f"✅ Files '{os.path.basename(file1)}' are identical.")
            output_lines.append("✅ The XML files are identical.")

    except ET.ParseError as e:
        error_message = f"❌ XML Parse Error: {e}"
        print(error_message)
        output_lines.append(error_message)

    except FileNotFoundError as e:
        error_message = f"❌ File Not Found: {e}"
        print(error_message)
        output_lines.append(error_message)

    except Exception as e:
        error_message = f"❌ Unexpected Error: {e}"
        print(error_message)
        output_lines.append(error_message)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"📄 Saved result to: {output_file}\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input1_dir = os.path.join(script_dir, "Input1")
    input2_dir = os.path.join(script_dir, "Input2")

    # Timestamped results directory including seconds
    timestamp = datetime.now().strftime("Results_%d-%m-%Y_%H-%M-%S")
    result_dir = os.path.join(script_dir, timestamp)
    os.makedirs(result_dir, exist_ok=True)

    # Get common filenames
    files1 = {f for f in os.listdir(input1_dir) if f.endswith(".xml")}
    files2 = {f for f in os.listdir(input2_dir) if f.endswith(".xml")}
    common_files = files1.intersection(files2)

    if not common_files:
        print("⚠️ No matching XML filenames found in both Input1 and Input2.")
        return

    for filename in sorted(common_files):
        file1 = os.path.join(input1_dir, filename)
        file2 = os.path.join(input2_dir, filename)
        output_file = os.path.join(result_dir, f"{os.path.splitext(filename)[0]}.txt")

        print(f"\n🔍 Comparing: {filename}")
        compare_xml_files(file1, file2, output_file)



if __name__ == "__main__":
    main()
