from tkinter import *
from datetime import date
from tkinter.ttk import Combobox
import datetime
import tkinter as tk
import tkinter as ttk
import os
from tkinter import messagebox
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


from backend import *
from MYSQL import *



backgrounds = "#f0ddd5"
framebg = "#62a7ff"
framebg = "#fefbfb"
framefg = "#0e5365"


root = Tk()
root.title("Heart Attack Prediction System")
root.geometry("1450x730")
root.resizable(True, True)
root.config(bg=backgrounds) 



def analysis():
    global prediction
    try:
        
        dob_value = Dob.get()
        if "/" in dob_value:
            year = int(dob_value.split("/")[-1])
        else:
            year = int(dob_value)
        A = today.year - year
    except Exception:
        messagebox.showerror("missing", "Please enter valid birth year!")
        return

    try:
        B = selection()
    except Exception:
        messagebox.showerror("missing", "Please select gender!!")
        return

    try:
        F = selection2()
    except Exception:
        messagebox.showerror("missing", "Please select fbs!!")
        return

    try:
        I = selection3()
    except Exception:
        messagebox.showerror("missing", "Please select exang!!")
        return

    try:
        C = int(selection_cp())
    except Exception:
        messagebox.showerror("missing", "Please select cp!!")
        return

    try:
        G = int(selection_restecg())
    except Exception:
        messagebox.showerror("missing", "Please select cg!!")
        return

    try:
        K = int(selection_slope())
    except Exception:
        messagebox.showerror("missing", "Please select slope!!")
        return

    try:
        L = int(ca_combobox.get())
    except Exception:
        messagebox.showerror("missing", "Please select ca!!")
        return

    try:
        M = int(selection_thal())
    except Exception:
        messagebox.showerror("missing", "Please select thal!!")
        return

    try:
        D = int(trestbps.get())
        E = int(chol.get())
        H = int(thalach.get())
        J = int(oldpeak.get())
    except Exception:
        messagebox.showerror("missing data", "Few missing data entry!!")
        return

    print("A is ", A)
    print("B is ", B)
    print("C is ", C)
    print("D is ", D)
    print("E is ", E)
    print("F is ", F)
    print("G is ", G)
    print("H is ", H)
    print("I is ", I)
    print("J is ", J)
    print("K is ", K)
    print("L is ", L)
    print("M is ", M)
    
    
    ##### grafik pertama
    f = Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.plot(["sex", "fbs", "exang"], [B, F, I])
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    canvas._tkcanvas.place(width=250, height=250, x=600, y=240)
    
    ##### grafik kedua
    f2 = Figure(figsize=(5, 5), dpi=100)
    a2 = f2.add_subplot(111)
    a2.plot(["age", "testbps", "chol", "thalach"],[A, D, E, H])
    canvas2 = FigureCanvasTkAgg(f2)
    canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    canvas2._tkcanvas.place(width=250, height=250, x=860, y=240)
    
    ##### grafik ketiga
    f3 = Figure(figsize=(5, 5), dpi=100)
    a3 = f3.add_subplot(111)
    a3.plot(["oldpeak", "restcg", "cp"], [J, G, C])
    canvas3 = FigureCanvasTkAgg(f3)
    canvas3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    canvas3._tkcanvas.place(width=250, height=250, x=600, y=470)
    
    ##### grafik keempat
    f4 = Figure(figsize=(5, 5), dpi=100)
    a4 = f4.add_subplot(111)
    a4.plot(["slope", "ca", "thal"], [K, L, M])
    canvas4 = FigureCanvasTkAgg(f4)
    canvas4.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    canvas4._tkcanvas.place(width=250, height=250, x=860, y=470)
    
    
    #### input data
    input_data = (A, B, C, D, E, F, G, H, I, J, K, L, M)
    
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the numpy array as we are predicting for only one instance
    input_data_reshape = input_data_as_numpy_array.reshape(1, -1)
    print("Input ke model:", input_data_reshape)

    prediction = model.predict(input_data_reshape)
    print(prediction[0])

    if prediction[0] == 0:
        print('The Person does not have a Heart disease')
        report_label.config(text=f"Report: {0}", fg="#8dc63f")
        report_1.config(text=f"{name.get()}, you do not have a heart disease")
    else:
        print('The Person has Heart disease')
        report_label.config(text=f"Report: {1}", fg="#ed1c24")
        report_1.config(text=f"{name.get()}, you have a heart disease")



