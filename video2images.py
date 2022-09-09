import cv2
import os
import numpy as np
import logging
import coloredlogs
from argparse import ArgumentParser
lg = logging.getLogger(__name__)
coloredlogs.install(logging.DEBUG)


def parse_args():
    parser = ArgumentParser(description="extract img from video")
    parser.add_argument('input_video', type=str, help='input video path')
    parser.add_argument("--output-dir", type=str, help="output dir to save images")
    parser.add_argument("--image-extention", type=str, choices=['jpg', 'png'], default='jpg')
    parser.add_argument("--interval", type=int, default=1, help="interval time to save image")
    args = parser.parse_args()
    return args

def get_infomation(cap, input_video, output_dir, interval):
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    lg.info('input video path is {}'.format(input_video))
    lg.info('output directory is {}'.format(output_dir))
    lg.info('interval is {}'.format(interval))
    lg.info('fps {}, total num {}, size:{}x{}'.format(fps, number, height, width))
    info_file = os.path.join(output_dir, 'info.txt')
    with open(info_file, 'w') as f:
        f.write('orignal video path is: {}\n'.format(os.path.abspath(input_video)))
        f.write('video fps is: {}, frame number is {}, size: {}x{}, \n'.format(fps, number, height, width))
        f.write('extract interval: {}\n'.format(interval))
    return


def run():
    args = parse_args()
    input_video = args.input_video
    assert os.path.exists(input_video), '{} doest no exist'.format(input_video)
    output_dir = 'tmp' if not args.output_dir else args.output_dir
    os.makedirs(output_dir, exist_ok= True)
    cap = cv2.VideoCapture(input_video)
    interval = args.interval
    get_infomation(cap, input_video, output_dir, interval)
    idx = 0
    prefix = os.path.basename(input_video).rsplit('.')[0]
    while True:
        ret, img = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            ret = cv2.imwrite(os.path.join(output_dir, '{}_{}.{}'.format(prefix, idx,args.image_extention)), img)
            if not ret:
                lg.warning('can not save frame')
        idx += 1
        if idx % 100 == 0:
            lg.info('{}'.format(idx))
    
    lg.info('done! total frame is {}'.format(idx))

if __name__ == '__main__':
    run()