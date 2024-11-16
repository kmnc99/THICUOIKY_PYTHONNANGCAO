#GIAO DIỆN MÁY TÍNH
#import
import tkinter as tk
from tkinter import ttk
import os
#Cửa số lớn hiển thị ra màn hình khi run
win = tk.Tk()
#Tiêu đề của cửa sổ
win.title("Calculator Basic")
#Thay đổi icon cho cửa sổ
win.iconbitmap
PATH_DIRECTORY = os.path.dirname(__file__) #Vào thằng folder dự án đang làm việc
PATH_IMAGES = os.path.join(PATH_DIRECTORY, 'imgs') #Từ folder dự án join vào folder ảnh 'imgs'
win.iconbitmap(os.path.join(PATH_IMAGES, 'icon-calculator.ico'))
#Tạo tab
notebook = ttk.Notebook(win)
#Tab 1 tính toán
tabTinhToan = ttk.Frame(notebook)
notebook.add(tabTinhToan, text = "Tính toán")

# Tạo frame cho nhập số
frame_nhapso = ttk.LabelFrame(tabTinhToan, text="Nhập số", padding=(10, 10))
frame_nhapso.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

# Tạo frame cho phép tính
frame_pheptinh = ttk.LabelFrame(tabTinhToan, text="Phép tính", padding=(10, 10))
frame_pheptinh.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

# Tạo frame cho kết quả
frame_ketqua = ttk.LabelFrame(tabTinhToan, text="Kết quả", padding=(10, 10))
frame_ketqua.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

# Khung nhập số
a_label = tk.Label(frame_nhapso, text="Nhập số thứ nhất",font=('Arial', 10), padx=5, pady=5, fg="Blue")
a_label.grid(column=0, row=0, padx=5, pady=5)

number_a = tk.StringVar()
a_entry = tk.Entry(frame_nhapso, width=20, textvariable=number_a)
a_entry.grid(column=1, row=0)
a_entry.focus()

b_label = tk.Label(frame_nhapso, text="Nhập số thứ hai",font=('Arial', 10), padx=5, pady=5, fg="Blue")
b_label.grid(column=0, row=1, padx=5, pady=5)

number_b = tk.StringVar()
b_entry = tk.Entry(frame_nhapso, width=20, textvariable=number_b)
b_entry.grid(column=1, row=1)

# Tạo widget Entry cho kết quả
result_entry = tk.Entry(frame_ketqua, width=20)
result_entry.grid(column=0, row=0)

# Các hàm tính toán
def phep_cong():
    try:
        ketqua = float(number_a.get()) + float(number_b.get())
        show_ketqua(ketqua)
    except ValueError:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "Error")

def phep_tru():
    try:
        ketqua = float(number_a.get()) - float(number_b.get())
        show_ketqua(ketqua)
    except ValueError:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "Error")

def phep_nhan():
    try:
        ketqua = float(number_a.get()) * float(number_b.get())
        show_ketqua(ketqua)
    except ValueError:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "Error")

def phep_chia():
    try:
        ketqua = float(number_a.get()) / float(number_b.get())
        show_ketqua(ketqua)
    except ValueError:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "Error")
    except ZeroDivisionError:
        result_entry.delete(0, tk.END)
        result_entry.insert(0, "Divide by 0")

def delete_all():
    a_entry.delete(0, tk.END)
    b_entry.delete(0, tk.END)
    result_entry.delete(0, tk.END)

def show_ketqua(ketqua):
    result_entry.delete(0, tk.END)
    result_entry.insert(0, str(ketqua))

# Buntton phép tính
action_cong = tk.Button(frame_pheptinh, text="+", command=phep_cong, font=('Arial', 10), padx=10, pady=10, bg="#f0f0f0", fg="Red")
action_cong.grid(column=0, row=0, padx=5, pady=5)

action_tru = tk.Button(frame_pheptinh, text="-", command=phep_tru, font=('Arial', 10), padx=10, pady=10, bg="#f0f0f0",fg="Red")
action_tru.grid(column=1, row=0, padx=5, pady=5)

action_nhan = tk.Button(frame_pheptinh, text="x", command=phep_nhan,font=('Arial', 10), padx=10, pady=10, bg="#f0f0f0", fg="Red")
action_nhan.grid(column=0, row=1, padx=5, pady=5)

action_chia = tk.Button(frame_pheptinh, text="/", command=phep_chia, font=('Arial', 10), padx=10, pady=10,bg="#f0f0f0", fg="Red")
action_chia.grid(column=1, row=1, padx=5, pady=5)

