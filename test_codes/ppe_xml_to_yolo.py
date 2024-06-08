import re
import os
from PIL import Image
import xml.etree.ElementTree as ET

from annotate_from_xml import draw_boxes

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def crop_image(image_path, output_path, xmin, xmax, ymin, ymax):
    # Open an image file
    with Image.open(image_path) as img:
        # Crop the image using the bounding box
        cropped_img = img.crop((xmin, ymin, xmax, ymax))
        # Save the cropped image
        cropped_img.save(output_path)
        print(f"Cropped image saved to {output_path}")


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

def replace_str(text, new_folder):
    # Define the regex pattern to match '/images/'
    pattern = r'/labels'
    # Replace all occurrences of the pattern with '/labels/'
    replaced_text = re.sub(pattern, f'/{new_folder}', text)
    return replaced_text

def parse_xml(xml_file: str)-> tuple:
    """
    take annotations from xml_file and convert it to list fromats
    """
    person_lst, ppe_lst = list(), list()
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    boxes = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        class_id = class_dict.get(name)
        
        if class_id == 777: #person
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            
            person_lst.append((class_id, (w, h), (xmin, xmax, ymin, ymax)))
        elif class_id is not None:
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            
            ppe_lst.append((class_id, (w, h), (xmin, xmax, ymin, ymax)))
        else:
            print("None class")
        
    return person_lst, ppe_lst

def save_to_yolo(boxes, output_file):
    with open(output_file, 'w') as f:
        for box in boxes:
            class_id, bb = box
            f.write(f"{class_id} {' '.join(map(str, bb))}\n")

# Updated class dictionary with more classes
class_dict = {
    "person": 777,
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

def change_extension(filename:str, new_extension:str, additional_desc: str="")->str:
    """
    Change the previous extension to new.
    """
    # Split the filename into the base and the extension
    base = os.path.splitext(filename)[0]
    # Create the new filename with the new extension
    new_filename = f"{base+additional_desc}.{new_extension}"
    return new_filename

def change_to_yolo(input_dir: str, output_dir: str, person_image_folder:str) -> None:
    """
    Convert XML to YOLO annotation, from directory 
    """
    os.makedirs(output_dir) if not os.path.exists(output_dir) else None
        
    for file in os.listdir(input_dir):
        xml_file = os.path.join(input_dir, file)
        image_file = os.path.join(replace_str(input_dir, new_folder="images"), change_extension(file, new_extension="jpg"))
        person_lst, ppe_lst = parse_xml(xml_file)

        for idx in range(len(person_lst)):
            _, _, (xmin, xmax, ymin, ymax) = person_lst[idx]

            # create cropped person image dir, if not exist
            create_directory(replace_str(input_dir, new_folder=person_image_folder))
            ppe_image_file = os.path.join(replace_str(input_dir, new_folder=person_image_folder), change_extension(file, new_extension="jpg", additional_desc=f"_person_{idx}"))
            crop_image(image_path=image_file, output_path=ppe_image_file, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

            temp_ppe = list()
            for elem2 in ppe_lst:
                class_id_ppe, size_ppe, (xmin_ppe, xmax_ppe, ymin_ppe, ymax_ppe) = elem2
                if xmin <= xmin_ppe and ymin <= ymin_ppe \
                    and xmax >= xmax_ppe and ymax >= ymax_ppe:
                    # temp_ppe.append(elem2)
                    bb = convert_to_yolo(size_ppe, (xmin_ppe-xmin, xmax_ppe-xmin, ymin_ppe-ymin, ymax_ppe-ymin))
                    temp_ppe.append((class_id_ppe, bb))

            print("ppe coordinates: ", temp_ppe)
            draw_boxes(ppe_image_file, [(class_id_ppe,xmin_ppe-xmin, ymin_ppe-ymin, xmax_ppe-xmin, ymax_ppe-ymin)]).save("annotated_image.jpg")
            
            
            
            output_file = os.path.join(output_dir, change_extension(file, "txt", f"_person_{idx}"))
            save_to_yolo(temp_ppe, output_file)
        
        print("Done processing: ", file)
        break
        
change_to_yolo(input_dir="/mnt/d/Codes/ppe_yolov8/datasets/labels", output_dir="/mnt/d/Codes/ppe_yolov8/datasets/labels_yolo_ppe", person_image_folder = "images_ppe")
