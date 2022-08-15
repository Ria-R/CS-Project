import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector as sq
import datetime
import time
import winsound
import schedule
    
root = tk.Tk()
root.title('To-Do List')
root.geometry("400x250+500+300")
root.configure(bg='white')
style = ttk.Style()
style.configure("TButton",foreground="orchid4", background="black")
   
  
    
conn = sq.connect(host = 'localhost', user= 'root', password = '' )
cur = conn.cursor()

r2 = cur.execute('use project;')


cur.execute('create table if not exists tasks(todo varchar(100), dateoftask DATETIME NOT NULL DEFAULT(current_timestamp()))')
#cur.execute('alter table tasks add category varchar(100);')
   
task = []
    #------------------------------- Functions--------------------------------
def addTask():
    word = e1.get()
    if len(word)==0:
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        task.append(word)
        cur.execute("insert into tasks (todo)values ('%s')",(word))
        conn.commit()
        listUpdate()
        e1.delete(0,'end')
        
        
'''
def addCategory(): # block may show an indentation error
        wo = e3.get()
        if len(wo) == 0:
            messagebox.showinfo('Empty Entry', 'Enter category name')
        else:
            #line for appending into list
            cur.execute("insert into tasks (category) values (%s)", (wo)) #column needs to be created in table
            listUpdate() #function needs to be modified
            e3.delete(0,'end') #index may change based on list nesting
            '''

def scheduler():
    schedule.every().day.at(answer).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)




def Habitpicker():
    try:
        global uniq
        uniq= t.get(t.curselection())
        print (uniq)
        messagebox.showinfo('Habits','Setting habit for {}'.format(uniq))
        global answer
        answer = simpledialog.askstring("Habits", "Enter time of reminder in 00:00 format",parent=root)
        print(answer)
        scheduler()
        
        
    except:
         messagebox.showinfo('Habits','Please Select Task Item For Building Habits')

def job():
    messagebox.showinfo('Habits', 'It is time to work on {}!'.format(uniq))

            
    
def listUpdate():
    clearList()
    for i in task:
        t.insert('end', i)
    
def delOne():
    try:
        val = t.get(t.curselection())
        if val in task:
            task.remove(val)
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
    except:
         messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

def pomodoro():
          while True:
    # show take break dialog
            show_break_dialog()
    # wait for 20 minutes
            time.sleep(WAIT_TIME)
            
            
        
def deleteAll():
       mb = messagebox.askyesno('Delete All','Are you sure?')
       if mb==True:
            while(len(task)!=0):
                task.pop()
            cur.execute('delete from tasks')
            listUpdate()

def num_tasks():
    num_tasks = len(task)
    
    msg = "There are {} tasks in the list".format(num_tasks)
    l6["text"]=msg

def sort_list_up():
    task.sort()
    listUpdate()
    
def sort_list_down():
    task.sort()
    task.reverse()
    listUpdate()
    
def clearList():
        t.delete(0,'end')
    
def bye():
        print(task)
        root.destroy()
    
def retrieveDB():
        while(len(task)!=0):
            task.pop()
            cur.execute('select todo from tasks')
            x = cur.fetchone()
        #for row in x:
            task.append(x[0])



# define break and wait timings in seconds
BREAK_TIME = 300
WAIT_TIME = 1500

BREAK_TIME_TEST = 5
WAIT_TIME_TEST = 10

# dialog constants
break_dialog_title = "Break Time.."


def countdown(count, label, root):

    label['text'] = " Take a break for : " + str(count) + " sec"

    if count > 0:
        root.after(1000, countdown, count - 1, label, root)
    else:
        root.destroy()


def show_break_dialog():

    root = tk.Tk()
    root.lift()
    root.attributes('-topmost', True)
    root.resizable(0, 0)

    root.title(break_dialog_title)
    label = tk.Label(root, font=("Helvetica", 16), pady=25)
    label.pack()
    Button(root, text="CANCEL", font=("Helvetica", 16), command=root.destroy).pack()

    countdown(BREAK_TIME, label, root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("350x150+%d+%d" % (screen_width / 2 - 275, screen_height / 2 - 125))

    root.mainloop()



    

          
    #------------------------------- Functions-------------------------------- 


l1 = ttk.Label(root, text = 'To-Do List')
l2 = ttk.Label(root, text='Enter task title: ')
e1 = ttk.Entry(root, width=21)
t = tk.Listbox(root, height=11, selectmode='SINGLE')
b1 = ttk.Button(root, text='Add task', width=20,command=addTask)
b2 = ttk.Button(root, text='Delete', width=20, command=delOne)
b3 = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
b6 = ttk.Button(root, text='Number of tasks', width=20, command=num_tasks)
l6 = ttk.Label(root, width=30)
b7 = ttk.Button(root, text='Sort in Ascending', width=20, command=sort_list_up)
b8 = ttk.Button(root, text='Sort in Descending', width=20, command=sort_list_down)
b4 = ttk.Button(root, text='Exit', width=20, command=bye)
b5 = ttk.Button(root, text ='Pomodoro timer',width = 20, command = pomodoro) #function needs to be added
b6 = ttk.Button(root, text ='Habit builder',width = 20, command = Habitpicker)

    
retrieveDB()
listUpdate()

    
    #Place geometry
l2.place(x=50, y=50)
e1.place(x=50, y=80)
b1.place(x=50, y=110)
b2.place(x=50, y=140)
b3.place(x=50, y=170)
b6.place(x=50, y=200)
l6.place(x=220, y=80)
b7.place(x=50, y=230)
b8.place(x=50, y=260)
b4.place(x=50, y =290)
b5.place(x=50, y=320)
b6.place(x = 50, y = 350)
l1.place(x=50, y=20)
t.place(x=220, y = 110)
root.mainloop()
    
conn.commit()
cur.close()


    





    