def Info():
    icon_window = Toplevel(root)
    icon_window.title("Info")
    icon_window.geometry("700x600+300+100")

    icon_image = PhotoImage(file="Images/info.png")
    icon_window.iconphoto(False, icon_image)


    Label(icon_window, text="Information Related to dataset", font="robot 19 bold").pack(padx=20, pady=20)


    Label(icon_window, text="age - age in years", font="arial 11").place(x=20, y=100)
    Label(icon_window, text="sex - sex (1 = male; 0 = female)", font="arial 11").place(x=20, y=130)
    Label(icon_window, text="cp - chest pain type (0 = typical angina; 1 = atypical angina; 2 = non-anginal pain; 3 = asymptomatic)", font="arial 11").place(x=20, y=160)
    Label(icon_window, text="trestbps - resting blood pressure (in mm Hg on admission to the hospital) ", font="arial 11").place(x=20, y=190)
    Label(icon_window, text="chol - serum cholestoral in mg/dl", font="arial 11").place(x=20, y=220)
    Label(icon_window, text="fbs - fasting blood sugar > 120 mg/dl (1 = true; 0 = false) ", font="arial 11").place(x=20, y=250)
    Label(icon_window, text="restecg - resting electrocardiographic results (0 = normal; 1 = having ST-T; 2 = hypertrophy) ", font="arial 11").place(x=20, y=280)
    Label(icon_window, text="thalach - maximum heart rate achieved ", font="arial 11").place(x=20, y=310)
    Label(icon_window, text="exang - exercise induced angina (1 = yes; 0 = no) ", font="arial 11").place(x=20, y=340)
    Label(icon_window, text="oldpeak - ST depression induced by exercise relative to rest", font="arial 11").place(x=20, y=370)
    Label(icon_window, text="slope - the slope of the peak exercise ST segment (0 = upsloping; 1 = flat; 2 = downsloping)", font="arial 11").place(x=20, y=400)
    Label(icon_window, text="ca - number of major vessels (0-3) colored by flourosopy ", font="arial 11").place(x=20, y=430)
    Label(icon_window, text="thal - 0 = normal; 1 = fixed defect; 2 = reversable defect ", font="arial 11").place(x=20, y=460)





    icon_window.mainloop()
    
def logout():
    root.destroy()
    

def clear():
    name.set('')    
    Dob.set('')
    trestbps.set('')
    chol.set('')
    thalach.set('')
    oldpeak.set('')
    
