import cv2


def sign_image(img, text, x, y, font_size):


    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (x, y-10) #todo
    fontScale = font_size
    fontColor = (0, 0, 0)
    lineType = 1

    cv2.putText(img, text, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

    # Save image
    cv2.imwrite("signed_images/sign.jpg", img)