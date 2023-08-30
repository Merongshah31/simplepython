from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('C:\\Users\\shah8\\OneDrive\\Pictures\\qrcode\\test.png')

result = decode(img)

print(result)
