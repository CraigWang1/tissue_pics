# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 17:43:32 2020

@author: craig

Python script to convert labelImg .xml files to 
a .csv file that is compatible with this github's implementation of EfficientDet:
https://github.com/tristandb/EfficientDet-PyTorch/

How to call:
    python xml_to_csv.py --img_folder_path (path to image folder with .xml annotations) --csv_file (path to csv file that you want to save to)

"""

from lxml import etree
import csv
import os
import argparse


# function to extract the values from the annotation .xml file
# compatible with file_path and class_name
def find_file_val(tree, identifier):
    filePathIx = tree.find(identifier)
    value = ""

    for char in tree[filePathIx+6:]:
        if char != "<":
            value += char
        else:
            return value

# a function to extract the a bbox coord from the annotation .xml file
def find_bbox_val(tree, identifier):  #identifier is the identifier in the .xml file
    filePathIx = tree.find(identifier)  #e.g. "<xmin>" or "<ymax>"
    bbox_val = ""

    for digit in tree[filePathIx+6:]:
        try:
            int(digit)   #if its a number, then add it to xmin
            bbox_val += digit
        except:
            return int(bbox_val)   #return the xmin as an int

# a function to get all of the bbox coordinates
def find_bbox(tree):
    #extract xmin
    xmin = find_bbox_val(tree, "<xmin>")  
    ymin = find_bbox_val(tree, "<ymin>")
    xmax = find_bbox_val(tree, "<xmax>") #finds xmin, ymin, xmax, and ymax of bbox
    ymax = find_bbox_val(tree, "<ymax>")
    return xmin, ymin, xmax, ymax

# a function to assemble the row of image_path, x1, y1, x2, y2, class_name
def construct_row(xml_filepath):
    # turn xml file contents into string
    tree = etree.parse(xml_filepath)
    tree = str(etree.tostring(tree.getroot()))
    #assemble the row
    row = []
    row.append(find_file_val(tree, identifier="<path>"))  #add the filepath to the row
    row.extend([coord for coord in find_bbox(tree)])      #add the bbox coordinates (x1, y1, x2, y2)
    row.append(find_file_val(tree, "<name>"))             #adds the class_name
    return row


# a function that iterates over all .xml files in the image folder
# and adds the data from those .xml files to the csv file
def iterate_and_write(img_folder_path, csv_path):
    with open(csv_path, "w") as csvfile:
        #opens the file writer, so we are able to write on the file
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        for filename in os.listdir(img_folder_path):
            if filename.endswith(".xml"):
                annot_file = os.path.join(img_folder_path, filename)
                filewriter.writerow(construct_row(annot_file))

# the final function, does it all
# gets user img folder filepath, grabs the xml file data from the folder
# gets user csv_file, writes the data extracted from the .xml files onto the csv_file
def main():
    parser = argparse.ArgumentParser(description="Extracting annotation data into .csv format.")
    parser.add_argument("--img_folder_path",
                        help="The filepath to the folder that contains training images and .xml annotations.",
                        type=str)
    parser.add_argument("--csv_file",
                        help="The .csv file that you want to save the annotation data to.",
                        type=str)
    args = parser.parse_args()
    
    iterate_and_write(img_folder_path=args.img_folder_path,
                      csv_path=args.csv_file)
    
    print("Successful! \nCSV file saved at", args.csv_file)

if __name__ == '__main__':
    main()






