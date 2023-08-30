from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('you location file')

result = decode(img)

print(result)

#scan qrcode
