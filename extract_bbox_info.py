from PIL import Image

class_names = ['boneanomaly', 'bonelesion', 'foreignbody', 'fracture', 'metal', 'periostealreaction', 'pronatorsign', 'softtissue', 'text']

# function to convert YOLO format to dictionary
def yolo_to_dict(yolo_file, image_file):
    img = Image.open(image_file)
    width, height = img.size

    # read YOLO file
    with open(yolo_file, 'r') as f:
        lines = f.readlines()

    # create dictionary to store annotations
    annotations = {}
    for class_name in class_names:
        annotations[class_name] = []

    # read annotations from YOLO file
    for line in lines:
        line = line.strip().split()
        if len(line) == 5:
            class_id, x_center, y_center, bbox_width, bbox_height = map(float, line)
            class_name = class_names[int(class_id)]
            x_min = int((x_center - bbox_width/2) * width)
            y_min = int((y_center - bbox_height/2) * height)
            x_max = int((x_center + bbox_width/2) * width)
            y_max = int((y_center + bbox_height/2) * height)
            annotations[class_name].append((x_min, y_min, x_max, y_max))

    return annotations