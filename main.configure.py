import shutil
try:
    shutil.copyfile("FileTP.log","FileTP.log.bak")
except:
    pass
from filetp_consoleui import *
try:#可能是不必要的
    nullio=open(os.devnull,"w+")
except:
    nullio=open("null.tmp","w+")
if(platform.uname()[0]=="Windows"):
    from ctypes import windll
    from subprocess import Popen
    cp=windll.kernel32.GetConsoleCP()
    path=os.path.join(os.getenv("SystemRoot"),"System32","chcp.com")#%SystemRoot%\System32\chcp.com
    p=Popen([path,str(cp)],shell=True,stdout=sys.stdout,stderr=nullio,cwd=os.getcwd())#重新加载codepage
    p.wait()

def main():
    Log.info("----------FileTP Setting "+main_thread().name+" Start: argv="+str(sys.argv)+
                     ",cwd="+str(os.getcwd())+
                     ",mainthread_ident="+str(main_thread().ident)+
                     ",pid:"+str(os.getpid())+
                     ",time="+str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))+
                     "----------"
                     )
    ui=ConsoleUI()
    ui.init()
    ui.settitle("FileTP Settings")
    print("正在读取设置...")
    print(config)
    time.sleep(1)
    ui.update()
    os.system("pause")
    ui.mainloop()
    ui.end()
if(__name__=="__main__"):
    try:
        main()
        sys.exit(0)
    except SystemExit as e:
        raise e
    except:
        print("\n"+strings.app.error.fatalmsg.replace("{msg}",getexc()))
        Log.fatal("----------UNHANDLED EXCEPTION!!!!!!!----------")
        Log.printerror()
        sys.exit(-1)