from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from bicepscurl import *
from lunges import *
from pushups import *
from squats import *


#---------------------------------------------------------------Login Function --------------------------------------
def clear():
	userentry.delete(0,END)
	passentry.delete(0,END)

def close():
	win.destroy()	


def login():
	if user_name.get()=="" or password.get()=="":
		messagebox.showerror("Error","Enter User Name And Password",parent=win)	
	else:
		try:
			con = pymysql.connect(host="localhost",user="root",password="123456",database="posetrainer")
			cur = con.cursor()

			cur.execute("select * from user where username=%s and password = %s",(user_name.get(),password.get()))
			row = cur.fetchone()

			if row==None:
				messagebox.showerror("Error" , "Invalid User Name And Password", parent = win)

			else:
				messagebox.showinfo("Success" , "Successfully Login" , parent = win)
				close()
				dashboard()
			con.close()
		except Exception as es:
			messagebox.showerror("Error" , f"Error Dui to : {str(es)}", parent = win)

#---------------------------------------------------------------End Login Function ---------------------------------

#---------------------------------------------------- DeshBoard Panel -----------------------------------------
def dashboard():

	des = Tk()
	des.title("Pose Trainner Dashboard")	
	des.maxsize(width=800 ,  height=500)
	des.minsize(width=800 ,  height=500)		

		#heading label {user_name.get()}
	heading = Label(des , text = f"Samad" , font = 'Verdana 20 bold')
	heading.place(x=10 , y=10)

	heading = Label(des , text = f"Choose Your Excercise" , font = 'Verdana 20 bold')
	heading.place(x=220 , y=100)

	
	bcurl = Button(des, text= "Biceps Curl",height=2, width=50, command=bicepscurl)
	bcurl.place(x=220, y=170)

	pushup = Button(des, text= "Standing Knee Raise",height=2, width=50, command=kneeraise)
	pushup.place(x=220, y=240)

	squat = Button(des, text= "Squat",height=2, width=50, command=squats)
	squat.place(x=220, y=310)

	
	lunge = Button(des, text= "Lunges",height=2, width=50, command=lunges)
	lunge.place(x=220, y=380)



					
#-----------------------------------------------------End Deshboard Panel -------------------------------------


#----------------------------------------------------------- Signup Window --------------------------------------------------

def signup():
	# signup database connect 
	def action():
		if full_name.get()=="" or email.get()=="" or user_name.get()=="" or password.get()=="" or very_pass.get()=="":
			messagebox.showerror("Error" , "All Fields Are Required" , parent = winsignup)
		elif password.get() != very_pass.get():
			messagebox.showerror("Error" , "Password & Confirm Password Should Be Same" , parent = winsignup)
		else:
			try:
				con = pymysql.connect(host="localhost",user="root",password="123456",database="posetrainer")
				cur = con.cursor()
				cur.execute("select * from user where username=%s",user_name.get())
				row = cur.fetchone()
				if row!=None:
					messagebox.showerror("Error" , "User Name Already Exits", parent = winsignup)
				else:
					cur.execute("insert into user(fullname,username,email,password) values(%s,%s,%s,%s)",
						(
						full_name.get(),
						user_name.get(),
						email.get(),
						password.get()
						))
					con.commit()
					con.close()
					messagebox.showinfo("Success" , "Ragistration Successfull" , parent = winsignup)
					clear()
					switch()
				
			except Exception as es:
				messagebox.showerror("Error" , f"Error Dui to : {str(es)}", parent = winsignup)

	# close signup function			
	def switch():
		winsignup.destroy()

	# clear data function
	def clear():
		full_name.delete(0,END)
		email.delete(0,END)
		user_name.delete(0,END)
		password.delete(0,END)
		very_pass.delete(0,END)


	# start Signup Window	

	winsignup = Tk()
	winsignup.title("Docter Appointment App")
	winsignup.maxsize(width=500 ,  height=600)
	winsignup.minsize(width=500 ,  height=600)


	#heading label
	heading = Label(winsignup , text = "Signup" , font = 'Verdana 20 bold')
	heading.place(x=80 , y=60)

	# form data label
	full_name = Label(winsignup, text= "Full Name :" , font='Verdana 10 bold')
	full_name.place(x=80,y=133)

	email = Label(winsignup, text= "Email Id" , font='Verdana 10 bold')
	email.place(x=80,y=178)

	user_name = Label(winsignup, text= "User Name :" , font='Verdana 10 bold')
	user_name.place(x=80,y=223)

	password = Label(winsignup, text= "Password :" , font='Verdana 10 bold')
	password.place(x=80,y=268)

	very_pass = Label(winsignup, text= "Verify Password:" , font='Verdana 10 bold')
	very_pass.place(x=80,y=313)


	# Entry Box ------------------------------------------------------------------

	full_name = StringVar()
	email = StringVar()
	user_name = StringVar()
	password = StringVar()
	very_pass = StringVar()


	full_name = Entry(winsignup, width=40 , textvariable = full_name)
	full_name.place(x=200 , y=133)


	
	email = Entry(winsignup, width=40 , textvariable = email)
	email.place(x=200 , y=178)

	
	user_name = Entry(winsignup, width=40, textvariable=user_name)
	user_name.place(x=200 , y=223)
	
	password = Entry(winsignup, width=40 , textvariable = password)
	password.place(x=200 , y=268)

	
	very_pass = Entry(winsignup, width=38,textvariable = very_pass)
	very_pass.place(x=211 , y=313)

	# button login and clear

	btn_signup = Button(winsignup, text = "Signup" ,font='Verdana 10 bold', command = action)
	btn_signup.place(x=200, y=413)


	btn_login = Button(winsignup, text = "Clear" ,font='Verdana 10 bold' , command = clear)
	btn_login.place(x=280, y=413)


	sign_up_btn = Button(winsignup , text="Switch To Login" , command = switch )
	sign_up_btn.place(x=350 , y =20)


	winsignup.mainloop()
#---------------------------------------------------------------------------End Singup Window-----------------------------------	


	

#------------------------------------------------------------ Login Window -----------------------------------------

win = Tk()

# app title
win.title("Docter Appointment App")

# window size
win.maxsize(width=500 ,  height=500)
win.minsize(width=500 ,  height=500)


#heading label
heading = Label(win , text = "Login" , font = 'Verdana 25 bold')
heading.place(x=80 , y=150)

username = Label(win, text= "User Name :" , font='Verdana 10 bold')
username.place(x=80,y=220)

userpass = Label(win, text= "Password :" , font='Verdana 10 bold')
userpass.place(x=80,y=260)

# Entry Box
user_name = StringVar()
password = StringVar()
	
userentry = Entry(win, width=40 , textvariable = user_name)
userentry.focus()
userentry.place(x=200 , y=223)

passentry = Entry(win, width=40, show="*" ,textvariable = password)
passentry.place(x=200 , y=260)


# button login and clear

btn_login = Button(win, text = "Login" ,font='Verdana 10 bold',command = login)
btn_login.place(x=200, y=293)


btn_login = Button(win, text = "Clear" ,font='Verdana 10 bold', command = clear)
btn_login.place(x=260, y=293)

# signup button

sign_up_btn = Button(win , text="Switch To Sign up" , command = signup )
sign_up_btn.place(x=350 , y =20)


win.mainloop()

#-------------------------------------------------------------------------- End Login Window ---------------------------------------------------