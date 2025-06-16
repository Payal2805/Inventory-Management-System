from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib       # pip install smtplib
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed By Payal ")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        self.otp=""

        # ===========================
        self.var_employee_id=StringVar()
        self.var_password=StringVar()


        # Phone Image
        self.phone_image=Image.open("Images\images8.png",)
        self.phone_image=self.phone_image.resize((500,680),Image.ANTIALIAS)
        self.phone_image=ImageTk.PhotoImage(self.phone_image)

        lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=10)

        # Login Frame
        login_frame=Frame(self.root,bd=4,relief=RIDGE ,bg="white")
        login_frame.place(x=730,y=70,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",18),bg="white",fg="#767171").place(x=50,y=100)
        txt_user=Entry(login_frame,textvariable=self.var_employee_id,font=("times new roman",18),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password ",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.var_password,show="*",font=("times new roman",18),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=153,y=355)

        but_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",activebackground="white",fg="#00759E",activeforeground="#00759E",bd=0,cursor="hand2").place(x=100,y=390)

        # Frame 2
        register_frame=Frame(self.root,bd=4,relief=RIDGE ,bg="white")
        register_frame.place(x=730,y=550,width=350,height=60)

        lbl_reg=Label(register_frame,text="Inventory Managment System",font=("times new roman",18),bg="white").place(x=0,y=15,relwidth=1)
        
        
        
        # Animation  Images

        #self.im1=ImageTk.PhotoImage(file="Images/images10.jpg")
        #self.im2=ImageTk.PhotoImage(file="Images/images11.jpg")
        #self.im3=ImageTk.PhotoImage(file="Images/images12.png")

        self.im1=Image.open("Images\images10.jpg",)
        self.im1=self.im1.resize((270,550),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.im2=Image.open("Images\images11.jpg",)
        self.im2=self.im2.resize((270,550),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.im3=Image.open("Images\images12.png",)
        self.im3=self.im3.resize((270,550),Image.ANTIALIAS)
        self.im3=ImageTk.PhotoImage(self.im3)

        self.lbl_change_image=Label(self.root,bg="black")
        self.lbl_change_image.place(x=380,y=67,width=275,height=555)
        self.animate()
        

    #============================================================================================================

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    def login(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_employee_id.get()=="" or self.var_password.get()=="":
                messagebox.showerror("Error","All Fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.var_employee_id.get(),self.var_password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid Username/Password",parent=self.root)
                else:
                    #print(user)
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashbord.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_employee_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=? ",(self.var_employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID, Try again",parent=self.root)
                else:
                    # =======Forget Window ========
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()         
                    self.var_conf_pass=StringVar()

                    # call send_email_function()
                    chk=self.send_email(email[0])
                    if chk =='f':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                        
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("Reset Password")
                        self.forget_win.geometry("350x460+730+70")     #login_frame.place(x=730,y=70,width=350,height=460)
                        self.forget_win.config(bg="white",bd=7,relief=RIDGE)
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Forget Password",font=("Elephant",25,"bold"),bg="white").place(x=0,y=30,relwidth=1)

                        lbl_reset=Label(self.forget_win,text="Enter OTP Sent on Registered Email",font=("Andalus",14),bg="white",fg="#767171").place(x=20,y=100)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",18),bg="#ECECEC").place(x=20,y=140,width=250)

                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=100,y=180,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("Anadalus",15),bg="white",fg="#767171").place(x=20,y=225)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",18),bg="#ECECEC").place(x=20,y=255,width=250,height=30)

                        lbl_conf_pass=Label(self.forget_win,text="Confirm Password",font=("Anadalus",15),bg="white",fg="#767171").place(x=20,y=300)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",18),bg="#ECECEC").place(x=20,y=330,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2")
                        self.btn_update.place(x=20,y=380,width=250,height=35)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!= self.var_conf_pass.get():
            messagebox.showerror("Error","New password and Confirm password should be same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r"ims.db")
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.var_employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password Updated Sucessfully",parent=self.forget_win)
                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, Try again",parent=self.forget_win)

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_= email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(str(time.strftime("%H%S%M")))+int(str(time.strftime("%S")))
        #print(self.otp)
        
        subj="IMS-Reset Password OTP"
        msg=f"Dear Sir/Madam,\n\nYour Reset OTP is{str(self.otp)}.\n\nWith Regards, \nIMS Team"
        msg="Subject:{}\n\n{}".format(subj,msg)

        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'  

    











root=Tk()
obj=Login_System(root)
root.mainloop()