# Nút xóa
action_xoa = tk.Button(frame_pheptinh, text="Xóa", command=delete_all, font=('Arial', 10), padx=10, pady=10,bg="#f0f0f0",fg="Green")
action_xoa.grid(column=0, row=2, columnspan=3, padx=10, pady=10)

#Tab 2 đổi đơn vị đo
TabDonViDo = ttk.Frame(notebook)
notebook.add(TabDonViDo, text= "Đơn vị đo")

#Khung nhập số cho đơn vị đo
frame_nhapso_donvido = ttk.LabelFrame(TabDonViDo, text="Nhập chiều dài", padding=(10,10))
frame_nhapso_donvido.grid(column=0,row=0, padx = 10, pady=10, sticky="nsew")

# Nhập chiều dài
chieu_dai_label = tk.Label(frame_nhapso_donvido, text="Nhập chiều dài:", font=('Arial', 10),fg="Blue")
chieu_dai_label.grid(column=0, row=0, padx=10, pady=5)

chieu_dai_var = tk.StringVar()
nhap_chieu_dai = tk.Entry(frame_nhapso_donvido, width=20, textvariable=chieu_dai_var)
nhap_chieu_dai.grid(column=1, row=0)

# Đơn vị gốc
don_vi_goc_label = tk.Label(frame_nhapso_donvido, text="Đơn vị gốc:", font=('Arial', 10),fg="Blue")
don_vi_goc_label.grid(column=0, row=1, padx=10, pady=5)

don_vi_goc_var = tk.StringVar()
don_vi_goc_combo = ttk.Combobox(frame_nhapso_donvido, textvariable=don_vi_goc_var)
don_vi_goc_combo['values'] = ('km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm')
don_vi_goc_combo.grid(column=1, row=1)

# Đơn vị đích
don_vi_dich_label = tk.Label(frame_nhapso_donvido, text="Đơn vị đích:", font=('Arial', 10),fg="Blue")
don_vi_dich_label.grid(column=0, row=2, padx=10, pady=5)

don_vi_dich_var = tk.StringVar()
don_vi_dich_combo = ttk.Combobox(frame_nhapso_donvido, textvariable=don_vi_dich_var)
don_vi_dich_combo['values'] = ('km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm')
don_vi_dich_combo.grid(column=1, row=2)

# Hàm chuyển đổi đơn vị đo cho nút chuyển đổi
def chuyen_doi_chieu_dai():
    try:
        chieu_dai = float(chieu_dai_var.get())
        don_vi_goc = don_vi_goc_var.get()
        don_vi_dich = don_vi_dich_var.get()
        
        # Hàm chuyển đổi chiều dài
        chuyen_doi_chieu_dai_meters = {
            'km': 1000,
            'hm': 100,
            'dam': 10,
            'm': 1,
            'dm': 0.1,
            'cm': 0.01,
            'mm': 0.001
        }

        if don_vi_goc in chuyen_doi_chieu_dai_meters and don_vi_dich in chuyen_doi_chieu_dai_meters:
            # Chuyển đổi sang mét
            chieu_dai_meters = chieu_dai * chuyen_doi_chieu_dai_meters[don_vi_goc]
            # Chuyển đổi từ mét sang đơn vị đích
            chuyen_doi_length = chieu_dai_meters / chuyen_doi_chieu_dai_meters[don_vi_dich]
            ket_qua_chuyen_doi.delete(0, tk.END)
            ket_qua_chuyen_doi.insert(0, str(chuyen_doi_length))
        else:
            ket_qua_chuyen_doi.delete(0, tk.END)
            ket_qua_chuyen_doi.insert(0, "Đơn vị không hợp lệ!")
    except ValueError:
        ket_qua_chuyen_doi.delete(0, tk.END)
        ket_qua_chuyen_doi.insert(0, "Error")

# Kết quả chuyển đổi
ket_qua_chuyen_doi = tk.Entry(TabDonViDo, width=20)
ket_qua_chuyen_doi.grid(column=0, row=3, columnspan=2)

# Nút chuyển đổi
chuyen_doi_button = tk.Button(TabDonViDo, text="Chuyển đổi", command=chuyen_doi_chieu_dai, font=('Arial', 10), padx=10, pady=10, bg="#f0f0f0",fg="Green")
chuyen_doi_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

notebook.pack(expand=1, fill="both")
win.mainloop()