import cv2
import numpy 
import glob
import os
import sys

def run(folder_name):
    files = list(glob.glob(os.path.join(folder_name, '*.*g')))
    files = sorted(files)
    idx = 0
    while True:
        if idx >= len(files):
            idx = len(files) - 1
        elif idx < 0:
            idx = 0
        ff = files[idx]
        print(f'{ff}' )
        img = cv2.imread(ff)
        h, w = img.shape[:2]
        new_h, new_w = h//2, w//2
        left_top_xy = (w//4, h//4)
        img = img[left_top_xy[1]:left_top_xy[1] + new_h, left_top_xy[0] : left_top_xy[0] + new_w, :]
        scale = 1.5
        show_img = cv2.resize(img, (int(scale*w), int(scale * h)))
        cv2.imshow('img', show_img)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break
        elif key == ord('p'):
            idx -= 1
        elif key == ord('r'):
            idx = 0
        else:
            idx += 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Error. usage: python vis_folder.py img_folder')
        exit(1)
    folder_name = sys.argv[1]
    run(folder_name)