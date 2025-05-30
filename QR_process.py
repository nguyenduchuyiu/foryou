import cv2
import numpy as np
from PIL import Image, ImageFilter

def recolor_qr_code(image_path, pink=(255, 192, 203), threshold=240):
    """
    Đọc một hình ảnh mã QR hình trái tim, chuyển đổi màu sắc, làm sắc nét, loại bỏ nhiễu, bồi tụ và xói mòn, sau đó làm sắc nét lại.

    :param image_path: Đường dẫn đến hình ảnh mã QR.
    :param pink: Bộ giá trị RGB cho màu hồng. Mặc định là (255, 192, 203).
    :param threshold: Ngưỡng để xác định màu trắng. Các giá trị RGB trên ngưỡng này được coi là màu trắng. Mặc định là 240.
    """
    try:
        # Mở hình ảnh bằng PIL
        img = Image.open(image_path).convert("RGB")
        img_np = np.array(img)

        # Chuyển đổi hình ảnh thành ảnh xám
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Tạo mask dựa trên ngưỡng
        mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]

        # Đảo ngược mask để các pixel không phải màu trắng là màu trắng
        mask = cv2.bitwise_not(mask)

        # Làm sắc nét hình ảnh trước khi xử lý hình thái
        img = Image.fromarray(img_np)
        img = img.filter(ImageFilter.SHARPEN)
        img_np = np.array(img)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
        mask = cv2.bitwise_not(mask)

        # Loại bỏ nhiễu bằng phép toán mở (erosion followed by dilation)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # Bồi tụ (dilation) để làm dày các đường
        mask = cv2.dilate(mask, kernel, iterations=1)

        # Xói mòn (erosion) để làm mỏng các đường
        mask = cv2.erode(mask, kernel, iterations=1)

        # Chuyển đổi mask trở lại thành hình ảnh màu
        color_mask = np.zeros_like(img_np)
        color_mask[mask != 0] = pink  # Đặt màu hồng cho các pixel không phải màu trắng

        # Kết hợp mask màu với hình ảnh gốc
        img_np[mask != 0] = color_mask[mask != 0]

        # Chuyển đổi trở lại thành hình ảnh PIL
        img = Image.fromarray(img_np)

        # Làm sắc nét hình ảnh sau khi xử lý hình thái
        img = img.filter(ImageFilter.SHARPEN)

        # Lưu hình ảnh đã sửa đổi
        img.save("heart_shaped_qr_code_recolored.png")
        print("Đã lưu hình ảnh đã sửa đổi thành heart_shaped_qr_code_recolored.png")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp hình ảnh tại '{image_path}'.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Sử dụng hàm
recolor_qr_code("heart-shaped-qr-code.jpg")