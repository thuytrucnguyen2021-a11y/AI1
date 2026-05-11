import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import tkinter as tk
from tkinter import ttk

# 1. Đọc dữ liệu từ file Excel
data = pd.read_csv("C:\\Users\\Admin\\Downloads\\xe_may_cu_300_mau_updated.csv", sep=';', decimal=',', encoding='latin-1')
data.head()

# 2. Xác định biến đầu vào (features) và biến mục tiêu (target)
X = data[["Hang_xe", "Dong_xe", "Nam_san_xuat", "So_km_da_chay",
        "Tinh_trang_xe", "Phu_tung"]]
y = data["Gia_goc"]

# 3. Tiền xử lý dữ liệu
categorical_features = ["Hang_xe", "Dong_xe"]
numeric_features = ["Nam_san_xuat", "So_km_da_chay",
        "Tinh_trang_xe", "Phu_tung"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), numeric_features)])

# 4. Tạo pipeline với Linear Regression
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# 5. Chia dữ liệu train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Huấn luyện mô hình
model.fit(X_train, y_train)

# 7. Đánh giá mô hình
y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R²:", r2_score(y_test, y_pred))

# --- GIAO DIỆN CHÍNH  ---
def show_main_app():
    def calculate_price():
        try:
            new_car = pd.DataFrame({
                "Hang_xe": [brand_cb.get()],
                "Dong_xe": [model_cb.get()],
                "Nam_san_xuat": [int(year_cb.get())],
                "So_km_da_chay": [int(km_entry.get())],
                "Tinh_trang_xe": [int(status_cb.get())],
                "Phu_tung": [1 if part_cb.get() != "0" else 0]
            })
            predicted_price = model.predict(new_car)[0]
            result_label.config(text=f"Giá dự đoán: {predicted_price:,.0f} triệu đồng")
        except:
            result_label.config(text="Lỗi: Vui lòng kiểm tra dữ liệu nhập")

    # Khởi tạo cửa sổ chính
    root = tk.Tk()
    root.title("Hệ thống Dự đoán giá xe máy cũ")
    root.state('zoomed')
    root.configure(bg="#121212")

    style = ttk.Style()
    style.theme_use('default')
    large_font = ("Times", 16, "bold")
    title_font = ("Times", 28, "bold")
    button_font = ("Times", 16, "bold")

    style.configure("TLabel", background="#121212", foreground="white", font=large_font)
    style.configure("TCombobox", font=("Times", 13))
    style.configure("TEntry", font=("Times", 13))

    main_container = tk.Frame(root, bg="#121212")
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(main_container, text="Dự đoán giá xe máy cũ",
                           bg="#121212", foreground="white", font=title_font)
    title_label.pack(pady=(0, 50))

    form_frame = tk.Frame(main_container, bg="#121212")
    form_frame.pack()
    form_frame.columnconfigure((0, 1, 2, 3), weight=1, pad=20)

    # Hãng xe
    tk.Label(form_frame, text="Hãng xe:", bg="#121212", fg="white", font=large_font).grid(row=0, column=0, sticky="e", pady=15)
    brand_cb = ttk.Combobox(form_frame, values=["Honda", "Yamaha", "Suzuki"], width=20)
    brand_cb.grid(row=0, column=1, padx=20, sticky="w")

    #Dòng xe
    tk.Label(form_frame, text="Dòng xe:", bg="#121212", fg="white", font=large_font).grid(row=0, column=2, sticky="e", pady=15)
    model_cb = ttk.Combobox(form_frame, values=["Future", "Wave", "SH", "Vision"], width=20)
    model_cb.grid(row=0, column=3, padx=20, sticky="w")

    # Năm sản xuất
    tk.Label(form_frame, text="Năm sản xuất:", bg="#121212", fg="white", font=large_font).grid(row=1, column=0, sticky="e", pady=15)
    year_cb = ttk.Combobox(form_frame, values=[str(i) for i in range(2010, 2026)], width=20)
    year_cb.grid(row=1, column=1, padx=20, sticky="w")

    #Số km đã chạy
    tk.Label(form_frame, text="Số km đã chạy:", bg="#121212", fg="white", font=large_font).grid(row=1, column=2, sticky="e", pady=15)
    km_entry = tk.Entry(form_frame, width=22, font=("Times", 12), bg="#333333", fg="white", insertbackground="white")
    km_entry.grid(row=1, column=3, padx=20, sticky="w")

    # Tình trạng xe
    tk.Label(form_frame, text="Tình trạng (1-10):", bg="#121212", fg="white", font=large_font).grid(row=2, column=0, sticky="e", pady=15)
    status_cb = ttk.Combobox(form_frame, values=[str(i) for i in range(1, 11)], width=20)
    status_cb.grid(row=2, column=1, padx=20, sticky="w")

    #Phụ tùng
    tk.Label(form_frame, text="Đã thay phụ tùng:", bg="#121212", fg="white", font=large_font).grid(row=2, column=2, sticky="e", pady=15)
    part_cb = ttk.Combobox(form_frame, values=["Có", "Không"], width=20)
    part_cb.grid(row=2, column=3, padx=20, sticky="w")

    button_frame = tk.Frame(main_container, bg="#121212")
    button_frame.pack(pady=50)

    #Nút xác nhận
    btn_confirm = tk.Button(button_frame, text="Xác nhận", width=25, bg="#333333", fg="white",
                            font=button_font, relief="flat", cursor="hand2")
    btn_confirm.pack(pady=10)

    #Nút tính giá
    btn_calc = tk.Button(button_frame, text="Tính giá tiền", width=30, bg="white", fg="black",
                         font=button_font, relief="flat", cursor="hand2", command=calculate_price)
    btn_calc.pack(pady=10)

    #Hiển thị giá
    result_container = tk.Frame(main_container, bg="#1E1E1E", padx=50, pady=20)
    result_container.pack(pady=20)

    result_label = tk.Label(result_container, text="Giá dự đoán: -- triệu đồng",
                            bg="#1E1E1E", foreground="white", font=("Times", 22, "bold"))
    result_label.pack()

    root.mainloop()

# --- CỬA SỔ MỞ ĐẦU  ---
def open_main_window():
    splash.destroy()   # Đóng cửa sổ splash
    show_main_app()    # Khởi tạo và chạy giao diện chính

splash = tk.Tk()
splash.title("2OLD2SELL")
splash.configure(bg="black")
splash.state('zoomed')

# Căn giữa cửa sổ splash trên màn hình
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (400 // 2)
splash.geometry(f"600x400+{x}+{y}")

title_label = tk.Label(splash, text="2OLD2SELL",
                       bg="black", fg="white",
                       font=("Times", 36, "bold"))
title_label.pack(expand=True)

login_btn = tk.Button(splash, text="Đăng nhập",
                      font=("Times", 18, "bold"),
bg="white", fg="black",
                      command=open_main_window)
login_btn.pack(pady=30)

splash.mainloop()
