import cv2
import numpy as np
import os


def max_lines_unique_numbers(folder_path):
    max_lines = 0
    max_unique_numbers = 0
    max_file = ""

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path) as f:
                lines = f.readlines()
                unique_numbers = set()
                for line in lines:
                    if len(line.split()) > 0:
                        first_word = line.split()[0]
                        if first_word.isdigit():
                            unique_numbers.add(first_word)
                if len(lines) > max_lines or (len(lines) == max_lines and len(unique_numbers) > max_unique_numbers):
                    max_lines = len(lines)
                    max_unique_numbers = len(unique_numbers)
                    max_file = filename

    return max_file


def draw_boxes(image_path, txt_path, output_path):
    class_names = ["boneanomaly", "bonelesion", "foreignbody", "fracture",
                   "metal", "periostealreaction", "pronatorsign", "softtissue", "text"]

    colors = [[255, 0, 0], [0, 255, 0], [255, 178, 29], [255, 178, 29], [
        207, 210, 49], [71, 249, 10], [255, 128, 0], [26, 147, 52], [26, 147, 52]]

    # Load the input image
    image = cv2.imread(image_path)

    # Read the bounding box information from the txt file
    with open(txt_path, "r") as f:
        lines = f.readlines()

        # Draw the bounding boxes on the image
    for line in lines:
        data = line.strip().split()
        class_id = int(data[0])
        x = float(data[1])
        y = float(data[2])
        w = float(data[3])
        h = float(data[4])

        xmin = int((x - w/2) * image.shape[1])
        ymin = int((y - h/2) * image.shape[0])

        xmax = int((x + w/2) * image.shape[1])
        ymax = int((y + h/2) * image.shape[0])

        color = tuple(colors[class_id])
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)

        class_name = class_names[class_id]
    # Get the size of the text
        (text_width, text_height), _ = cv2.getTextSize(
            class_name, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    # Draw the text rectangle
        cv2.rectangle(image, (xmin, ymin-text_height-20),
                      (xmin+text_width+20, ymin), color, -1)
        cv2.putText(image, class_name, (xmin+10, ymin-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imwrite(output_path, image)
    print("Output image saved to", output_path)


def draw_bounding_boxes(image_path, txt_path):

    # read image
    image = cv2.imread(image_path)
    # read txt file
    with open(txt_path, "r") as f:
        lines = f.readlines()

    class_names = ["boneanomaly", "bonelesion", "foreignbody", "fracture",
                   "metal", "periostealreaction", "pronatorsign", "softtissue", "text"]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255,
                                                                     0, 255), (0, 255, 255), (255, 255, 255), (0, 0, 0), (255, 128, 0)]
    # parse bounding box information from txt file
    for line in lines:
        parts = line.strip().split(" ")
        class_id = parts[0]
        class_name = class_names[int(class_id)]
        color = colors[int(class_id)]
        x, y, w, h = map(float, parts[1:5])
        x1 = int((x - w / 2) * image.shape[1])
        y1 = int((y - h / 2) * image.shape[0])
        x2 = int((x + w / 2) * image.shape[1])
        y2 = int((y + h / 2) * image.shape[0])

        # draw bounding box on image
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, class_name, (x1, y1-30),
                    cv2.FONT_HERSHEY_DUPLEX, 2, color, 2)
    # save the output image
    cv2.imwrite("output2.jpg", image)
