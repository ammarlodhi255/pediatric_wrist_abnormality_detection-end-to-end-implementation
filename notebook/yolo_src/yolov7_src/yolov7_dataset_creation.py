import os

# Folder path
folder_path = r"D:\Ammar's\FYP_DATA\YOLOv7 Formatted Data (with test)\images\test"

# Open the text file for writing
with open(r"D:\Ammar's\FYP_DATA\YOLOv7 Formatted Data (with test)\test.txt", 'w') as file:
  # Iterate over all files in the folder
  for file_name in os.listdir(folder_path):
    # Write the file path to the text file
    file.write(os.path.join(folder_path, file_name) + '\n')