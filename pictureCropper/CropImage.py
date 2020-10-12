def crop_image(img, params):

    widthImg, heightImg = img.size

    x = widthImg * params["x"]
    y = widthImg * params["y"]
    width = widthImg * params["width"]
    height = widthImg * params["height"]

    area = (x, y, x + width, y + height)
    cropped_img = img.crop(area)
    # cropped_img.show()
    # k = 2
    # out = cropped_img.resize([int(k * s) for s in cropped_img.size])
    cropped_img.save("dataImages/"+params["number"]+".png")