import os
import re
import logging
import argparse
import subprocess
import time
import signal
lg = logging.getLogger(__name__)
lg.setLevel(logging.INFO)
logging.basicConfig(format= logging.BASIC_FORMAT)

import cv2
import numpy as np
import psutil

parser = argparse.ArgumentParser()
parser.add_argument('--output_dir', default = 'cap_video', type = str)
parser.add_argument('--stage', default = 1, type = int)
parser.add_argument('-d', '--device', default = 0, type = int)
parser.add_argument('--use_uvc_backend', default = 0, type = int)
parser.add_argument('--use_uvc_time', default = 0, type = int)
parser.add_argument('--vis', default = 1, type = int)
parser.add_argument('--calib_mode', default = 0, type = int)
parser.add_argument('--resolution_width', default = 1280, type = int)
parser.add_argument('--resolution_height', default = 720, type = int)
args = parser.parse_args()
idx_to_name = ('cam',)

boot_time = psutil.boot_time()

out_video_name = 'out.avi'
continue_run = True

def signal_handler(signal,frame):
    global continue_run
    continue_run= False

class VideoCapture:
    def __init__(self, uid_or_device_index, use_uvc : bool):
        if use_uvc:
            import uvc
            lg.info('using uvc as backend')
            devices = uvc.device_list()
            lg.info('there are {} camera devices, devices:'.format(len(devices)))
            select_device = None
            for d in devices:
                lg.info(d)
                if d['uid'] == uid_or_device_index:
                    select_device = d
            lg.info('opening {}'.format(select_device['uid']))
            self.cap = uvc.Capture(select_device['uid'])
        else:
            lg.info('using opencv as camera backend')
            self.cap = cv2.VideoCapture(uid_or_device_index)
            #self.cap.set(cv2.CAP_PROP_EXPOSURE,30)
            assert self.cap.isOpened(), 'can not open {}'.format(uid_or_device_index)
    
    def set_resolution(self, w_h : tuple):
        if isinstance(self.cap, cv2.VideoCapture):
            assert self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_h[0])
            assert self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, w_h[1])
        else:
            self.cap.frame_mode = (w_h[0], w_h[1], 30)

    def read(self):
        if isinstance(self.cap, cv2.VideoCapture):
            time_stamp = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            out_time = uptime()/1000
            print('opencv time stamp {}, uvc timestamp:{}, diff:{}'.format(time_stamp, out_time, out_time - time_stamp))
            return self.cap.read()
        else:
            frame = self.cap.get_frame_robust()
            return frame != None, frame.img

def uptime():
    if args.use_uvc_time:
        import uvc
        return uvc.get_time_monotonic() * 1000000 # keep the result with optitrack
    else:
        return round((time.time() - boot_time) * 1e6)

def correct_str_for_filename(file_name):
    return file_name.replace(' ', '_')

def simplify_usbid(usb_id):
    """replace special chars to -
        e.g. replace '0000:00:14.0-9' to 0000_00_14.0-9
    """
    return str.replace(usb_id, ':', '_')
def run():
    caps = []
    output_dirs = []
    valid_devices = [args.device]
    videoWriter = cv2.VideoWriter(out_video_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (args.resolution_width, args.resolution_height))
    for cam_id, device_name in zip(valid_devices, idx_to_name):
        cap = VideoCapture(cam_id, use_uvc = args.use_uvc_backend)
        
        if 'diweitai' in device_name:
            logging.warn('force set diweitai camera resolution to 1920*1080') 
            # cap.set_resolution((1280,720))
            cap.set_resolution((args.resolution_width, args.resolution_height))

        elif 'cam0135' in device_name:
            logging.warn('force set cam0135 camera resolution to 1280*720') 
            # cap.set_resolution((1280,720))
            cap.set_resolution((args.resolution_width, args.resolution_height))

        else:
            cap.set_resolution((args.resolution_width, args.resolution_height))
        caps.append(cap)
        cur_dir = os.path.join(args.output_dir, '{}_stage_{}'.format(device_name, args.stage))
        output_dirs.append(cur_dir)
        os.makedirs(cur_dir, exist_ok = True)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while continue_run:
        imgs = []
        times_after = []
        times_before = []
        for cap in caps:
            times_before.append(uptime())
            ret, img = cap.read()
            # long stamp = cap.get( CV_CAP_PROP_POS_MSEC ); // THIS DOESN'T SEEM TO WORK
            if not ret:
                lg.error('can not read frame')
                exit()
            imgs.append(img)
            times_after.append(uptime())
        for cur_img, t_before, t_after, cur_dir in zip(imgs, times_before, times_after, output_dirs):
            out_name = os.path.join(cur_dir, '{}_{}.png'.format(t_before, t_after))
            videoWriter.write(cur_img)
            print(f'output_name:{out_name}')
            ret = cv2.imwrite(out_name, cur_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            assert ret, 'can not write image to {}'.format(out_name)
        
        if args.calib_mode:
            print('calib mode, only one frame is saved')
            break

        if args.vis:    
            for cam_name, img in zip(idx_to_name, imgs):
                cv2.line(img, (0, int(img.shape[0]/2)),(int(img.shape[1]),int(img.shape[0]/2)),(0,0,0),1)
                cv2.line(img, (int(img.shape[1]/2),0),(int(img.shape[1]/2),int(img.shape[0])),(0,0,0),1)
                cv2.imshow(cam_name, img)
            key = cv2.waitKey(1)
            if key == 27 or key == ord('q'):
                lg.warn('stop recording')
                break

def test_2_get_time_methods():
    import uvc
    t1 = uvc.get_time_monotonic() * 1000 # keep the result with optitrack
    t2 = round((time.time() - boot_time) * 1e6)
    print('t1:{}, t2:{}'.format(t1, t2))

if __name__ == '__main__':
    lg.info('args:{}'.format(args))
    run()
    lg.info(f'write video to {out_video_name}')
    lg.info('done')