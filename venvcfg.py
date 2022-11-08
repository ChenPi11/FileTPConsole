# /usr/bin/env python3
# -*- coding:utf-8 -*-
try:
    def YN():
        res=input("(y/N)").lower()=="y"
        return res
    import venv
    import os
    import platform
    import glob
    import sys
    import shutil
    def _rm_pycache(_,p):
        l=glob.glob(os.path.join(p,"*"))
        if(os.path.basename(p)=="__pycache__"):
            _.append(p)
        for i in l:
            if(os.path.isdir(i)):
                _rm_pycache(_,i)
    def rm_pycache():
        _=[]
        _rm_pycache(_,".")
        for i in _:
            print(i)
            try:
                shutil.rmtree(i)
            except Exception as e:
                print("ERR:",i,e)
                
    if(not os.path.exists("venv")):
        print("[INIT] 正在创建 venv")
        venv.create("venv",with_pip=True)
        print("[SUC] 创建成功")
    print("[INIT] 进入管理器..")
    pip=""
    python=""
    if(platform.uname()[0]=="Windows"):
        pip=os.path.abspath(".\\venv\\Scripts\\pip.exe")
        python=os.path.abspath(".\\venv\\Scripts\\python.exe")
    else:
        pip="./venv/bin/pip"
        python="./venv/bin/python"
    def pipman_main():
        print("pip管理器\n输入exit退出")
        while(1):
            c=input("pip $(input):>>")
            if(c=="exit"):
                break
            cmd=[pip,c]
            cmd.extend(c.strip().split(" "))
            venv.subprocess.Popen(cmd,shell=True).wait()
    def python_shell():
        venv.subprocess.Popen([python],shell=True).wait()
    def python_m():
        print("python -m ",end="")
        c=input()
        cmd=[python,"-m"]
        cmd.extend(c.strip().split(" "))
        venv.subprocess.Popen(cmd,shell=True).wait()
    def venv_init():
        print("[INFO] 正在安装PyInstaller")
        venv.subprocess.Popen([pip,"install","PyInstaller"],shell=True).wait()
        print("[SUC] 初始化完成:安装PyInstaller")
    def install_dependence():
        try:
            f=open("dependence.list","r",encoding="utf-8")
            l=[pip,"install"]
            for i in f.readlines():
                l.append(i.strip())
            #l.extend(f.readlines())
            print(l)
            f.close()
            venv.subprocess.Popen(l,shell=True).wait()
        except Exception as e:
            print("ERROR:"+e.__class__.__name__+": "+str(e))
    def make():
        specs=list(glob.glob("*.spec"))
        if(len(specs)==0):
            print("找不到*.spec")
            return
        print("准备make..")
        print(specs)
        for i in specs:
            i=os.path.abspath(i)
            print("making",i,"...")
            venv.subprocess.Popen([python,"-m","PyInstaller",i],shell=True).wait()
        print("make完成")
    def clean():
        print("是否clean?")
        if(YN()):
            print("rm __pycache__")
            rm_pycache()
            print("rm dist")
            try:
                shutil.rmtree("dist")
            except:
                pass
            print("rm build")
            try:
                shutil.rmtree("build")
            except:
                pass
            print("rm FileTP.log")
            try:
                os.remove("FileTP.log")
            except:
                pass
            print("rm FileTP.log.bak")
            try:
                os.remove("FileTP.log.bak")
            except:
                pass
    try:
        if(sys.argv[1]=="make"):
            make()
            sys.exit(0)
        elif(sys.argv[1]=="clean"):
            clean()
            sys.exit(0)
    except SystemExit:
        raise
    except:
        pass
    while(1):
        print("venv 管理器\n\t0:初始化venv\n\t1:pip 管理器\n\t2:python shell\n\t3:python -m 执行\n\t4:make\n\t5:安装dependence.list中依赖\n\t6:clean\n\t7:exit退出")
        try:
            i=int(input(":"))
            if(i==0):
                venv_init()
            elif(i==1):
                pipman_main()
            elif(i==2):
                python_shell()
            elif(i==3):
                python_m()
            elif(i==4):
                make()
            elif(i==5):
                install_dependence()
            elif(i==6):
                clean()
            elif(i==7):
                sys.exit(0)
            else:
                raise ValueError()
        except ValueError:
            print("ERROR:输入无效!\n")
except SystemExit:
    raise
except Exception as e:
    print("FATAL ERROR:"+e.__class__.__name__+": "+str(e))