def Save():
    B2 = name.get()
    C2 = date_var.get()
    D2 = Dob.get()
    
    today = datetime.date.today()
    E2 = today.year - int(Dob.get())

    try:
        F2 = selection()
    except Exception:
        messagebox.showerror("Missing Data", "Please select Gender!")
        return

    try:
        J2 = selection2()
    except Exception:
        messagebox.showerror("Missing Data", "Please select FBS!")
        return

    try:
        M2 = selection3()
    except Exception:
        messagebox.showerror("Missing Data", "Please select Exang!")
        return

    try:
        G2 = selection_cp()
    except Exception:
        messagebox.showerror("Missing Data", "Please select CP!")
        return

    try:
        K2 = selection_restecg()
    except Exception:
        messagebox.showerror("Missing Data", "Please select Restecg!")
        return

    try:
        O2 = selection_slope()
    except Exception:
        messagebox.showerror("Missing Data", "Please select Slope!")
        return

    try:
        P2= selection_ca()
    except Exception:
        messagebox.showerror("Missing Data", "Please select CA!")
        return

    try:
        Q2 = selection_thal()
    except Exception:
        messagebox.showerror("Missing Data", "Please select Thal!")
        return
    
    H2 = trestbps.get()
    I2 = chol.get()
    L2 = thalach.get()
    N2 = float(oldpeak.get())
    
    print(B2)
    print(C2)
    print(D2)
    print(E2)
    print(F2)
    print(G2)
    print(H2)
    print(I2)
    print(J2)
    print(K2)
    print(L2)
    print(M2)
    print(N2)
    print(O2)
    print(P2)
    print(Q2)
    
    input_data = (
        int(E2), int(F2), int(G2), int(H2), int(I2), int(J2), int(K2), int(L2),
        int(M2), float(N2), int(O2), int(P2), int(Q2)
    )
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshape = input_data_as_numpy_array.reshape(1, -1)
    prediction = model.predict(input_data_reshape)

    Save_Data_MySQL(
        B2, C2, int(D2), int(E2), int(F2), int(G2), int(H2), int(I2), J2,
        int(L2), int(M2), float(N2), int(O2), int(P2), int(Q2), int(prediction[0])
    )

    clear()
    root.destroy()
    os.system("main.py")
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#icon 1
image_icon = PhotoImage(file="images/icon.png")
root.iconphoto(False, image_icon)


#header section 2
logo = PhotoImage(file="images/header.png")
myimage = Label(root, image=logo, bg=backgrounds)
myimage.place(x=0, y=0)



## >>>>> frame 3
Heading_entry = Frame(root, width=800,height=190, bg="#df2d48")
Heading_entry.place(x=600, y=20)

Label(Heading_entry, text="Registrasion No.", font="arial 13", bg="#df2d48",fg=framebg).place(x=30, y=0)
Label(Heading_entry, text="Date :", font="arial 13", bg="#df2d48",fg=framebg).place(x=430, y=0)

Label(Heading_entry, text="Patient Name :", font="arial 13", bg="#df2d48",fg=framebg).place(x=30, y=90)
Label(Heading_entry, text="Birth Year :", font="arial 13", bg="#df2d48",fg=framebg).place(x=430, y=90)


Entry_image = PhotoImage(file="Images/Rounded Rectangle 1.png")
Entry_image2 = PhotoImage(file="Images/Rounded Rectangle 2.png")
Label(Heading_entry, image=Entry_image, bg="#df2d48").place(x=20, y=30)
Label(Heading_entry, image=Entry_image, bg="#df2d48").place(x=430, y=30)

Label(Heading_entry, image=Entry_image2, bg="#df2d48").place(x=20, y=120)
Label(Heading_entry, image=Entry_image2, bg="#df2d48").place(x=430, y=120)

Registration=IntVar()
reg_entry=Entry(Heading_entry, textvariable=Registration, width=30, font="arial 15", bg="#0e5365", fg="white", bd=0)
reg_entry.place(x=30, y=45)


date_var = StringVar()
today = date.today()
d1 = today.strftime("%d/%m/%Y")
date_entry = Entry(Heading_entry, textvariable=date_var, width=15, font="arial 15", bg="#0e5365", fg="white", bd=0)
date_entry.place(x=500, y=45)
date_var.set(d1)

name=StringVar()
name_entry=Entry(Heading_entry, textvariable=name, width=20, font="arial 20", bg="#ededed", fg="#222222", bd=0)
name_entry.place(x=30, y=130)

Dob=StringVar()
dob_entry=Entry(Heading_entry, textvariable=Dob, width=20, font="arial 20", bg="#ededed", fg="#222222", bd=0)
dob_entry.place(x=450, y=130)


############################### Body ##################################################### 4
Detail_entry = Frame(root, width=490,height=260, bg="#dbe0e3", bd=1)
Detail_entry.place(x=30, y=450)

#################radio button#################### 5
Label(Detail_entry, text ="sex:", font="arial 13", bg=framebg,fg=framefg).place(x=10, y=10)
Label(Detail_entry, text ="fbs", font="arial 13", bg=framebg,fg=framefg).place(x=180, y=10)
Label(Detail_entry, text ="exang", font="arial 13", bg=framebg,fg=framefg).place(x=335, y=10)

