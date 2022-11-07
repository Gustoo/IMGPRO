#python -m streamlit run ImageProcessing.py
import cv2
import numpy as np
import streamlit as st
#from cv2 import dnn_superres
import imutils
import zipfile
import os
def show():
    st.title('Collection of image processing tools')
    st.write("""By Gusto""")
    st.info("This software is used to process the uploaded image,"
            "Features include: Object Counting, Image Format Conversion,"
            "Image Compression,Convert To Jiugongge Image,Increase Image Resolution."
            )
    st.info("More features are in development!")
def changePJ(image):
# PNG TO jpg
    #png_img = cv2.imread(image)
    png_img = image
    cv2.imwrite('img.jpg', png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
def changeJP(image):
# JPG TO png
    #jpg_img = cv2.imread(image)
    jpg_img = image
    cv2.imwrite('img.png', jpg_img, [int(cv2.cv2.IMWRITE_PNG_COMPRESSION), 9])
def radioF():
    type = st.radio(
        "Choose the features you want to experience",
        ("👍",
         "Object Counting",
         'Image Format Conversion',
         'Image Compression',
         'Convert Jiugongge Image',
         "Increase Image Resolution"
         ))

    if type == "Object Counting":
        st.write('You selected Object Counting')
        Object_counting(image)

    elif type == 'Image Format Conversion':
        st.write("You select Image Format Conversion")
        Image_format_conversion(image)

    elif type == 'Image Compression':
        st.write("You select Image Compression")
        Image_Compression(image)

    elif type == 'Convert Jiugongge Image':
        st.write("You select Convert To Jiugongge Image")
        Convert_To_Jiugongge_Image(image)

    elif type == "Increase Image Resolution":
        st.write("You select Increase Image Resolution")
        #Increase_image_resolution(image)

    else :
        st.write("i like this software.")
def downloadimg(imgdl,type):
    with open(imgdl, "rb") as file:
        btn = st.download_button(
                label="Download image",
                data=file,
                file_name="Changed%s"%(type),
                mime="image/png/jpg"
              )
        if btn == True:
            st.success("The picture is downloaded successfully")
def downloadzip(imgzip):
    with open(imgzip, "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="myfile.zip",
            mime="application/zip"
        )
        if btn == True:
            st.success("The zipfile is downloaded successfully")
def Image_format_conversion(image):
    try:
        type = st.radio(
            "Which image format do you want to convert to",
            ('next time','.jpg', '.png'))
        if type == '.jpg':
            st.write('You selected jpg.')
            changePJ(image)
            downloadimg('img.jpg','.jpg')
        elif type == '.png':
            st.write("You select png.")
            changeJP(image)
            downloadimg('img.png','.png')
        else:
            st.write("Please select something.")
    except:
        st.error("Please upload a picture")
def uploadimg():
    uploaded_file = st.file_uploader("Choose a image file first", type=['png', 'jpg'])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        #st.image(opencv_image, channels="BGR")
        return opencv_image
# def Increase_image_resolution(image):
#     try:
#         #"bilinear","bicubic"
#         algorithm = "bilinear"
#         # 放大比例，可输入值2，3，4
#         scale = 2
#         original_img = image.copy()
#         sr = dnn_superres.DnnSuperResImpl_create()
#         if algorithm == "bilinear":
#             img_new = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
#         elif algorithm == "bicubic":
#             img_new = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
#         else:
#             print("Algorithm not recognized")
#
#         cv2.imwrite("bilinear.jpg", img_new)
#         downloadimg('bilinear.jpg','.jpg')
#
#     except:
#         st.error("Please upload a picture")
def Image_Compression(image):
    try:
        message = st.text_input("Please enter a zoom ratio(0.1-1)")
        size = float(message)
        if size>0.1:
            img = cv2.resize(image, (0, 0), fx=size, fy=size, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite('resize.jpg', img)
            downloadimg('resize.jpg', '.jpg')
    except:
        st.error("Please enter a zoom ratio from 0.1 to 1")
def Convert_To_Jiugongge_Image(image):
    try:
        if len(image.shape) == 2:
            last_dim = 1
        else:
            last_dim = 3
        if image.shape[0] != image.shape[1]:
            new_image = np.zeros((max(image.shape), max(image.shape), last_dim), dtype=np.uint8) + 255
            new_image[
            int((new_image.shape[0] - image.shape[0]) / 2):image.shape[0] + int((new_image.shape[0] - image.shape[0]) / 2),
            int((new_image.shape[1] - image.shape[1]) / 2):image.shape[1] + int((new_image.shape[1] - image.shape[1]) / 2),
            :] = image
        else:
            new_image = image
        col_width = int(new_image.shape[0] / 3)
        image_list = [new_image[i * col_width:(i + 1) * col_width, j * (col_width):(j + 1) * col_width, :] for i in range(3)
                      for j in range(3)]
        path = os.getcwd() + '\\' + "img"
        if not os.path.exists(path):
            os.mkdir(path)
        for i in range(9):
            cv2.imwrite(path+"\%s.jpg"%(i+1), np.array(image_list[i]))
        zipf(path)
        downloadzip("img.zip")

    except:
        st.error("Please upload a picture")
def zipf(path):
    zip_file = path + '.zip'
    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    print(z)
    for path, dirname, file_name in os.walk(path):
        fpath = path.replace(path, '')
        fpath = fpath and fpath + os.sep
        for filename in file_name:
            z.write(os.path.join(path, filename), fpath + filename)
    z.close()
    return zip_file
def Object_counting(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = cv2.Canny(blurred, 50, 130)
        #cv2.imshow('edged', edged)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        total = 0
        for c in cnts:
            if cv2.contourArea(c) < 25:
                continue
            cv2.drawContours(image, [c], -1, (204, 0, 255), 2)
            total += 1
        st.success("There are %s objects in the picture"%(total))
        st.image(edged)
    except:
        st.error("Please upload a picture")
if __name__ == '__main__':
    show()
    image = uploadimg()
    radioF()

