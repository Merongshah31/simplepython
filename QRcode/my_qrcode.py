import qrcode


data = 'test'

img = qrcode.make(data)
type(img)
img.save('C:\\Users\\shah8\\OneDrive\\Pictures\\qrcode\\test.png')