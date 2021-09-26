from PIL import Image

def loadimg_bbox(imgfile,alphapart=False):
    if isinstance(imgfile,str):
        im = Image.open(imgfile)
    else:
        im = imgfile
        im.verify()
    #(left,upper,right,lower) = im.getbbox()
    if alphapart:
        (left,upper,right,lower) = im.getbbox()
    else:
        (left,upper,right,lower) = (0,0,im.size[0],im.size[1])
    return im,(left,upper,right,lower)

def editImgHor(imgfile1,imgfile2,imgtosave=None):
    img1, bbox1 = loadimg_bbox(imgfile1)
    img2, bbox2 = loadimg_bbox(imgfile2)
    imgbasewidth = bbox1[2] + bbox2[2]
    imgbaseheight = bbox1[3]
    imgbasesize = (imgbasewidth, imgbaseheight)
    imgbase = Image.new(mode="RGBA", size=imgbasesize)
    #imgbase.show()
    imgbase.paste(img1, box=bbox1, mask=None)
    #imgbase.show()
    bboxInImg1 = (bbox1[2],bbox1[1],imgbasewidth,imgbaseheight)
    imgbase.paste(img2, box=bboxInImg1, mask=None)
    #imgbase.show()
    if imgtosave:
        imgbase.save(imgtosave)
    return imgbase


def editImgVer(imgfile1,imgfile2,imgtosave=None):
    img1, bbox1 = loadimg_bbox(imgfile1)
    img2, bbox2 = loadimg_bbox(imgfile2)
    imgbasewidth = bbox1[2]
    imgbaseheight = bbox1[3] + bbox2[3]
    imgbasesize = (imgbasewidth, imgbaseheight)
    imgbase = Image.new(mode="RGBA", size=imgbasesize)
    #imgbase.show()
    imgbase.paste(img1, box=bbox1, mask=None)
    #imgbase.show()
    bboxInImg1 = (bbox1[0], bbox1[3], imgbasewidth, imgbaseheight)
    imgbase.paste(img2, box=bboxInImg1, mask=None)
    #imgbase.show()
    if imgtosave:
        imgbase.save(imgtosave)
    return imgbase


def editImgFillTrans(imgfile1, imgfile2, imgtosave=None):
    img1, bbox1 = loadimg_bbox(imgfile1)
    img2, bbox2 = loadimg_bbox(imgfile2)
    imgbasewidth = bbox1[2]
    imgbaseheight = bbox2[3]
    imgbasesize = (imgbasewidth, imgbaseheight)
    imgbase = Image.new(mode="RGBA", size=imgbasesize)
    bboxInBase = (bbox2)
    imgbase.paste(img2,box=bboxInBase, mask=None)
    #left,upper,right,lower
    if imgtosave:
        imgbase.save(imgtosave)
    return imgbase

def editImg(imgfile1,imgfile2,pastedir=False,imgtosave="img1edited.png",placeimgx=1.0,placeimgy=1.0):
    """Depreciated function, replaced by editImgHor and editImgVer"""
    img1, bbox1 = loadimg_bbox(imgfile1)
    img2, bbox2 = loadimg_bbox(imgfile2)
    if bbox1[2]==bbox2[2] and bbox1[3] == bbox2[3]:
        print("X,Y:",placeimgx,placeimgy)
        bboxInImg1 = (int(bbox1[2]*placeimgx),int(bbox1[1]*(1-placeimgy)),int((bbox2[3]*2)-(bbox2[3]*(1-placeimgx))),int(bbox1[3]*placeimgy))
        #bboxInImg1 = (int(bbox1[2] * placeimgx), bbox1[1], int(bbox2[3] * 2 * (1 - placeimgx)),bbox1[3])
        imgbasewidth = bbox1[2] * 2
        imgbaseheight = bbox1[3]
        print("bbox1:",bbox1)
        print("bbox2:", bbox2)
        print("Image Sizes Match!...\n")
    else:
        print("bbox1:", bbox1)
        print("bbox2:", bbox2)
        bboxInImg1 = None
    if pastedir:    #Appends Img2 vertically if pastedir is True
        #bboxInImg1 = (bbox1[0],bbox1[3],bbox1[2],bbox1[3]*2)
        bboxInImg1 = (int(bbox1[0]*(1-placeimgx)), int(bbox1[3]*placeimgy), int(bbox2[2]*placeimgx), int((bbox1[3]*2)-(bbox1[3]*(1-placeimgy))))
        imgbasewidth -= bbox1[2]
        imgbaseheight *= 2
    if bboxInImg1 != None:
        #img1.paste(img2,box=bboxInImg1,mask=None)
        #img1.show()
        #img1.save("img1edited.png")
        imgbasesize = (imgbasewidth, imgbaseheight)
        imgbase = Image.new(mode="RGBA", size=imgbasesize)
        imgbase.show()
        imgbase.paste(img1,box=bbox1,mask=None)
        imgbase.show()
        imgbase.paste(img2,box=bboxInImg1,mask=None)
        imgbase.show()
        imgbase.save(imgtosave)
    else:
        print("Error! Img1 and Img2 sizes don't match!")

def debugtestfunction(imgf):
    img = Image.open(imgf)
    img.verify()


#editImgFillTrans("testtile1.png", "0011.png", imgtosave="testfiller.png")
#debugtestfunction("inp2.png")
#editImgHor("inp2.png","inp5.png",imgtosave="inp6.png")
#editImgVer("inp3.png","inp5.png",imgtosave="inp6.png")

#editImg("inp1.png","inp2.png",pastedir=True,imgtosave="tesvert.png")    #Appends img2 to the end of img1 horizontally if direction not specified
