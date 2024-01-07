import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
import cv2

def test():
    bgr = cv2.imread('pic/crosswalk.png')
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    # random example images
    # images = np.random.randint(0, 255, (1,128, 128, 3), dtype=np.uint8)
    images = rgb[None, ...]
    images = np.repeat(images, 5, axis=0)
    # Sometimes(0.5, ...) applies the given augmenter in 50% of all cases,
    # e.g. Sometimes(0.5, GaussianBlur(0.3)) would blur roughly every second image.
    sometimes = lambda aug: iaa.Sometimes(1, aug)

    # Define our sequence of augmentation steps that will be applied to every image
    # All augmenters with per_channel=0.5 will sample one value _per image_
    # in 50% of all cases. In all other cases they will sample new values
    # _per channel_.

    seq = iaa.Sequential(
        [
            # execute 0 to 1 of the following (less important) augmenters per image
            # don't execute all of them, as that would often be way too strong
            iaa.SomeOf((0, 1),
                [
                    sometimes(iaa.GaussianBlur((0, 1.0))),
                    sometimes(iaa.Sharpen(alpha=(0, 0.8), lightness=(0.75, 1.5))), # sharpen images,
                    sometimes(iaa.LinearContrast((0.5, 1.5), per_channel=0.3)), # improve or worsen the contrast
                ],
                random_order=True
            )
        ],
        random_order=True
    )
    images_aug = seq(images=images)
    for aug_img in images_aug:
        vis_aug_img = cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR)
        cv2.imshow('aug', vis_aug_img)
        cv2.waitKey(0)

if __name__ == '__main__':
    test()