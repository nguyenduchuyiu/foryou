import qrcode
import numpy as np
from PIL import Image, ImageDraw

URL = "https://nguyenduchuyiu.github.io/foryou/"

# ——————————————
# 1) Tạo QR pink & mask trái tim (toàn bộ canvas)
# ——————————————
# Tạo QR color pink
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=4
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="pink", back_color="white").convert("RGB")
w, h = qr_img.size

# Tạo mask trái tim bằng parametric curve
mask = Image.new("L", (w, h), 0)
t = np.linspace(0, 2*np.pi, 1000)
xt = 16 * np.sin(t)**3
yt = 13 * np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
# Normalize & flip
xt = (xt - xt.min())/(xt.max()-xt.min())*(w*0.9) + w*0.05
yt = (yt - yt.min())/(yt.max()-yt.min())*(h*0.9) + h*0.05
yt = h - yt  # lật ngược theo trục y
points = list(zip(xt, yt))
ImageDraw.Draw(mask).polygon(points, fill=255, outline=255) # Thêm outline

# Ghép QR pink vào shape trái tim
heart_qr = Image.new("RGB", (w, h), "white")
heart_qr.paste(qr_img, mask=mask)

# ——————————————————
# 2) Tạo QR vuông nhỏ, màu hồng
# ——————————————————
small_size = 0.4  # tỉ lệ so với trái tim
bw = int(w * small_size)
# Sinh QR mới với kích thước phù hợp
qr2 = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=int(bw / (qr_img.size[0] / (20))),  # box_size tự tính sao cho tổng = bw
    border=4
)
qr2.add_data(URL)
qr2.make(fit=True)
qr2_img = qr2.make_image(fill_color="pink", back_color="white").convert("RGBA")

# Chuyển trắng → trong suốt
pw = qr2_img.load()
fw, fh = qr2_img.size
for y in range(fh):
    for x in range(fw):
        if pw[x,y][:3] == (255,255,255):
            pw[x,y] = (0,0,0,0)

# ——————————————————
# 3) Paste QR nhỏ vào center của heart
# ——————————————————
cx = (w - fw)//2
cy = (h - fh)//2
heart_qr = heart_qr.convert("RGBA")

# Đè một hình vuông màu trắng
white_square = Image.new("RGBA", (fw, fh), (255, 255, 255, 255))
heart_qr.paste(white_square, (cx, cy))

heart_qr.paste(qr2_img, (cx, cy), qr2_img)

# ——————————————————
# 4) Lưu kết quả
# ——————————————————
heart_qr.save("heart_with_embedded_qr.png")
print("Đã lưu file: heart_with_embedded_qr.png")
