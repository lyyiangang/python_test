import cv2
import numpy as np
# https://www.cnblogs.com/amxiang/p/14889393.html
# http://jfdream.com/rgb2yuv.html

def convert_rgb_to_nv12(rgb_image):
    # Convert RGB image to YUV
    h, w = rgb_image.shape[:2]
    yuv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YUV)

    # Extract Y (luminance) and UV (chrominance) planes
    y_plane = yuv_image[:, :, 0]
    uv_plane = yuv_image[:, :, 1:]

    # Combine Y and UV planes to create NV12 data
    nv12_data = np.concatenate((y_plane, uv_plane.flatten()), axis=None)
    return nv12_data[:int(h * w * 3 / 2)]

def convert_nv12_to_yuv444(width, height, nv12_data):
    y_size = width * height

    y_plane = nv12_data[:y_size].reshape(height, width)
    uv_plane = nv12_data[y_size:]

    u_plane = uv_plane[0::2]
    v_plane = uv_plane[1::2]
    import ipdb;ipdb.set_trace()
    u_plane = cv2.resize(u_plane.reshape(height//2, width//2), (width, height), interpolation=cv2.INTER_NEAREST)  # Resize U channel (use NEAREST interpolation - fastest, but lowest quality).
    v_plane = cv2.resize(v_plane.reshape(height//2, width//2), (width, height), interpolation=cv2.INTER_NEAREST)  # Resize V channel
    yuv444 = np.dstack((y_plane, u_plane, v_plane))
    return yuv444

def test():
    img = cv2.imread('pic/hsv_info.PNG')
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
    # bgr_new = cv2.cvtColor(rgb_new, cv2.COLOR_RGB2BGR)

    nv12=convert_rgb_to_nv12(rgb)
    yuv444 = convert_nv12_to_yuv444(w, h, nv12)
    rgb = cv2.cvtColor(yuv444, cv2.COLOR_YCrCb2BGR)
    rgb_test = np.array([(1, 0, 1.13983),
                        (1, -0.39465, -0.58060),
                        (1, 2.03211, 0)]) @ yuv444.reshape(-1, 3).T
    rgb_test = rgb_test.T.reshape(h, w, 3).astype(np.uint8)
    bgr_test = cv2.cvtColor(rgb_test, cv2.COLOR_RGB2BGR)
    cv2.imshow('img', bgr_test)
    cv2.waitKey(0)
    import ipdb;ipdb.set_trace()
    cv2.imshow('bgr_new', bgr_new)
    cv2.imshow('img', img)
    cv2.waitKey(0)

# def test2():
#     # Example usage
#     width = 640
#     height = 480
#     nv12_data = bytearray(...)  # Replace '...' with your actual NV12 data

#     yuv444_data = convert_nv12_to_yuv444(width, height, nv12_data)


test()
# test2()