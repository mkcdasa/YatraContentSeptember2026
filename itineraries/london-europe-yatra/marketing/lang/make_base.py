"""
Removes the English text from the designer's poster (poster_en.jpg) so the
language versions can be written on top. Text on the sky and the river is
inpainted; boxes that get redrawn (date pill, amount badge, labels, panels) are
simply covered by the HTML overlay. Writes poster_base.png.

    python3 marketing/lang/make_base.py
"""
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
img = cv2.imread(os.path.join(HERE, "poster_en.jpg"))
mask = np.zeros(img.shape[:2], np.uint8)

# title + subtitle: dark red / dark text on the light golden sky
x0, y0, x1, y1 = 230, 135, 905, 352
roi = img[y0:y1, x0:x1].astype(int)
b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
dark = ((r + g + b) / 3 < 150) | ((r - g > 60) & (g < 120))
mask[y0:y1, x0:x1][dark] = 255

# "(Including International Flights)" and "+ 5% GST, + 2% TCS": light text on the river
x0, y0, x1, y1 = 430, 872, 720, 930
roi = img[y0:y1, x0:x1].astype(int)
mask[y0:y1, x0:x1][roi.mean(axis=2) > 150] = 255

mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=4)
clean = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
# soften the inpainted sky so leftover traces do not show
blur = cv2.GaussianBlur(clean, (0, 0), 14)
soft = mask.astype(float)[..., None] / 255
soft = cv2.GaussianBlur(soft, (0, 0), 4)[..., None] if soft.ndim == 2 else cv2.GaussianBlur(soft, (0, 0), 4)
if soft.ndim == 2:
    soft = soft[..., None]
clean = (clean * (1 - soft) + blur * soft).astype(np.uint8)
cv2.imwrite(os.path.join(HERE, "poster_base.png"), clean)
print("wrote poster_base.png")
