import subprocess
import tkinter as tk
from tkinter import filedialog,messagebox
import os
gui = tk.Tk()

def package():
    global subto
    if packfilepath.get() == '':
        messagebox.showerror('错误！','部分打*的项目还没有填写。请检查后重试。')
    else:
        subto = subprocess.Popen('python exepackagemain.py',text=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,encoding='utf-8',stderr=subprocess.STDOUT)
        args = [packfilepath.get(),savefilepath.get(),str(issimple.get()),str(onkey.get()),key.get(),str(ondebug.get()),str(iswindow.get()),str(onicon.get()),iconfilepath.get()]
        subto.stdin.write('|'.join(args))#此处换行一次就是一个INPUT
        subto.stdin.close()#向子进程输入信息
        while subto.poll() is None:
            line = subto.stdout.readline()
            line = line.strip()
            if line:
                terminal.insert(tk.END,line + '\n')#追踪程序执行
            if subto.returncode == 0:
                terminal.insert(tk.END,'程序执行成功，可在您选定的目录里查看dist文件夹下文件。\n')
            else:
                errlog = {1:'无法安装pyinstaller库，请检查您的pip配置。',2:'在指令生成/运行中出现问题。'}
                if subto.returncode == 1:
                    terminal.insert(tk.END,'程序执行失败，错误码：' + str(subto.returncode) + '，错误原因：' + errlog[subto.returncode])
                    with open('errorlog.txt','a',encoding='utf-8') as f:
                        f.write('ErrorWhileExecuting[' + str(subto.returncode) + '] Reason:' + errlog[subto.returncode])
def getpackagefile():#获取文件路径
    topackfile = filedialog.askopenfilename(title='请选择文件',filetypes=[('Python程序','.py')])
    if topackfile != '':
        packfilepath.set(topackfile)
def savepackagefile():#获取文件路径
    topackfile = filedialog.askdirectory(title='请选择输出文件路径')
    if topackfile != '':
        savefilepath.set(topackfile)
def getdisabledofkey():
    if onkey.get():
        keyinput['state'] = 'normal'
    else:
        keyinput['state'] = 'disabled'
def geticonfile():#获取文件路径
    toiconfile = filedialog.askopenfilename(title='请选择图标',filetypes=[('icon图标','.py')])
    if toiconfile != '':
        iconfilepath.set(toiconfile)
def getdisabledoficon():
    if onicon.get():
        iconload['state'] = 'normal'
        iconloadbutt['state'] = 'normal'
    else:
        iconload['state'] = 'disabled'
        iconloadbutt['state'] = 'disabled'
packfilepath = tk.StringVar()
packfilepath.set('')
savefilepath = tk.StringVar()
savefilepath.set('')
gui.geometry('500x500')
gui.title('Python打包exe')
tk.Label(gui,text='Python打包exe',background='orange',font=('华文细黑',22,'bold')).pack(fill='x')
#第一步：选择文件路径
step1 = tk.Frame(gui,relief='raised',borderwidth=2)
fileload = tk.Frame(step1,relief='groove',borderwidth=2)
tk.Label(fileload,text='选择要打包的.py文件路径*',font=('微软雅黑',10)).pack(side='left')
tk.Entry(fileload,width=40,textvariable=packfilepath).pack(side='left')
tk.Button(fileload,text='选择……',command=getpackagefile,font=('微软雅黑',8)).pack(side='left')

fileload.pack(anchor='w')
step1.pack(anchor='w')
#第二步：指定文件参数
step2 = tk.Frame(gui,relief='raised',borderwidth=2)
tk.Label(step2,text='打包文件附带的参数',font=('华文细黑',12,'bold')).pack(fill='x')
line1 = tk.Frame(step2)

simp = tk.Frame(line1,relief='groove',borderwidth=2)
issimple = tk.BooleanVar()
tk.Radiobutton(simp,text='单文件',value=True,variable=issimple).pack(side='left')
tk.Radiobutton(simp,text='多文件',value=False,variable=issimple).pack(side='left')
simp.pack(side='left')

key = tk.StringVar()
key.set('')
onkey = tk.BooleanVar()
onkey.set(False)
seckey = tk.Frame(line1,relief='groove',borderwidth=2)
tk.Checkbutton(seckey,text='加密打包',font=('微软雅黑',10),command=getdisabledofkey,onvalue=True,offvalue=False,variable=onkey).pack(side='left')
keyinput = tk.Entry(seckey,textvariable=key,font=('微软雅黑',10),state='disabled')
keyinput.pack(side='left')
seckey.pack(side='left')

ondebug = tk.BooleanVar()
debug = tk.Frame(line1,relief='groove',borderwidth=2)
tk.Checkbutton(debug,text='生成调试文件',font=('微软雅黑',10),onvalue=True,offvalue=False,variable=ondebug).pack(side='left')
debug.pack(side='left',fill='x')

line1.pack(anchor='w')

line2 = tk.Frame(step2)

window = tk.Frame(line2,relief='groove',borderwidth=2)
iswindow = tk.BooleanVar()
tk.Radiobutton(window,text='有控制台',value=True,variable=iswindow).pack(side='left')
tk.Radiobutton(window,text='无控制台',value=False,variable=iswindow).pack(side='left')
window.pack(side='left')

line2.pack(anchor='w')

line3 = tk.Frame(step2)

onicon = tk.BooleanVar()
onicon.set(False)
iconfilepath = tk.StringVar()
iconfilepath.set('')
icon = tk.Frame(line3,relief='groove',borderwidth=2)
tk.Checkbutton(icon,text='使用自定义图标',font=('微软雅黑',10),command=getdisabledoficon,onvalue=True,offvalue=False,variable=onicon).pack(side='left')
tk.Label(icon,text='选择.ico文件路径',font=('微软雅黑',10)).pack(side='left')
iconload = tk.Entry(icon,width=30,textvariable=iconfilepath,state='disabled')
iconload.pack(side='left')
iconloadbutt = tk.Button(icon,text='选择……',command=geticonfile,font=('微软雅黑',8),state='disabled')
iconloadbutt.pack(side='left')
icon.pack(side='left')

line3.pack(anchor='w')
step2.pack(anchor='w')

tk.Button(gui,text='开始打包（所耗时间约15秒，请耐心等待）',background='green',activebackground='purple',foreground='white',font=('华文宋体',12,'bold'),command=package).pack(fill='x')
terminal = tk.Text(gui,font=('Consolas',10))
terminal.pack(fill='both')
gui.mainloop()