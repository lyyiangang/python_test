import cv2
import numpy as np
# https://www.cnblogs.com/amxiang/p/14889393.html
# http://jfdream.com/rgb2yuv.html

def convert_rgb_to_nv12_v1(rgb_image):
    # Convert RGB image to YUV
    h, w = rgb_image.shape[:2]
    yuv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YUV)

    # Extract Y (luminance) and UV (chrominance) planes
    y_plane = yuv_image[:, :, 0]
    uv_plane = yuv_image[:, :, 1:]

    # Combine Y and UV planes to create NV12 data
    nv12_data = np.concatenate((y_plane, uv_plane.flatten()), axis=None)
    return nv12_data[:int(h * w * 3 / 2)]

def convert_rgb_to_nv12(rgb_image):
    # Convert RGB image to YUV
    h, w = rgb_image.shape[:2]
    yuv420 = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YUV_I420)
    # tmp_bgr = cv2.cvtColor(yuv420, cv2.COLOR_YUV2BGR_I420)#equal
    # cv2.imshow('tmp_bgr', tmp_bgr)
    yuv420=yuv420.reshape(-1)
    cv2.waitKey(0)
    # Extract Y (luminance) and UV (chrominance) planes
    y_start = w * h
    y_plane = yuv420[:y_start]
    u_plane = yuv420[y_start : y_start + int(w * h / 4)]
    v_plane = yuv420[y_start + int(w * h / 4) : ]
    assert u_plane.shape[0] == v_plane.shape[0]
    nv12_data = np.hstack((y_plane.reshape(-1), np.dstack((u_plane, v_plane)).reshape(-1)))
    return nv12_data
    # Combine Y and UV planes to create NV12 data
    # nv12_data = np.concatenate((y_plane, uv_plane.flatten()), axis=None)
    # return nv12_data[:int(h * w * 3 / 2)]

# def convert_nv12_to_yuv444(width, height, nv12_data):
#     y_size = width * height
#     y_plane = nv12_data[:y_size].reshape(height, width)
#     uv_plane = nv12_data[y_size:]

#     u_plane = uv_plane[0::2]
#     v_plane = uv_plane[1::2]
#     u_plane = cv2.resize(u_plane.reshape(height//2, width//2), (width, height), interpolation=cv2.INTER_NEAREST)  # Resize U channel (use NEAREST interpolation - fastest, but lowest quality).
#     v_plane = cv2.resize(v_plane.reshape(height//2, width//2), (width, height), interpolation=cv2.INTER_NEAREST)  # Resize V channel
#     yuv444 = np.dstack((y_plane, u_plane, v_plane))
#     return yuv444

