import os
import re
import logging
import argparse
lg = logging.getLogger(__name__)
lg.setLevel(logging.INFO)
logging.basicConfig(format= logging.BASIC_FORMAT)

import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--output_dir', default = 'tmp', type = str)
parser.add_argument('-d', '--devices', default = '0', type = str)
parser.add_argument('-W', default = 1280, type = int)
parser.add_argument('-H', default = 720, type = int)
args = parser.parse_args()

def run(args):
    w, h = args.W, args.H 
    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok= True)
    lg.info(f'saving result to {out_dir}')
    devices = [ int(d) for d in args.devices.split(',')]
    lg.info(f'trying to open devices:{devices}')
    caps = []
    for d in devices:
        lg.info(f'opening {d}')
        cap = cv2.VideoCapture(d)
        assert cap.isOpened(), f'can not open {d}'
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        caps.append(cap)
    frame_idx = 0    
    while True:
        imgs = []
        for idx, cap in enumerate(caps):
            ret, img = cap.read()
            assert ret, 'can not read frame'
            imgs.append(img)
            cv2.imshow(str(idx), img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            for idx, img in enumerate(imgs):
                name = os.path.join(out_dir, f'cam{idx}_{frame_idx}.jpg')
                lg.info(f'wrting {name}')
                ret = cv2.imwrite(name, img)
                assert ret, f'can not write {name}'
        
        frame_idx += 1

if __name__ == '__main__':
    run(args)