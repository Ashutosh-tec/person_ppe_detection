import os
import xml.etree.ElementTree as ET

def convert_to_yolo(size:list, box:list)-> tuple:
    """
    convert coordinate to YOLO format
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def parse_xml(xml_file: str)-> list:
    """
    take annotations from xml_file and convert it to list fromats
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    boxes = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        class_id = class_dict.get(name)
        
        if class_id is not None:
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            
            bb = convert_to_yolo((w, h), (xmin, xmax, ymin, ymax))
            boxes.append((class_id, bb))
        
    return boxes

def save_to_yolo(boxes, output_file):
    with open(output_file, 'w') as f:
        for box in boxes:
            class_id, bb = box
            f.write(f"{class_id} {' '.join(map(str, bb))}\n")

# Updated class dictionary with more classes
class_dict = {
    # "person": 0,
    "hard-hat": 0,
    "gloves": 1,
    "mask": 2,
    "glasses": 3,
    "boots": 4,
    "vest": 5,
    "ppe-suit": 6,
    "ear-protector": 7,
    "safety-harness": 8
}

# # Path to the XML annotation file
# xml_file = "/mnt/d/Codes/ppe_yolov8/datasets/labels/-184-_png_jpg.rf.b02963998a79b9ad5079f57b65130bc2.xml"
# # Output file for YOLO formatted annotations
# output_file = "annotation.txt"
# # Parse the XML and convert to YOLO format
# boxes = parse_xml(xml_file)
# # Save the YOLO formatted annotations to a file
# save_to_yolo(boxes, output_file)
# print(f"YOLO formatted annotations saved to {output_file}")

def change_extension(filename:str, new_extension:str)->str:
    """
    Change the previous extension to new.
    """
    # Split the filename into the base and the extension
    base = os.path.splitext(filename)[0]
    # Create the new filename with the new extension
    new_filename = f"{base}.{new_extension}"
    return new_filename

def change_to_yolo(input_dir: str, output_dir: str) -> None:
    """
    Convert XML to YOLO annotation, from directory 
    """
    os.makedirs(output_dir) if not os.path.exists(output_dir) else None
        
    for file in os.listdir(input_dir):
        xml_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, change_extension(file, "txt"))
        boxes = parse_xml(xml_file)
        save_to_yolo(boxes, output_file)
        print("Done processing: ", file)
        
change_to_yolo(input_dir="/mnt/d/Codes/ppe_yolov8/datasets/labels", output_dir="/mnt/d/Codes/ppe_yolov8/datasets/labels_yolo_ppe")