def convert_nv12_to_yuv444_fast(width, height, nv12_data):
    y_start = width * height
    y_buf = nv12_data[:y_start]
    u_buf = nv12_data[y_start::2]
    v_buf = nv12_data[y_start+1::2]

    # yuv_420=np.concatenate((y_buf, u_buf, v_buf)).reshape(-1, width)
    # bgr=cv2.cvtColor(yuv_420, cv2.COLOR_YUV2BGR_I420)
    # cv2.imshow('tmp', bgr)
    # cv2.waitKey(0)


    # u_buf = np.repeat(u_buf[None, :], 2, axis=0)
    # u_buf = np.repeat(u_buf[:, :, None], 2, axis = -1)
    # u_buf = u_buf.reshape(height, width)
    # v_buf = np.repeat(v_buf[None, :], 2, axis=0)
    # v_buf = np.repeat(v_buf[:, :, None], 2, axis = -1)
    # v_buf = v_buf.reshape(height, width)
    # import ipdb;ipdb.set_trace()
    u_buf = u_buf.reshape(height//2, -1)
    v_buf = v_buf.reshape(height//2, -1)
    u_buf = cv2.resize(u_buf, (width, height), cv2.INTER_NEAREST)
    v_buf = cv2.resize(v_buf, (width, height), cv2.INTER_NEAREST)
    yuv444 = np.dstack((y_buf.reshape(height, width), u_buf, v_buf))
    return yuv444
    
def convert_nv12_to_yuv444_naive(width, height, nv12_data):
    yuv444 = np.zeros((height, width,  3), nv12_data.dtype)
    yuv444[:, :, 0] = nv12_data[:width * height].reshape(height, width)
    uv_start = width * height
    import math
    for j in range(height):
        for i in range(width):
            uv_idx = uv_start + (width * math.floor(j / 2)) + (math.floor(i / 2))*2
            u = nv12_data[uv_idx]
            v = nv12_data[uv_idx+1]
            # print(uv_idx, uv_idx + 1)
            # import ipdb;ipdb.set_trace()
            yuv444[j, i , 1:] = u, v
    return yuv444

def test_2():
    import numpy as np
    import subprocess as sp
    import shlex
    import cv2

    # sp.run(shlex.split('ffmpeg -y -f lavfi -i pic/hsv_info.PNG=size=192x108:rate=1:duration=1 -vcodec rawvideo -pix_fmt nv12 nv12.yuv'))
    sp.run(shlex.split('ffmpeg  -y -i pic/hsv_info.PNG -s 757x300 -vcodec rawvideo -pix_fmt nv12 nv12.yuv'))
    sp.run(shlex.split('ffmpeg -y -f rawvideo -video_size 757x300 -pixel_format gray -i nv12.yuv -pix_fmt gray nv12_gray.png'))


    # sp.run(shlex.split('ffmpeg -y -f rawvideo -video_size 192x162 -pixel_format gray -i nv12.yuv -pix_fmt gray nv12_gray.png'))
    #sp.run(shlex.split('ffmpeg -y -f rawvideo -video_size 192x108 -pixel_format nv12 -i nv12.yuv -vcodec rawvideo -pix_fmt yuv444p yuv444.yuv'))
    #sp.run(shlex.split('ffmpeg -y -f rawvideo -video_size 192x324 -pixel_format gray -i yuv444.yuv -pix_fmt gray yuv444_gray.png'))
    #sp.run(shlex.split('ffmpeg -y -f rawvideo -video_size 192x108 -pixel_format yuv444p -i yuv444.yuv -pix_fmt rgb24 rgb.png'))
    #sp.run(shlex.split('ffmpeg -y -f rawvideo -video_size 192x108 -pixel_format gbrp -i yuv444.yuv -filter_complex "extractplanes=g+b+r[g][b][r],[r][g][b]mergeplanes=0x001020:gbrp[v]" -map "[v]" -vcodec rawvideo -pix_fmt rgb24 yuvyuv.yuv'))
    #sp.run(shlex.split('ffmpeg -y -f rawvideo -video#_size 576x108 -pixel_format gray -i yuvyuv.yuv -pix_fmt gray yuvyuv_gray.png'))

    nv12 = cv2.imread('nv12_gray.png', cv2.IMREAD_GRAYSCALE)
    cols, rows = nv12.shape[1], nv12.shape[0]*2//3

    nv12_y_data = nv12[0:rows, :].flatten()
    nv12_u_data = nv12[rows:, 0::2].flatten()
    nv12_v_data = nv12[rows:, 1::2].flatten()

    yuv444_res = np.zeros((rows, cols, 3), np.uint8)

    for h in range(rows):
        # centralize yuv 444 data for inference framework
        for w in range(cols):
            yuv444_res[h][w][0] = (nv12_y_data[h * cols + w]).astype(np.int8)
            yuv444_res[h][w][1] = (nv12_u_data[int(h / 2) * int(cols / 2) + int(w / 2)]).astype(np.int8)
            yuv444_res[h][w][2] = (nv12_v_data[int(h / 2) * int(cols / 2) + int(w / 2)]).astype(np.int8)

    y = nv12[0:rows, :]
    shrunk_u = nv12[rows:, 0::2].copy()
    shrunk_v = nv12[rows:, 1::2].copy()

    u = cv2.resize(shrunk_u, (cols, rows), interpolation=cv2.INTER_NEAREST)  # Resize U channel (use NEAREST interpolation - fastest, but lowest quality).
    v = cv2.resize(shrunk_v, (cols, rows), interpolation=cv2.INTER_NEAREST)  # Resize V channel

    yuv444 = np.dstack((y, u, v))

    is_eqaul = np.all(yuv444 == yuv444_res)
    print('is_eqaul = ' + str(is_eqaul))  # is_eqaul = True

    # Convert to RGB for display
    yvu = np.dstack((y, v, u))  # Use COLOR_YCrCb2BGR, because it's uses the corrected conversion coefficients.
    rgb = cv2.cvtColor(yvu, cv2.COLOR_YCrCb2BGR)

    # Show results:
    cv2.imshow('nv12', nv12)
    cv2.imshow('yuv444_res', yuv444_res)
    cv2.imshow('yuv444', yuv444)
    cv2.imshow('rgb', rgb)
    cv2.waitKey()
    cv2.destroyAllWindows()

def test():
    img = cv2.imread('/home/bst/Pictures/car.png')
    h, w = img.shape[:2]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    yuv = np.array([(0.299, 0.587, 0.114),
                    (-0.14713, -0.28886, 0.436),
                    (0.615, -0.51499, -0.10001)]) @ rgb.astype(np.float32).reshape(-1, 3).T

    rgb_new = np.array([(1, 0, 1.13983),
                        (1, -0.39465, -0.58060),
                        (1, 2.03211, 0)]) @ yuv
    rgb_new = rgb_new.T.reshape((h, w, 3)).astype(np.uint8)

    # ocv_yuv = cv2.cvtColor(rgb, cv2.COLOR_RGB2YUV) 
    # ocv_bgr = cv2.cvtColor(ocv_yuv, cv2.COLOR_YUV2BGR)
    # cv2.imwrite('tmp.jpg', ocv_bgr)
    # import ipdb;ipdb.set_trace()
    # rgb->nv12->yuv
    # nv12 = cv2.cvtColor(rgb, cv2.COLOR_YUV2RGB_NV12)
    # print(f'mean diff:{(rgb_new - rgb).reshape(-1).mean()}, std::{np.std(rgb_new - rgb)}')
    bgr_new = cv2.cvtColor(rgb_new, cv2.COLOR_RGB2BGR)

    nv12=convert_rgb_to_nv12(rgb)
    yuv444 = convert_nv12_to_yuv444_fast(w, h, nv12)
    yuv444_naive = convert_nv12_to_yuv444_naive(w, h, nv12)
    # yuv444_ocv = cv2.cvtColor(rgb, cv2.COLOR_RGB2YUV)
    print(f'mean:{np.abs(yuv444 - yuv444_naive).mean()}')
    # rgb = cv2.cvtColor(yuv444, cv2.COLOR_YCrCb2BGR)
    # rgb_test = np.array([(1, 0, 1.13983),
    #                     (1, -0.39465, -0.58060),
    #                     (1, 2.03211, 0)]) @ yuv444.reshape(-1, 3).T
    # rgb_test = rgb_test.T.reshape(h, w, 3).astype(np.uint8)
    rgb = cv2.cvtColor(yuv444, cv2.COLOR_YUV2RGB)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow('img', bgr)
    cv2.imshow('ori', bgr_new)
    cv2.waitKey(0)
    # import ipdb;ipdb.set_trace()
    # cv2.imshow('bgr_new', bgr_new)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

# def test2():
#     # Example usage
#     width = 640
#     height = 480
#     nv12_data = bytearray(...)  # Replace '...' with your actual NV12 data

#     yuv444_data = convert_nv12_to_yuv444(width, height, nv12_data)


def test_aug():
    pass
test()
# test2()
# test_2()