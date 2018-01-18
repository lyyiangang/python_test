import numpy as np
import cv2

img_file = "seatBeltWhite.png"
original_img = cv2.imread(img_file)
img = original_img.copy()
ply_pts = []

i_before = id(img)

# def test(img):
#     other_img  = np.array([2,3])
#     np.copyto(other_img, img)
#     i_a = id(img)
#     a =0


# test(img)
# i_after = id(img)

def plot(img, pts):
    global original_img
    #img = original_img.copy()
    np.copyto(original_img, img)
    for pt in pts:
        cv2.circle(img, center = pt, radius = 4, color = (0,0,255))
    npts = len(pts)
    if npts <2 :
        return
    for ii in range(npts):
        if ii == npts -1 :
            cv2.line(img, pts[ii], pts[0], color=(255,0,0))
        else:
            cv2.line(img, pts[ii], pts[ii+1], color = (255, 0, 0))


def on_mouse_cb(event, x, y, flags, userdata):
    global img
    if event == cv2.EVENT_LBUTTONDOWN :
        ply_pts.append((x,y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        ply_pts.clear()
    plot(img, ply_pts)

while True:
    cv2.imshow("test", img)
    cv2.setMouseCallback("test", on_mouse_cb)
    key = cv2.waitKey(1)
    if key > 0:
        if chr(key) == 'q':
            break
        
