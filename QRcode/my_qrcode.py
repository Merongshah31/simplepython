import qrcode


data = 'test'

img = qrcode.make(data)
type(img)
img.save('#your location file')

#made Qrcode
