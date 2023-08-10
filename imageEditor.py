from PIL import Image, ImageEnhance, ImageFilter
import os

path = './imgs'
pathOut = '/editedImgs'

for filename in os.listdir(path):
    img = Image.open(f"{path}/{filename}")
    # img.show()
    print(img.size, img.format, img.mode)

    out = img.rotate(-90)
    t = img.filter(ImageFilter.SHARPEN)
    t2 = img.convert('L')
    t.show()
    t2.show()
    t3 = t2.convert('RGB')
    t3.show()
    # out.show()
    out.save(f"./{pathOut}/{os.path.splitext(filename)[0]}_edited.jpg")