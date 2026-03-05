import qrcode

url = "https://www.instagram.com/"

qr = qrcode.make(url)
qr.save("insta.png")