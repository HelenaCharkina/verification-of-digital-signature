import cv2


def crop_image(img, params, len):

    widthImg, heightImg = img.size

    x = widthImg * params["x"]
    y = widthImg * params["y"]
    width = widthImg * params["width"]
    height = widthImg * params["height"]

    area = (x, y, x + width, y + height)
    cropped_img = img.crop(area)

    if str(len) == params["number"]:

        area_r = (x, y, x + width, y + height/2)
        r_img = img.crop(area_r)
        r_img.save("dataImages/r.png")
        area_s = (x, y + height/2, x + width, y + height)
        s_img = img.crop(area_s)
        s_img.save("dataImages/s.png")
    else:
        cropped_img.save("dataImages/"+params["number"]+".png")