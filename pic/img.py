from PIL import Image
import pytesseract

im = Image.open('5.jpg');
imgry = im.convert('L')
imgry.show()
text = pytesseract.image_to_string(imgry,lang='chi_sim')


print(text);