def selection():
    if gen.get() == 1:
        return 1
    elif gen.get() == 2:
        return 0
    else:
        raise Exception("Gender not selected")

def selection2():
    if fbs.get() == 1:
        return 1
    elif fbs.get() == 2:
        return 0
    else:
        raise Exception("FBS not selected")

def selection3():
    if Exang.get() == 1:
        return 1
    elif Exang.get() == 2:
        return 0
    else:
        raise Exception("Exang not selected")


gen = IntVar()
R1 = Radiobutton(Detail_entry, text='Male', variable=gen, value=1, command=selection)
R2 = Radiobutton(Detail_entry, text='Female', variable=gen, value=2, command=selection)
R1.place(x=43, y=10)
R2.place(x=93, y=10)

fbs = IntVar()
R3 = Radiobutton(Detail_entry, text='True', variable=fbs, value=1, command=selection2)
R4 = Radiobutton(Detail_entry, text='False', variable=fbs, value=2, command=selection2)
R3.place(x=213, y=10)   
R4.place(x=263, y=10)  

Exang = IntVar()
R5 = Radiobutton(Detail_entry, text='Yes', variable=Exang, value=1, command=selection3)
R6 = Radiobutton(Detail_entry, text='No', variable=Exang, value=2, command=selection3)
R5.place(x=387, y=10)
R6.place(x=430, y=10)








########################### Combobox ############################## 6
Label(Detail_entry, text="cp :", font="arial 13", bg=framebg,fg=framefg).place(x=10, y=50)
Label(Detail_entry, text="restecg", font="arial 13", bg=framebg,fg=framefg).place(x=10, y=90)
Label(Detail_entry, text="slope :", font="arial 13", bg=framebg,fg=framefg).place(x=10, y=130)
Label(Detail_entry, text="ca :", font="arial 13", bg=framebg,fg=framefg).place(x=10, y=170)
Label(Detail_entry, text="thal :", font="arial 13", bg=framebg,fg=framefg).place(x=10, y=210)

def selection_cp():
    input = cp_combobox.get()
    if input == "0 = typical angina":
        return 0
    elif input == "1 = atypical angina":
        return 1
    elif input == "2 = non-anginal pain":
        return 2
    elif input == "3 = asymptomatic":
        return 3
    else:
        print(input)

def selection_restecg():
    input = restecg_combobox.get()
    if input == "0 = normal":
        return 0
    elif input == "1 = ST-T wave abnormality":
        return 1
    elif input == "2 = left ventricular hypertrophy":
        return 2
    else:
        print(input)

def selection_slope():
    input = slope_combobox.get()
    if input == "0 = upsloping":
        return 0
    elif input == "1 = flat":
        return 1
    elif input == "2 = downsloping":
        return 2
    else:
        print(input)

def selection_ca():
    input = ca_combobox.get()
    if input == "0":
        return 0
    elif input == "1":
        return 1
    elif input == "2":
        return 2
    elif input == "3":
        return 3
    elif input == "4":
        return 4
    else:
        print(input)

def selection_thal():
    input = thal_combobox.get()
    if input == "0 = normal":
        return 0
    elif input == "1 = fixed defect":
        return 1
    elif input == "2 = reversible defect":
        return 2
    else:
        print(input)




cp_combobox = Combobox(
    Detail_entry,
    values=[
        "0 = typical angina",
        "1 = atypical angina",
        "2 = non-anginal pain",
        "3 = asymptomatic"
    ],
    font="arial 12",
    state="readonly",
    width=14
)
cp_combobox.place(x=50, y=50)


restecg_combobox = Combobox(
    Detail_entry,
    values=[
        "0 = normal",
        "1 = ST-T wave abnormality",
        "2 = left ventricular hypertrophy"
    ],
    font="arial 12",
    state="readonly",
    width=11
)
restecg_combobox.place(x=80, y=90)


