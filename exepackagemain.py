import subprocess
import sys
if 'pyinstaller' in subprocess.run(
        'pip list', encoding='utf-8', text=True,
        stdout=subprocess.PIPE).stdout:  #获取pyinstaller库的安装
    print('检测到了pyinstaller的安装，开始进行打包')  #检测库安装
else:
    print('未安装pyinstaller')
    if subprocess.run('python.exe -m pip install pyinstaller').returncode != 0:
        exit(1)
    else:
        print('自动安装成功！')
args = sys.stdin.read().split('|')
shellcmd = 'pyinstaller "' + args[0] + "\""
if args[2] == 'True':
    shellcmd += ' -F'
else:
    shellcmd += ' -D'
if args[3] == 'True':
    shellcmd += ' -d all'
if args[4] == 'True':
    shellcmd += ' -c'
else:
    shellcmd += ' -w'
if args[5] == 'True':
    shellcmd += ' --icon="' + args[6] + '"'
if args[7] == 'True':
    shellcmd += ' -y'
print('要运行的指令：', shellcmd, '开始运行……')
create = subprocess.run(shellcmd)
if create.returncode == 0:
    print('指令执行成功！(0)')
    exit(0)
else:
    print('运行错误(' + str(create.returncode) + ')')
    exit(2)