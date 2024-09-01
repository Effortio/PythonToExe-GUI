import os
import subprocess
import sys
from time import sleep
import tkinter as tk
from tkinter import filedialog, messagebox
import threading  #异步

gui = tk.Tk()

subto = terminal = result = None


def package():
    global subto, terminal, result
    overrun = tk.Tk()
    result = tk.Label(overrun,
                      text='运行时的输出',
                      background='purple',
                      font=('华文细黑', 22, 'bold'),
                      foreground='white')
    result.pack(fill='x')
    scroll = tk.Scrollbar(overrun, orient="vertical")

    terminal = tk.Text(overrun,
                       font=('Consolas', 10),
                       yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    terminal.pack(fill='both')
    scroll.config(command=terminal.yview)

    subto = subprocess.Popen('python ' + os.path.dirname(sys.argv[0]) +
                             '/exepackagemain.py',
                             text=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             encoding='utf-8',
                             stderr=subprocess.STDOUT,
                             cwd=savefilepath.get())
    args = [
        packfilepath.get(),
        savefilepath.get(),
        str(issimple.get()),
        str(ondebug.get()),
        str(iswindow.get()),
        str(onicon.get()),
        iconfilepath.get(),
        str(isforcedel.get())
    ]
    subto.stdin.write('|'.join(args))  #此处换行一次就是一个INPUT
    subto.stdin.close()  #向子进程输入信息
    overrun.mainloop()


def getoutput():
    global subto, terminal, result
    while subto is None:
        sleep(0.05)  #等待执行完毕
    while subto.poll() is None:
        try:
            line = subto.stdout.readline()
            line = line.strip()
            if line:
                terminal.insert(tk.END, line + '\n')  #追踪程序执行
        except:
            pass
    if subto.returncode == 0:
        terminal.insert(tk.END, '程序执行成功，可在您选定的目录里查看dist文件夹下文件。\n')
        result["text"] = "运行完成"
        result["bg"] = "green"
    else:
        errlog = {1: '无法安装pyinstaller库，请检查您的pip配置。', 2: '在指令生成/运行中出现问题。'}
        terminal.insert(
            tk.END, '程序执行失败，错误码：' + str(subto.returncode) + '，错误原因：' +
            errlog[subto.returncode])
        result["text"] = "运行失败"
        result["bg"] = "red"


def threadment():
    if packfilepath.get() == '' or savefilepath.get() == '':
        messagebox.showerror('错误！', '部分打*的项目还没有填写。请检查后重试。')
    else:
        th1 = threading.Thread(target=package)
        th1.daemon = True
        th1.start()
        th2 = threading.Thread(target=getoutput)
        th2.daemon = True
        th2.start()


def getpackagefile():  #获取文件路径
    topackfile = filedialog.askopenfilename(title='请选择文件',
                                            filetypes=[('Python程序', '.py')])
    if topackfile != '':
        packfilepath.set(topackfile)


def getpackagefold():  #获取文件目录
    topackdir = filedialog.askdirectory(title='请选择目录')
    if topackdir != '':
        savefilepath.set(topackdir)


def savepackagefile():  #获取文件路径
    topackfile = filedialog.askdirectory(title='请选择输出文件路径')
    if topackfile != '':
        savefilepath.set(topackfile)


def geticonfile():  #获取文件路径
    toiconfile = filedialog.askopenfilename(title='请选择图标',
                                            filetypes=[('icon图标', '.ico')])
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
gui.geometry('500x300')
gui.title('Python打包exe')
tk.Label(gui,
         text='Python打包exe',
         background='orange',
         font=('华文细黑', 22, 'bold')).pack(fill='x')
#第一步：选择文件路径
step1 = tk.Frame(gui, relief='raised', borderwidth=2)
fileload = tk.Frame(step1, relief='groove', borderwidth=2)
tk.Label(fileload, text='选择要打包的.py文件路径*', font=('微软雅黑', 10)).pack(side='left')
tk.Entry(fileload, width=39, textvariable=packfilepath).pack(side='left')
tk.Button(fileload, text='选择……', command=getpackagefile,
          font=('微软雅黑', 8)).pack(side='left')

packin = tk.Frame(step1, relief='groove', borderwidth=2)
tk.Label(packin, text='选择打包到的路径下*', font=('微软雅黑', 10)).pack(side='left')
tk.Entry(packin, width=40, textvariable=savefilepath).pack(side='left')
tk.Button(packin, text='选择……', command=getpackagefold,
          font=('微软雅黑', 8)).pack(side='left')

fileload.pack(anchor='w')
packin.pack(anchor='w')
step1.pack(anchor='w')
#第二步：指定文件参数
step2 = tk.Frame(gui, relief='raised', borderwidth=2)
tk.Label(step2, text='打包文件附带的参数', font=('华文细黑', 12, 'bold')).pack(fill='x')
line1 = tk.Frame(step2)

simp = tk.Frame(line1, relief='groove', borderwidth=2)
issimple = tk.BooleanVar()
tk.Radiobutton(simp, text='单文件', value=True,
               variable=issimple).pack(side='left')
tk.Radiobutton(simp, text='多文件', value=False,
               variable=issimple).pack(side='left')
simp.pack(side='left')

window = tk.Frame(line1, relief='groove', borderwidth=2)
iswindow = tk.BooleanVar()
tk.Radiobutton(window, text='有控制台', value=True,
               variable=iswindow).pack(side='left')
tk.Radiobutton(window, text='无控制台', value=False,
               variable=iswindow).pack(side='left')
window.pack(side='left')

line1.pack(anchor='w')
line2 = tk.Frame(step2)

forcedel = tk.Frame(line2, relief='groove', borderwidth=2)
isforcedel = tk.BooleanVar()
tk.Checkbutton(forcedel,
               text='强制移除目录下已存在文件',
               font=('微软雅黑', 10),
               command=getdisabledoficon,
               onvalue=True,
               offvalue=False,
               variable=isforcedel).pack(side='left')
forcedel.pack(side="left")
window.pack(side='left')

ondebug = tk.BooleanVar()
debug = tk.Frame(line2, relief='groove', borderwidth=2)
tk.Checkbutton(debug,
               text='生成调试文件',
               font=('微软雅黑', 10),
               onvalue=True,
               offvalue=False,
               variable=ondebug).pack(side='left')
debug.pack(side='left', fill='x')
line2.pack(anchor='w')

line3 = tk.Frame(step2)

onicon = tk.BooleanVar()
onicon.set(False)
iconfilepath = tk.StringVar()
iconfilepath.set('')
icon = tk.Frame(line3, relief='groove', borderwidth=2)
tk.Checkbutton(icon,
               text='使用自定义图标',
               font=('微软雅黑', 10),
               command=getdisabledoficon,
               onvalue=True,
               offvalue=False,
               variable=onicon).pack(side='left')
tk.Label(icon, text='选择.ico文件路径', font=('微软雅黑', 10)).pack(side='left')
iconload = tk.Entry(icon,
                    width=30,
                    textvariable=iconfilepath,
                    state='disabled')
iconload.pack(side='left')
iconloadbutt = tk.Button(icon,
                         text='选择……',
                         command=geticonfile,
                         font=('微软雅黑', 8),
                         state='disabled')
iconloadbutt.pack(side='left')
icon.pack(side='left')

line3.pack(anchor='w')
step2.pack(anchor='w')

go = tk.Button(gui,
               text='开始打包',
               background='green',
               activebackground='purple',
               foreground='white',
               font=('等线', 17, 'bold'),
               command=threadment).pack(fill='x')
tk.Label(gui, text="打包时间约15~20秒，请耐心等待").pack()
gui.mainloop()