from PIL import Image
import pytesseract
#
# 1.下载installer   https://github.com/tesseract-ocr/tesseract/wiki/Downloads
#
# 2.下载中文语言包 https://github.com/tesseract-ocr/tessdata/blob/master/chi_tra.traineddata
# chi_sim.traineddata
# chi_tra.traineddata

im = Image.open('5.jpg');
imgry = im.convert('L')
imgry.show()
text = pytesseract.image_to_string(imgry,lang='chi_sim')


print(text);