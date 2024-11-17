import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from Databasee import AppDatabase

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống quản lý")

        # Biến kết nối cơ sở dữ liệu
        self.db_name = tk.StringVar(value='mydb210')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='quanlysinhvien2')

        # Giao diện đăng nhập
        self.create_login_screen()
    # Giao diện đăng nhập
    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="ĐĂNG NHẬP", font=("Arial", 16, "bold"),fg="#EC2A43").grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.login_frame, text="Tên người dùng:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
        tk.Entry(self.login_frame, textvariable=self.user, font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Mật khẩu:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w")
        tk.Entry(self.login_frame, textvariable=self.password, show="*", font=("Arial", 10)).grid(row=2, column=1)

        tk.Button(self.login_frame, text="Đăng nhập", command=self.connect_db, font=("Arial", 10),bg="#FFDB59", width=10).grid(row=3, column=0, columnspan=2, pady=10)
        
    # Kết nối dữ liệu = Đăng nhập
    def connect_db(self):
        self.database = AppDatabase(
            db_name=self.db_name.get(),
            user=self.user.get(),
            password=self.password.get(),
            host=self.host.get(),
            port=self.port.get()
        )
        if self.database.connect():
            messagebox.showinfo("Đăng nhập thành công", "Bạn đã đăng nhập thành công!")
            self.login_frame.pack_forget()  # Ẩn giao diện đăng nhập
            self.create_main_screen()  # Hiển thị giao diện chính sau khi đăng nhập
        else:
            messagebox.showerror("Đăng nhập thất bại", "Kiểm tra lại thông tin đăng nhập!")

    def create_main_screen(self):
        # Tạo notebook cho tab
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Tab quản lý sinh viên
        self.student_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.student_tab, text="Quản lý sinh viên")
        self.create_student_management_tab(self.student_tab)
        
        # Tab about
        self.student_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.student_tab, text="About")
        self.about_tab(self.student_tab)
        
    # Giao diện chinh - Quản lý sinh viên
    def create_student_management_tab(self, tab):
        lable_title = tk.Label(tab, text="QUẢN LÝ SINH VIÊN", font=("Arial", 20, "bold"), fg="#033E8C")
        lable_title.pack(pady=10)

        # Frame chứa 'Tải dữ liệu' và 'Tìm kiếm'
        frame = tk.Frame(tab)
        frame.pack(padx=10, pady=10, fill="x")

        # Frame tải dữ liệu sinh viên
        query_frame = tk.LabelFrame(frame, text="Tải dữ liệu", font=("Arial", 12, "bold"), fg="#EC2A43")
        query_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        tk.Label(query_frame, text="Nhập tên bảng:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name, font=("Arial", 10)).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(query_frame, text="Tải lên", command=self.load_data, font=("Arial", 10),bg="#FFDB59", width=10).grid(row=0, column=2, padx=5, pady=5)

        # Frame tìm kiếm sinh viên
        search_frame = tk.LabelFrame(frame, text="Tìm kiếm sinh viên", font=("Arial", 12, "bold"), fg="#EC2A43")
        search_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        tk.Label(search_frame, text="Nhập MSSV:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 10))
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(search_frame, text="Tìm kiếm", command=lambda: self.search_student(search_entry.get()), font=("Arial", 10),bg="#FFDB59", width=10).grid(row=0, column=2, padx=5, pady=5)
        
        # Tiêu đề thêm sinh viên mới
        title_label = tk.Label(tab, text="THÊM SINH VIÊN MỚI", font=("Arial", 12,"bold"), fg="#08ad56", anchor="w")
        title_label.pack(padx=0, anchor="w")  # Căn trái và đệm với margin
        
        # Thêm LabelFrame mới cho sinh viên (Mã, Tên, Ngành)
        student_info_frame = tk.LabelFrame(tab, text="Thông tin sinh viên", font=("Arial", 12, "bold"), fg="#EC2A43")
        student_info_frame.pack( padx=10,anchor="w", expand=True,fill="x")
        
        # Thêm sinh viên
        tk.Label(student_info_frame, text="Nhập tên sinh viên:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = tk.Entry(student_info_frame, font=("Arial", 10), width=100)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(student_info_frame, text=" Nhập mã sinh viên:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.student_name_entry = tk.Entry(student_info_frame, font=("Arial", 10), width=100)
        self.student_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(student_info_frame, text="Nhập ngành học:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.student_major_entry = tk.Entry(student_info_frame, font=("Arial", 10), width=100)
        self.student_major_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Nút Tạo (Insert) dữ liệu sinh viên
        tk.Button(student_info_frame, text="Tạo mới", command=self.insert_student, font=("Arial", 10),bg="#FFDB59", width=10).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Xóa sinh viên
        tk.Label(student_info_frame, text="Nhập mã SV để xóa:", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=5, pady=5)
        self.student_delete_entry = tk.Entry(student_info_frame, font=("Arial", 10), width=100)
        self.student_delete_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Nút Xóa sinh viên
        tk.Button(student_info_frame, text="Xóa sinh viên", command=self.delete_student, font=("Arial", 10),bg="#FFDB59", width=10).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Tiêu đề căn bên trái cho bảng dữ liệu sinh viên
        title_label = tk.Label(tab, text="BẢNG THÔNG TIN SINH VIÊN", font=("Arial", 12, "bold"), fg="#08ad56", anchor="w")
        title_label.pack(padx=10, anchor="w")  # Căn trái và đệm với margin
        
        # Bảng hiển thị dữ liệu sinh viên
        self.tree = ttk.Treeview(tab, columns=('STT', 'HỌ VÀ TÊN', 'MSSV', 'NGÀNH HỌC'), show='headings', height=10)
        self.tree.pack(padx=10, pady=5, fill="x")
        self.tree.heading('STT', text='STT')
        self.tree.heading('HỌ VÀ TÊN', text='HỌ VÀ TÊN')
        self.tree.heading('MSSV', text='MSSV')
        self.tree.heading('NGÀNH HỌC', text='NGÀNH HỌC')
    
    
    # Tải dữ liệu lên           
    def load_data(self):
        try:
            # Truy vấn dữ liệu từ bảng trong cơ sở dữ liệu
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(query)
            rows = self.database.cur.fetchall()

            self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ

            # Hiển thị dữ liệu lên bảng
            for index, row in enumerate(rows, start=1):
                self.tree.insert('', 'end', values=(index, row[1], row[0], row[2]))  # Giả sử thứ tự cột là [tên, MSSV, ngành học]
        except Exception as e:
            messagebox.showerror("Lỗi tải dữ liệu", f"Lỗi tải dữ liệu: {e}")
    # Tìm kiếm sinh viên
    def search_student(self, mssv):
        try:
            query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(query, (mssv,))
            rows = self.database.cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
            for index, row in enumerate(rows, start=1):
                self.tree.insert('', 'end', values=(index, row[1], row[0], row[2]))  # Hiển thị kết quả tìm kiếm
        except Exception as e:
            messagebox.showerror("Lỗi tìm kiếm", "Không tìm thấy!")        
    # Hàm delete_student
    def delete_student(self):
        student_id = self.student_delete_entry.get()  # Lấy MSSV từ ô nhập liệu
        if not student_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã sinh viên để xóa!")
            return

        # Xác nhận xóa sinh viên
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sinh viên có mã {student_id}?")
        if confirm:
            try:
                # Truy vấn xóa sinh viên khỏi cơ sở dữ liệu
                query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
                self.database.cur.execute(query, (student_id,))
                self.database.conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu

                messagebox.showinfo("Thành công", f"Sinh viên có mã {student_id} đã được xóa thành công!")

                # Cập nhật lại bảng dữ liệu
                self.load_data()

                # Xóa dữ liệu trong các trường nhập liệu
                self.student_id_entry.delete(0, tk.END)
                self.student_name_entry.delete(0, tk.END)
                self.student_major_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Lỗi xóa dữ liệu", f"Lỗi khi xóa sinh viên: {e}")        
    # Thêm sinh viên
    def insert_student(self):
        student_id = self.student_id_entry.get()
        student_name = self.student_name_entry.get()
        student_major = self.student_major_entry.get()

        if not student_id or not student_name or not student_major:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin sinh viên!")
            return
        
        try:
            # Truy vấn để chèn dữ liệu vào bảng sinh viên
            query = sql.SQL("INSERT INTO {} (name, mssv,  major) VALUES (%s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(query, (student_id, student_name, student_major))
            self.database.conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu

            messagebox.showinfo("Thành công", "Dữ liệu sinh viên đã được thêm thành công!")
            
            # Xóa các trường nhập liệu để tiếp tục thêm sinh viên mới
            self.student_id_entry.delete(0, tk.END)
            self.student_name_entry.delete(0, tk.END)
            self.student_major_entry.delete(0, tk.END)

            # Cập nhật lại bảng dữ liệu
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi chèn dữ liệu", f"Mã môn học đã tồn tại! Vui lòng nhập mã khác.")
    
    # Tab About
    def about_tab(self, tab):
        lable_title = tk.Label(tab, text="DESIGN BY KIM NGOC", font=("Arial", 10, "bold"), fg="#033E8C")
        lable_title.pack(pady=10)
if __name__ == '__main__':
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
