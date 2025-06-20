import mysql.connector
from tkinter import messagebox

def Save_Data_MySQL(B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q,):
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # kosongkan password untuk XAMPP
            database='Heart_Data'
        )
        mycursor = mydb.cursor()
        command = """INSERT INTO data
        (name, date, Dob, age, sex, cp, trestbps, chol, fbs, restcg, thalach, exang, oldpeak, slope, ca, thal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q)
        mycursor.execute(command, values)
        mydb.commit()
        mydb.close()
        messagebox.showinfo("Register", "New user added succesfully!")
    except Exception as e:
        messagebox.showerror("Connection", f"Database connection not stablished!\n{e}")