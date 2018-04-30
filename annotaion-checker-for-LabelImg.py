#!/usr/bin/python
# -*- coding: UTF-8 -*- 

# annotaion checker.  After generating some xml files via LabelImg, we could annotate some wrong labels.
# this script will check these label names and correct them to WANTTED_LABEL
import os.path 
import glob

from xml.etree.ElementTree import ElementTree,Element

LABELIMG_XML_DIR = R"C:\Users\lyy\Documents\labelImg_xml_src_dir"
WANTTED_LABEL = "dead_knot"

# <object>
# 	<name>deat_knot</name>
def ParsingOneFile(file_path):
    tree = ElementTree()
    tree.parse(file_path)
    object_nodes = tree.findall("object")
    print("find {} object nodes".format(len(object_nodes)))
    need_write_to_new_file = False
    for obj_node in object_nodes:
        name_node = obj_node.find("name")
        if name_node.text != WANTTED_LABEL:
            print("un recognized labe name, original name:{}, new name:{}".format(name_node.text, WANTTED_LABEL))
            name_node.text = WANTTED_LABEL
            need_write_to_new_file = True
    
    if need_write_to_new_file:
        os.rename(file_path, file_path + ".bak")
        tree.write(file_path + ".new.xml")
    else:
        print("the xml is good. no any modification")



all_xml_files = glob.glob(os.path.join(LABELIMG_XML_DIR,"*.xml"))
print("begin process the .xml files in directory {}, total files:{}".format(LABELIMG_XML_DIR, len(all_xml_files)))
for file in all_xml_files:
    print("---------------------Process file {}".format(file))
    ParsingOneFile(file)
