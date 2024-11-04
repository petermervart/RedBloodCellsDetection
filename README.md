# Detection of Red Blood Cells

## Controls
Esc - exit the program

After changing the image and other values in the trackbar, any key must be pressed to change the image.

## Procedure for Image 1

**Image 1**

![image_1](https://user-images.githubusercontent.com/55833503/222982429-421750f1-3018-46f2-9a15-35226942925b.png)

**1. Using Gaussian Blur**

I used it to remove noise (primarily the part with white blood cells and white-purple specks) from the image before applying color-based filtering. Before applying Gaussian blur, I converted the image to the HSV color model (for easier color range filtering). In this step, a relatively large kernel size of 31x31 was used (blurring even larger particles), which blurred parts of the noise and made them easier to eliminate in the next step. I opted for this blur because it was necessary to blur the edges as well, and the shape of the cells wasn't that important (a slight blur was not an issue).

![image](https://user-images.githubusercontent.com/55833503/222983073-5a8ae23c-5b16-4bac-b643-43cda537faed.png)

**2. Color Filtering**

I filtered the range of colors that best represented the color of red blood cells. A problem arose with the white reflection in the center of the cells, which was outside the color range. I had to ignore the central part of the cells because changing the color range displayed white blood cells (other bodies). Through testing, I arrived at the range: H: 134 - 176, S: 0 - 74, V: 210 - 239.

![image](https://user-images.githubusercontent.com/55833503/222983135-843da41d-94b9-4838-a303-c77e1af251a1.png)

**3. Dilation**

After filtering the colors, I used dilation to improve the situation of missing cell centers. However, with higher dilation, the cells started to connect, so I used a kernel size threshold of 5x5, which partially eliminated this problem but did not connect the cells.

![image](https://user-images.githubusercontent.com/55833503/222983235-5b58b701-2ea6-4bfb-9209-894f339e6ea0.png)

**4. Gaussian Blur + Threshold**

After dilation, I changed the image to the gray color model and applied an additional Gaussian blur with a kernel of 5x5 and a threshold to remove the misidentified cell in the center of the image (a small shape). This step slightly eliminated the dilation from the previous step. In this step, I used the value 178 - 255 and the threshold type THRESH_TOZERO, so that unwanted parts were completely eliminated.

![image](https://user-images.githubusercontent.com/55833503/222983423-1ab5c00f-2975-418e-9041-95c178cf1c15.png)

**5. Filling Holes in Cells**

I addressed the holes in the cells by finding contours that I filled in and drew onto the image. I also drew these contours onto a copy of the original image, which I then used for the watershed.

![image](https://user-images.githubusercontent.com/55833503/222984063-ad48d6fc-cc9e-4b55-9e6a-03b7c03aab1b.png)

**6. Watershed**

I used the watershed technique to remove connections between cells. The watershed was applied over the original image with the drawn contours (from step 5) to retain the shape of the cells. After the watershed technique, I drew the contours (only outlines) of the detected cells onto the image (from step 5). I did this because the watershed technique removed some cells, and I wanted to retain them. I outlined not only the main pixel but also the pixel above, below, to the right, and to the left (cross kernel). I used this method of outlining for better contour detection in the next step (without this outlining, some cells were not detected). Some connections were not eliminated, but I selected values to separate them as much as possible. The value I worked with was the ratio of background to foreground. I set this value to 37/50.

![image](https://user-images.githubusercontent.com/55833503/222984919-b098c594-c1dc-48eb-ad98-43dcf2cc1656.png)

![image](https://user-images.githubusercontent.com/55833503/222984959-852c8c96-3ace-482e-8c55-83338543e2f6.png)

**7. Contour Detection**

In the final step, I only found the contours and drew them onto the original image. This allowed me to detect 42 cells out of 45 (+1 very faintly visible in the upper part). I was unable to separate 3 connected cells that were at the edge of the image, so the watershed technique was not very effective in these cases. In this step, I used only the external contours to avoid duplicates.

![image](https://user-images.githubusercontent.com/55833503/222985493-14b71ecc-0d1c-4b21-9d91-acc85e019fc8.png)

## Procedure for Image 2

**Image 2**

![image_2](https://user-images.githubusercontent.com/55833503/222982434-1ded17ef-f250-4e4d-a2ea-72930f9a84d6.png)

The procedure for image 2 was the same as for image 1. I only changed a few parameters in the hue, dilation, and watershed technique. 

**1. Using Gaussian Blur**

![image](https://user-images.githubusercontent.com/55833503/222986437-8cea3c01-003f-415c-8302-c513dfc3f614.png)

**2. Color Filtering**

For image 2, I adjusted the maximum value of channel V to 240.

![image](https://user-images.githubusercontent.com/55833503/222986463-db70fad9-cd7e-4de5-a265-f54a8de54160.png)

**3. Dilation**

For image 2, I used a kernel size of 3x3.

![image](https://user-images.githubusercontent.com/55833503/222986476-08280b58-61bc-4795-91e5-9f2e11c119d8.png)

**4. Gaussian Blur + Threshold**

![image](https://user-images.githubusercontent.com/55833503/222986511-ca2c9e56-d0a1-4fc6-a153-b32a91889741.png)

**5. Filling Holes in Cells**

![image](https://user-images.githubusercontent.com/55833503/222986532-88a4f59a-a760-4519-8d38-847b79401bd8.png)

**6. Watershed**

For the image, I changed the foreground to background ratio to 28/50.

![image](https://user-images.githubusercontent.com/55833503/222986547-8543ba36-743d-4241-884a-2a77fa34fd06.png)

![image](https://user-images.githubusercontent.com/55833503/222986563-2f237f07-3d57-4c67-9d6f-99edf8175e8b.png)

**7. Contour Detection**

Overall, the result is worse than for image 1. This is due to much more significant overlap of the cells, which I was unable to separate entirely. In total, I managed to find 46 cells. 

![image](https://user-images.githubusercontent.com/55833503/222986586-e5b25a73-c583-451f-9b56-ccf3cadfbadd.png)

## Other Considered Solutions

To close the cells, I tried using dilation and closing, but in both cases, the cells began to connect before I could close them.

In the last detection of cells, I first tried to use erosion to increase the edges of the cell distribution, but it eliminated one cell (a very small part in image 1) in the upper right part of the image.