#GIAO DIỆN QUẢN LÝ SINH VIÊN
#KẾT NỐI DATABASE
import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from tkinter import ttk

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QUẢN LÝ SINH VIÊN")

        # Database connection fields
        self.db_name = tk.StringVar(value='mydb210')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='quanlysinhvien')

        # Create login(connect database)
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.LabelFrame(self.root, text="Login", font=("Arial", 12,"bold"),fg="#EC2A43")
        self.login_frame.grid(row=0, column=0, padx=10, pady=10, sticky="W",)

        tk.Label(self.login_frame, text="User:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="W")
        tk.Entry(self.login_frame, textvariable=self.user, font=("Arial", 10)).grid(row=1, column=1, padx=5, pady=5, sticky="W")

        tk.Label(self.login_frame, text="Password:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="W")
        tk.Entry(self.login_frame, textvariable=self.password, show="*", font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=5, sticky="W")

        tk.Button(self.login_frame, text="Login", command=self.connect_db, font=("Arial", 10),bg="#FFDB59").grid(row=5, column=0, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.login_frame.grid_forget()  # Hide login frame after success
            self.create_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def create_main_screen(self):
        lable_title = tk.Label(self.root, text="QUẢN LÝ SINH VIÊN", font=("Arial", 20, "bold"), fg="#033E8C")
        lable_title.grid(row=0, column=0, columnspan=2)

        # Query section
        query_frame = tk.LabelFrame(self.root, text="Load Data", width=200, font=("Arial", 12, "bold"), fg="#EC2A43")
        query_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        tk.Label(query_frame, text="Nhập tên bảng:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name, font=("Arial", 10)).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Load Data", command=self.load_data, font=("Arial", 10),bg="#FFDB59").grid(row=0, column=2 , columnspan=2, padx=5, pady=5)
        
        lable_titletable = tk.Label(self.root, text="BẢNG THÔNG TIN SINH VIÊN", font=("Arial", 12, "bold"), fg="#08ad56")
        lable_titletable.grid(row=2, column=0, sticky='w')
        
        # Data display table
        self.tree = ttk.Treeview(self.root, columns=('STT', 'MSSV', 'HỌ VÀ TÊN', 'NGÀNH HỌC'), show='headings', height=10)
        self.tree.grid(columnspan=2)
        
        self.tree.column('STT', width=80,) 
        self.tree.column('MSSV', width=120)
        self.tree.column('HỌ VÀ TÊN', width=270) 
        self.tree.column('NGÀNH HỌC', width=230) 

        # Set heading name
        self.tree.heading('STT', text='STT')
        self.tree.heading('MSSV', text='MSSV')
        self.tree.heading('HỌ VÀ TÊN', text='HỌ VÀ TÊN')
        self.tree.heading('NGÀNH HỌC', text='NGÀNH HỌC')
    
        self.tree.grid(row=3, column=0, padx=5, pady=5, sticky='w')

        # Insert section
        insert_frame = tk.LabelFrame(self.root, text="Insert Data", font=("Arial", 12, "bold"), fg="#EC2A43")
        insert_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()
        self.column3 = tk.StringVar()

        tk.Label(insert_frame, text="MSSV:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1, width=80, font=("Arial", 10)).grid(row=0, column=1,padx=5, pady=5)

        tk.Label(insert_frame, text="HỌ VÀ TÊN:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2, width=80, font=("Arial", 10)).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="NGÀNH HỌC:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column3, width=80, font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data, width=30, font=("Arial", 10),bg="#FFDB59").grid(row=3, column=0, columnspan=2, pady=10)

        # Search section
        search_frame = tk.LabelFrame(self.root, text="Search Student", font=("Arial", 12, "bold"), fg="#EC2A43")
        search_frame.grid(row=1, column=0, sticky='e', padx=(340,0))

        self.search_value = tk.StringVar()

        tk.Label(search_frame, text="Nhập tên SV:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_value, font=("Arial", 10)).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(search_frame, text="Search", command=self.search_data, font=("Arial", 10),bg="#FFDB59").grid(row=0, column=2, padx=5, pady=5)

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Clear previous data
            for index, row in enumerate(rows, start=1):
                self.tree.insert('', 'end', values=(index, row[1], row[0], row[2]))  # Assumes columns are [name, mssv, major]
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (name, mssv, major) VALUES (%s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get(), self.column3.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def search_data(self):
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(search_query, (self.search_value.get(),))
            result = self.cur.fetchone()
            self.tree.delete(*self.tree.get_children()) 
            if result:
                self.tree.insert('', 'end', values=(1, result[1], result[0], result[2]))  
                # messagebox.showinfo("No Result", "Không tìm thấy sinh viên.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
