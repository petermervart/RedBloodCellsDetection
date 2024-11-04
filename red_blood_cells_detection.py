import cv2
import numpy as np

def nothing(x):
    pass

def create_windows():
    cv2.namedWindow('trackbars', cv2.WINDOW_NORMAL)

    cv2.resizeWindow("trackbars", 700, 300)

def create_trackbars():
    cv2.createTrackbar('image', 'trackbars', 0, 1, nothing)

    cv2.createTrackbar('gaussian_blur_kernel', 'trackbars', 31, 50, nothing)

    cv2.createTrackbar('threshold_min', 'trackbars', 178, 255, nothing)

    cv2.createTrackbar('threshold_max', 'trackbars', 255, 255, nothing)

    cv2.createTrackbar('dilatation_size', 'trackbars', 2, 50, nothing)

    cv2.createTrackbar('min_color_H', 'trackbars', 134, 255, nothing)

    cv2.createTrackbar('min_color_S', 'trackbars', 0, 255, nothing)

    cv2.createTrackbar('min_color_V', 'trackbars', 210, 255, nothing)

    cv2.createTrackbar('max_color_H', 'trackbars', 176, 255, nothing)

    cv2.createTrackbar('max_color_S', 'trackbars', 74, 255, nothing)

    cv2.createTrackbar('max_color_V', 'trackbars', 240, 255, nothing)

    cv2.createTrackbar('watershed_distance_ratio', 'trackbars', 28, 50, nothing)

def main():

    create_windows()

    create_trackbars()

    while(True):

        which_image = cv2.getTrackbarPos('image', 'trackbars')

        if which_image == 0:
            basic_img = cv2.imread("image_1.png", cv2.IMREAD_COLOR)
            cv2.setTrackbarPos("dilatation_size", "trackbars", 5)
            cv2.setTrackbarPos("max_color_V", "trackbars", 239)
            cv2.setTrackbarPos("watershed_distance_ratio", "trackbars", 37)
        else:
            basic_img = cv2.imread("image_2.png", cv2.IMREAD_COLOR)
            cv2.setTrackbarPos("dilatation_size", "trackbars", 2)
            cv2.setTrackbarPos("max_color_V", "trackbars", 240)
            cv2.setTrackbarPos("watershed_distance_ratio", "trackbars", 28)

        img_source = basic_img.copy()

        img_main = cv2.cvtColor(basic_img, cv2.COLOR_BGR2HSV)

        gaussian_blur_kernel = cv2.getTrackbarPos('gaussian_blur_kernel', 'trackbars')

        treshold_max = cv2.getTrackbarPos('threshold_max', 'trackbars')

        treshold_min = cv2.getTrackbarPos('threshold_min', 'trackbars')

        dilatation_size = cv2.getTrackbarPos('dilatation_size', 'trackbars')

        color_min_h = cv2.getTrackbarPos('min_color_H', 'trackbars')

        color_min_s = cv2.getTrackbarPos('min_color_S', 'trackbars')

        color_min_v = cv2.getTrackbarPos('min_color_V', 'trackbars')

        color_max_h = cv2.getTrackbarPos('max_color_H', 'trackbars')

        color_max_s = cv2.getTrackbarPos('max_color_S', 'trackbars')

        color_max_v = cv2.getTrackbarPos('max_color_V', 'trackbars')

        watershed_ratio = cv2.getTrackbarPos('watershed_distance_ratio', 'trackbars')

        if gaussian_blur_kernel % 2 == 0:
            gaussian_blur_kernel = gaussian_blur_kernel + 1

        img_blur = cv2.GaussianBlur(img_main, (gaussian_blur_kernel, gaussian_blur_kernel), cv2.BORDER_DEFAULT)   # application of Gaussian blur

        lower_bound = np.array([color_min_h, color_min_s, color_min_v])
        upper_bound = np.array([color_max_h, color_max_s, color_max_v])

        img = cv2.inRange(img_blur, lower_bound, upper_bound)   # color filtering

        img = cv2.bitwise_and(img_blur, img_blur, mask=img)  # removing non-compliant parts from the image

        if dilatation_size % 2 == 0:
            dilatation_size += 1

        img = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilatation_size, dilatation_size)))   # dilation

        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)   # to gray model

        img = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)   # Gaussian blur again

        ret, img = cv2.threshold(img, treshold_min, treshold_max, cv2.THRESH_TOZERO)   # threshold to zero

        cv2.imshow('Before filling', img)

        img_contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)   # finding contours

        for cnt in img_contours:
            img = cv2.drawContours(img, [cnt], 0, 255, -1)   # drawing contours into the current image
            cv2.drawContours(img_source, [cnt], 0, (255, 255, 255), -1)   # drawing contours into a copy of the original image

        kernel = np.ones((3, 3), np.uint8)
        sure_bg = cv2.dilate(img, kernel, iterations=1)   # dilation = background of cells

        watershed_ratio = watershed_ratio / 50

        dist_transform = cv2.distanceTransform(img, cv2.DIST_L2, 3)   # distance based on the ratio of background to foreground
        ret, sure_fg = cv2.threshold(dist_transform, watershed_ratio * dist_transform.max(), 255, 0)   # threshold to obtain the foreground

        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)   # area between background and foreground = unknown part

        ret, markers = cv2.connectedComponents(sure_fg)   # connected components to obtain markers for watershed

        markers = markers + 1

        markers[unknown == 255] = 0

        img_new = img_source.copy()   # copying the original image with drawn contours

        markers = cv2.watershed(img_new, markers)   # watershed

        markers_length_x = len(markers)
        markers_length_y = len(markers[0])

        for i in range(0, markers_length_x):   # distortion of pixels in a crosswise manner
            for j in range(0, markers_length_x):
                if(markers[i, j] == -1):
                    img[i, j] = 0
                    if(i + 1 < markers_length_x):
                        img[i + 1, j] = 0
                    if(i - 1 > 0):
                        img[i - 1, j] = 0
                    if (j + 1 < markers_length_y):
                        img[i, j + 1] = 0
                    if (j - 1 > 0):
                        img[i, j - 1] = 0

        label_hue = np.uint8(179 * markers / np.max(markers))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)   # displaying contours in different colors

        for cnt in img_contours:
            cv2.drawContours(img_source, [cnt], 0, (255, 255, 255), -1)   # drawing contours outlines into the image

        cv2.imshow('Before finding contours', img)

        contours_all, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # finding contours in the image

        for cnt in contours_all:
            cv2.drawContours(basic_img, [cnt], 0, (0, 255, 0), 2)   # drawing contours into the original image

        print(len(contours_all))   # printing the number of found contours

        cv2.imshow('Result', basic_img)

        cv2.imshow('Image markers', labeled_img)

        k = cv2.waitKey(0) & 0xFF   # wait for a key, if it is ESC then turn off, otherwise repeat while cycle
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()