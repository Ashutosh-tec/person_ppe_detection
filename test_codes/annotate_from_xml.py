import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    boxes = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        boxes.append((name, xmin, ymin, xmax, ymax))
    
    return boxes

def draw_boxes(image_path:str, boxes:list):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    print("Given boxes: ", boxes)
    for box in boxes:
        name, xmin, ymin, xmax, ymax = box
        draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=2)
        draw.text((xmin, ymin), str(name), fill="red")
    
    return image

# Path to the XML annotation file
xml_file = "/mnt/d/Codes/ppe_yolov8/datasets/labels/-184-_png_jpg.rf.b02963998a79b9ad5079f57b65130bc2.xml"
# Path to the corresponding image file
image_path = "/mnt/d/Codes/ppe_yolov8/datasets/images/-184-_png_jpg.rf.b02963998a79b9ad5079f57b65130bc2.jpg"

# # Parse the XML to get bounding boxes
# boxes = parse_xml(xml_file)

# # Draw the bounding boxes on the image
# annotated_image = draw_boxes(image_path, boxes)

# # Display the image with bounding boxes
# annotated_image.show()

# # Optionally, save the image with bounding boxes
# annotated_image.save("annotated_image.jpg")
