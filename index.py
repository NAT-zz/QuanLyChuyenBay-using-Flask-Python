from flask import render_template, request, redirect, session, jsonify
from __init__ import app, CART_KEY, my_login
from admin import*
from models import*
from flask_login import login_user
import utils

@my_login.user_loader
#Bỏ cả đối tượng vào biến current_user
def user_load(user_id):
    return NguoiDung.query.get(user_id)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login_execute():
    username = request.form.get('username')
    password = request.form.get('password')
    #password = str(hashlib.md5(pwd.encode("utf-8")).digest())

    user = NguoiDung.query.filter(NguoiDung.TenDN==username, NguoiDung.MatKhau==password).first()

    if user:
        if user.VaiTro == "A":
            login_user(user)
    return redirect("/admin")

@app.route("/login-user", methods = ["POST", "GET"])
def norlogin_user():
    if not current_user.is_authenticated:
        err_msg = ""
        if request.method == "POST":
            username = request.form.get("username")
            pwd = request.form.get("password")

            user = NguoiDung.query.filter(NguoiDung.TenDN == username, NguoiDung.MatKhau == pwd).first()

            if user:
                login_user(user)
                return redirect(request.args.get("next", "/"))
            else:
                err_msg = "Kiểm tra lại thông tin"

        return render_template("login-user.html", err_msg=err_msg)
    return redirect("/")
    
@app.route("/logout-user")
def normaluser_logout():
    logout_user()
    return redirect("/login-user")

@app.route("/register-user", methods=["POST", "GET"])
def register():
    err_msg = ""
    if request.method == 'POST':
        try:
            password = request.form.get("matkhau")    
            confirm_password = request.form.get("confirmmatkhau")
            if password.strip() == confirm_password.strip():
                data = request.form.copy()
                del data['confirmmatkhau']

                if utils.add_user(**data):
                    return redirect("/login-user")
                else:
                    err_msg = "Kiểm tra lại thông tin/Tên đăng nhập có thể đã tồn tại"
            else:
                err_msg = "Mật khẩu không khớp"
        except:
            err_msg = "Lỗi hệ thống/Vui lòng thử lại"

    return render_template("reg-user.html", err_msg = err_msg)

@app.route("/list-ve")
def list_ve():
    if current_user.VaiTro == "N":
        return render_template("list-ve.html")
@app.route("/ban-ve")
def ban_ve():
    if current_user.VaiTro == "N":
        return render_template("banve.html")
@app.route("/nhan-lich")
def nhan_lich():
    if current_user.VaiTro == "N":
        return render_template("nhanlichchuyenbay.html")
@app.route("/list-khach")
def list_khach():
    if current_user.VaiTro == "N":
        return render_template("list-khachhang.html")

if __name__ == '__main__':
    app.run(debug=True)