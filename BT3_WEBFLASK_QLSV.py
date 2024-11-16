from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
from database import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thêm khóa bảo mật cho session

# Route trang đăng nhập (mặc định)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        user = request.form['user']
        password = request.form['password']
        
        # Tạo kết nối với thông tin từ form
        db = Database(db_name='mydb210', user=user, password=password, host='localhost', port=5432)
        if db.connect():
            # Lưu thông tin đăng nhập trong session
            session['user'] = user
            session['password'] = password
            db.cur.close()  # Đóng cursor
            db.conn.close()  # Đóng kết nối
            
            # Kết nối thành công, chuyển đến trang home
            return redirect(url_for('home'))
        else:
            # Kết nối thất bại, hiển thị thông báo lỗi
            flash("Kết nối không thành công. <br> Vui lòng kiểm tra lại thông tin đăng nhập.", 'error')
    
    return render_template('index.html')

# Trang chính khi kết nối thành công
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Kiểm tra session trước khi truy cập trang home
    if 'user' in session and 'password' in session:
        db = Database(db_name='mydb210', user=session['user'], password=session['password'], host='localhost', port=5432)
        search_query = request.args.get('search_query', '')  # Lấy từ khóa tìm kiếm từ query string
        status_query = request.args.get('status_query', '')  # Lấy trạng thái từ dropdown

        if db.connect():
            # Nếu có từ khóa tìm kiếm hoặc trạng thái tìm kiếm, sử dụng chúng trong câu lệnh SQL
            sql_query = "SELECT * FROM courses WHERE (course_name ILIKE %s OR course_code ILIKE %s)"
            params = [f'%{search_query}%', f'%{search_query}%']

            if status_query:  # Nếu có trạng thái tìm kiếm
                sql_query += " AND status = %s"
                params.append(status_query)

            db.cur.execute(sql_query, tuple(params))
            data = db.cur.fetchall()
            db.cur.close()
            db.conn.close()
            return render_template('home.html', data=data, search_query=search_query, status_query=status_query)

    # Nếu không có thông tin đăng nhập, chuyển về trang đăng nhập
    # flash("Bạn cần đăng nhập để truy cập trang này.", 'error')
    return render_template('index.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        gpa = request.form['gpa']
        status = request.form['status']

        db = Database(db_name='mydb210', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            # Kiểm tra xem mã môn học đã tồn tại chưa
            db.cur.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
            existing_course = db.cur.fetchone()

            if existing_course:
                # Nếu có môn học trùng mã, sử dụng flash để thông báo
                flash('Mã môn học đã tồn tại!', 'danger')
                return redirect(url_for('add_course'))

            # Nếu không trùng, thêm môn học vào cơ sở dữ liệu
            db.cur.execute("INSERT INTO courses (course_code, course_name, gpa, status) VALUES (%s, %s, %s, %s)",
                           (course_code, course_name, gpa, status))
            db.conn.commit()
            db.cur.close()
            db.conn.close()

            # Flash thông báo thành công
            flash('Môn học đã được thêm thành công!', 'success')
            return redirect(url_for('add_course'))

    return render_template('add_course.html')


from flask import flash

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    db = Database(db_name='mydb210', user=session['user'], password=session['password'], host='localhost', port=5432)
    if db.connect():
        db.cur.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
        course = db.cur.fetchone()
        
        if request.method == 'POST':
            course_code = request.form['course_code']
            course_name = request.form['course_name']
            gpa = request.form['gpa']
            status = request.form['status']
            
            db.cur.execute('UPDATE courses SET course_code = %s, course_name = %s, gpa = %s, status = %s WHERE id = %s', 
                           (course_code, course_name, gpa, status, course_id))
            db.conn.commit()
            db.cur.close()
            db.conn.close()
            
            # Thêm thông báo thành công
            flash('Môn học đã được chỉnh sửa thành công.', 'success')
            return render_template('edit_course.html', course=course)
        
    return render_template('edit_course.html', course=course)


# Xóa môn học
@app.route('/delete_course/<int:course_id>', methods=['GET'])
def delete_course(course_id):
    db = Database(db_name='mydb210', user=session['user'], password=session['password'], host='localhost', port=5432)
    if db.connect():
        db.cur.execute('DELETE FROM courses WHERE id = %s', (course_id,))
        db.conn.commit()
        db.cur.close()
        db.conn.close()
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