slope_combobox = Combobox(
    Detail_entry,
    values=[
        "0 = upsloping",
        "1 = flat",
        "2 = downsloping"
    ],
    font="arial 12",
    state="readonly",
    width=12
)
slope_combobox.place(x=70, y=130)


ca_combobox = Combobox(
    Detail_entry,
    values=[
        "0", "1", "2", "3", "4"
    ],
    font="arial 12",
    state="readonly",
    width=14
)
ca_combobox.place(x=50, y=170)


thal_combobox = Combobox(
    Detail_entry,
    values=[
        "0 = normal",
        "1 = fixed defect",
        "2 = reversible defect"
    ],
    font="arial 12",
    state="readonly",
    width=14
)
thal_combobox.place(x=50, y=210)



Label(Detail_entry, text="Smoking:", font="arial 13", width=7, bg="#dbe0e3", fg="black").place(x=240, y=50)
Label(Detail_entry, text="trestbps", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=90)
Label(Detail_entry, text="chol:", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=130)
Label(Detail_entry, text="thalach", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=170)
Label(Detail_entry, text="oldpeak", font="arial 13", width=7, bg=framebg, fg=framefg).place(x=240, y=210)

trestbps = StringVar()
chol = StringVar()
thalach = StringVar()
oldpeak = StringVar()


trestbps_entry = Entry(Detail_entry, textvariable=trestbps, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
chol_entry = Entry(Detail_entry, textvariable=chol, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
thalach_entry = Entry(Detail_entry, textvariable=thalach, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
oldpeak_entry = Entry(Detail_entry, textvariable=oldpeak, width=10, font="arial 15", bg="#ededed", fg="#222222", bd=0)
trestbps_entry.place(x=320, y=90)
chol_entry.place(x=320, y=130)
thalach_entry.place(x=320, y=170)
oldpeak_entry.place(x=320, y=210)


square_report_image = PhotoImage(file="images/Report.png")
report_background = Label(root, image=square_report_image, bg=backgrounds)
report_background.place(x=1120, y=340)

report_label = Label(root, font="arial 25 bold", bg="white", fg="#8dc63f")
report_label.place(x=1170, y=550)

report_1 = Label(root, font="arial 10 bold", bg="white")
report_1.place(x=1130, y=610)

graph_image = PhotoImage(file="images/graph.png")
Label(root, image=graph_image).place(x=600, y=270)
Label(root, image=graph_image).place(x=860, y=270)
Label(root, image=graph_image).place(x=600, y=500)
Label(root, image=graph_image).place(x=860, y=500)

Analysis_button = PhotoImage(file="images/Analysis.png")
Button(root, image=Analysis_button, bd=0, bg=backgrounds,cursor='hand2', command=analysis).place(x=1130, y=240)

info_button = PhotoImage(file="images/info.png")
Button(root, image=info_button, bd=0, bg=backgrounds, cursor='hand2', command=Info).place(x=10, y=240)

save_button = PhotoImage(file="images/save.png")
Button(root, image=save_button, bd=0, bg=backgrounds, cursor='hand2', command=Save).place(x=1370, y=250)

button_mode =True
choice = "smoking"
def changemode():
    global button_mode
    global choice
       
    if button_mode:
        choice = "non_smoking"
        mode.config(image=non_smoking_icon, activebackground="white")
        button_mode = False
        
    else:
        choice = "smoking"
        mode.config(image=smoking_icon, activebackground="white")
        button_mode = True
        
    print(choice)

smoking_icon = PhotoImage(file="images/smoker.png")
non_smoking_icon = PhotoImage(file="images/non-smoker.png")

mode = Button(root, image=smoking_icon, bg="#dbe0e3", bd=0, cursor='hand2' , command=changemode)
mode.place(x=350, y=495)

logout_icon = PhotoImage(file="images/logout.png")
logout_button = Button(root, image=logout_icon, bg="#df2d4b", cursor='hand2', bd=0, command=logout)
logout_button.place(x=1390, y=60)

root.mainloop()