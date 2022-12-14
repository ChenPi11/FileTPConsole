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
    ConsoleUILabel(ui,text="").update()
    ConsoleUILabel(ui,text="114514",layout=LAYOUT_MIDDLE)
    ConsoleUILabel(ui,text="1919810",layout=LAYOUT_MIDDLE)
    ConsoleUISeperator(ui)
    m=ConsoleUIMenu(ui,layout=LAYOUT_MIDDLE)
    m.set(["1"*10,"2","3"])
    m.update()
    ui.regkeyevent("\x1b",ui.end)#Esc
    Thread(target=ui.mainloop,daemon=True).start()
    c=m.l[m.getchoise()]
    m.destroy()
    print("choise:",c)
    os.system("pause")
    i=ConsoleUIInput(ui,"输入:")
    print(i.get())
    os.system("pause")
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
import curses
curses.getch