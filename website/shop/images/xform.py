from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
box = (0,0,1200,450)
f = open('imagelist.txt')
for line in f:
    im = Image.open(line.strip())
    im = im.crop(box)
    im.save('crop-' + line.strip())
    im.close()
    print "Transformed %s" % line

