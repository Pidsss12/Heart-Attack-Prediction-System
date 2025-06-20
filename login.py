import tkinter as tk
from tkinter import messagebox
import os

def show_login():
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("350x250")
    login_win.resizable(False, False)

    def register():
        reg_win = tk.Toplevel(login_win)
        reg_win.title("Register")
        reg_win.geometry("350x250")
        reg_win.resizable(False, False)

        tk.Label(reg_win, text="Username:").place(x=40, y=40)
        tk.Label(reg_win, text="Password:").place(x=40, y=80)

        reg_username = tk.StringVar()
        reg_password = tk.StringVar()

        tk.Entry(reg_win, textvariable=reg_username).place(x=120, y=40)
        tk.Entry(reg_win, textvariable=reg_password, show="*").place(x=120, y=80)

        def save_user():
            user = reg_username.get()
            pwd = reg_password.get()
            if user and pwd:
                with open("users.txt", "a") as f:
                    f.write(f"{user},{pwd}\n")
                tk.messagebox.showinfo("Sukses", "Registrasi berhasil!")
                reg_win.destroy()
            else:
                tk.messagebox.showerror("Error", "Username dan password harus diisi!")

        tk.Button(reg_win, text="Register", command=save_user, width=10).place(x=120, y=120)

    tk.Label(login_win, text="Username:").place(x=40, y=40)
    tk.Label(login_win, text="Password:").place(x=40, y=80)

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    tk.Entry(login_win, textvariable=username_var).place(x=120, y=40)
    tk.Entry(login_win, textvariable=password_var, show="*").place(x=120, y=80)

    def check_login():
        user = username_var.get()
        pwd = password_var.get()
        found = False
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f:
                for line in f:
                    u, p = line.strip().split(",")
                    if user == u and pwd == p:
                        found = True
                        break
        if found:
            login_win.destroy()
            import main  
        else:
            tk.messagebox.showerror("Login Gagal", "Username atau password salah!")

    tk.Button(login_win, text="Login", command=check_login, width=10).place(x=120, y=120)
    tk.Button(login_win, text="Sign Up", command=register, width=10).place(x=120, y=160)
    login_win.mainloop()

if __name__ == "__main__":
    show_login()