
def vis_nv12(frame_nv12, h):
    frame = np.frombuffer(frame_nv12, np.uint8).reshape(int(1.5 * h ), -1)
    bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV12)
    cv2.imshow('img_nv12', bgr)
    cv2.waitKey(0)
def test_nv12():
    board_nv12_file = '/home/abc/Downloads/codec/codec_nv12.yuv'
    jpeg_file = '/home/abc/Downloads/codec/codec_nv12.png'
    board_nv12 = np.fromfile(board_nv12_file, dtype = np.uint8)
    w, h = 1920, 1280
    board_nv12 = board_nv12.reshape(int(h * 1.5 ), -1)
    # 1920, 1280
    import time
    t_start = time.time()
    bgr = cv2.imread(jpeg_file)
    print(f'{time.time() - t_start}')
    nv21 = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV_I420)


    nv21 = nv21.reshape(int(h * 1.5 ), -1)
    import ffmpeg
    # jpg -> crop -> resize -> cropped_nv12
    #      -> rgb
    t_start = time.time() 
    raw_data = ffmpeg.input(jpeg_file) \
                    .filter_('scale', out_range = 'full')
    nv12_out = raw_data.crop(x = 0, y = 672, width = 1920, height = 864)\
                    .filter('scale', width = 1280, height = 576)\
                    .output('pipe:', format='rawvideo', pix_fmt='nv12') 
    nv12_buff, _ = nv12_out.run(capture_stdout=True, quiet = True)
    rgb_out = raw_data.output('pipe:', format='rawvideo', pix_fmt='rgb24') 
    test_rgb_buf, _ = rgb_out.run(capture_stdout=True, quiet = True)

    rgb_img = np.frombuffer(test_rgb_buf, np.uint8).reshape(1280, 1920, 3)
    bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
    cv2.imshow('scale_img', bgr_img)
    # ffmpeg -lavfi "scale=out_range=full" -i ./img_0_1684742356.24366593.jpg  -pix_fmt nv12 ffmpeg_full_rang.yuv
    vis_nv12(nv12_buff, 576)
    # vis_nv12(flip_out, h)

test_nv12()

