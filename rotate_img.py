from sys import argv
import numpy as np
import cv2
from pathlib import Path
import os

if __name__ == '__main__':
    file_name = argv[1]
    out_dir = argv[2]
    print(f'reading {file_name}')
    img = cv2.imread(file_name)
    result_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    os.makedirs(out_dir, exist_ok= True)
    out_name = out_dir + '/' + Path(file_name).name
    print(f'writing to {out_name}')
    cv2.imwrite(out_name, result_img)