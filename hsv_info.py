import numpy as np
import cv2

img_file = "test.png"
original_img = cv2.imread(img_file)
img = original_img.copy()
ply_pts = []

def plot(img, pts):
    global original_img
    img = original_img.copy()
    for pt in pts:
        cv2.circle(img, center = pt, radius = 2, color = (0,0,255))
    npts = len(pts)
    if npts <2 :
        return img
    for ii in range(npts):
        if ii == npts -1 :
            cv2.line(img, pts[ii], pts[0], color=(255,0,0))
        else:
            cv2.line(img, pts[ii], pts[ii+1], color = (255, 0, 0))
    return img

def dump_info(img, pts):
    if len(pts) < 3:
        return
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv_img", hsv_img)
    pts = np.array(pts, np.int)
    min_hsv = [1.0e6, 1.0e6, 1.0e6]
    max_hsv = [-1, -1, -1]
    for ((x,y,z),val) in np.ndenumerate(hsv_img):
        if cv2.pointPolygonTest(pts, (y, x), False) <= 0:
            continue
        min_hsv[z] = min_hsv[z] if min_hsv[z] < val else val
        max_hsv[z] = max_hsv[z] if max_hsv[z] > val else val

    print("min_vals:{}, max_vals:{}".format(min_hsv, max_hsv))


def on_mouse_cb(event, x, y, flags, userdata):
    global img, original_img, ply_pts
    if event == cv2.EVENT_LBUTTONDOWN :
        ply_pts.append((x,y))
        dump_info(original_img, ply_pts)
    elif event == cv2.EVENT_RBUTTONDOWN:
        ply_pts.clear()
    img = plot(img, ply_pts)


while True:
    cv2.imshow("test", img)
    cv2.setMouseCallback("test", on_mouse_cb)
    key = cv2.waitKey(1)
    if key > 0:
        if chr(key) == 'q':
            break
        
