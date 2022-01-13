from time import sleep

import cv2
import numpy as np
import pyautogui as pg


def click(x,y, delay=0.0):
    delay = float(delay)
    for i in range(len(x)):
        if delay > 0:
            sleep(delay)
        pg.click(x[i],y[i])
        print('click')



def get_click_point(needle_img, threshold = 0.70):

    needle_img = cv2.imread(needle_img, cv2.IMREAD_UNCHANGED)

    first_img = pg.screenshot()
    first_img = np.array(first_img) # changing datatype of image
    first_img = cv2.cvtColor(first_img, cv2.COLOR_RGB2BGRA) # converting to 4 channels to enable matching template

    needle_img = cv2.cvtColor(needle_img, cv2.COLOR_BGR2BGRA)

    rectangles = []
    result = cv2.matchTemplate(first_img, needle_img, cv2.TM_CCOEFF_NORMED)

    w = needle_img.shape[1]
    h = needle_img.shape[0]

    yloc, xloc = np.where(result >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(max_val)


    for (x,y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)]) # 2nd append for later group function (cannot be single rectangle, needed at least 2)

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)


    if not len(rectangles) == 0:
        locx = []
        locy = []
        for i in range(len(rectangles)):
            locx.append(int(rectangles[i][0] + rectangles[i][2] / 2))
            locy.append(int(rectangles[i][1] + rectangles[i][3] / 2))
            print(locx)
            print(locy)
        return locx, locy, True
    else:
        return False, True, False

def test(img, threshold = 0.70):

    needle_img = cv2.imread('test\\'+str(img), cv2.IMREAD_UNCHANGED)

    first_img = cv2.imread('test\\board.png', cv2.IMREAD_UNCHANGED)
    first_img = cv2.cvtColor(first_img, cv2.COLOR_RGB2BGRA) # converting to 4 channels to enable matching template

    needle_img = cv2.cvtColor(needle_img, cv2.COLOR_BGR2BGRA)

    rectangles = []

    cv2.imshow('First', first_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    result = cv2.matchTemplate(first_img, needle_img, cv2.TM_CCOEFF_NORMED)

    cv2.imshow('Result', result)
    cv2.waitKey()
    cv2.destroyAllWindows()

    w = needle_img.shape[1]
    h = needle_img.shape[0]

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    cv2.rectangle(first_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 2)
    yloc, xloc = np.where(result >= threshold)


    for (x,y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)]) # 2nd append for later group function (cannot be single rectangle, needed at least 2)

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    cv2.imshow('Found (click is at middle of the rectangle)', first_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    if not len(rectangles) == 0:
        return int(rectangles[0][0] + rectangles[0][2] / 2), int(rectangles[0][1] + rectangles[0][3] / 2)
    else:
        return False, True
if __name__ == "__main__":
    x, y = get_click_point()
    click(x,y)
