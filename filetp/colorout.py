from .config import *
import ctypes,platform,signal,os
STD_OUTPUT_HANDLE=    -11
nullfun = lambda *args: None
def _(n,msg,flush=False,end="\n",file=sys.stderr,*a,**kw):
    print(msg,flush=flush,end=end,file=file)
def has_color():
    no_color=False
    no_color=(no_color if no_color is not None else "NO_COLOR" in os.environ)
    return not no_color
initdt=[0,_,nullfun]#handle,colorize,colorreset
colors={}#white,black,red,green,yellow,blue,magenta,cyan,lightgray,darkgray,lightred,lightgreen,lightyellow,lightblue,lightmagenta,lightcyan
colors["white"]=37
colors["black"]=30
colors["red"]=31
colors["green"]=32
colors["yellow"]=33
colors["blue"]=34
colors["magenta"]=35
colors["cyan"]=36
colors["lightgray"]=37
colors["darkgray"]=90
colors["lightred"]=91
colors["lightgreen"]=92
colors["lightyellow"]=93
colors["lightblue"]=94
colors["lightmagenta"]=95
colors["lightcyan"]=96
def lcolorinit():
    global initdt
    initdt=[]
    initdt.append(0)
    def lshcolorize(num,string,bold=False,highlight=False,end="\n",flush=False,file=sys.stdout):
        try:
            attr = []
            if highlight: 
                num += 10
            attr.append(str(num))
            if bold: attr.append('1')
            if(has_color()):
                print('\x1b[%sm%s\x1b[0m' % (';'.join(attr), string),end=end,flush=flush,file=file)
            else:
                print(string,end=end,flush=flush,file=file)
        except:
            pass
    initdt.append(lshcolorize)
    def lshcolorreset(*a,**kw):
        try:
            if(has_color()):
                print('\033[0m',end="")
        except:
            pass
    initdt.append(lshcolorreset)
def wcolorinit():
    global initdt
    try:
        initdt=[]
        initdt.append(ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE))
        def wshcolorize(num,string,bold=False,highlight=False,end="\n",flush=False,file=sys.stderr):
            try:
                handle = initdt[0]
                ctypes.windll.kernel32.SetConsoleTextAttribute(handle, num)
                print(string,end=end,flush=flush,file=file)
            except:
                pass
        initdt.append(wshcolorize)
        def wshcolorreset(*a,**kw):
            try:
                handle = initdt[0]
                ctypes.windll.kernel32.SetConsoleTextAttribute(handle,7)
            except:
                pass
        initdt.append(wshcolorreset)
    except Exception as e:
        print("WARNING:",e.__class__.__name__,e)
        initdt=[]
        initdt.append(0)
        initdt.append(_)
        initdt.append(nullfun)
COMODE_DEFAULT=0
COMODE_LINUX=1
COMODE_WIN32=2
def init(mode:int=COMODE_DEFAULT):
    '''mode:COMODE_DEGAULT,COMODE_LINUX,COMODE_WIN32'''
    global colors
    if(mode==COMODE_LINUX):
        lcolorinit()
        colors["white"]=37
        colors["black"]=30
        colors["red"]=31
        colors["green"]=32
        colors["yellow"]=33
        colors["blue"]=34
        colors["magenta"]=35
        colors["cyan"]=36
        colors["lightgray"]=37
        colors["darkgray"]=90
        colors["lightred"]=91
        colors["lightgreen"]=92
        colors["lightyellow"]=93
        colors["lightblue"]=94
        colors["lightmagenta"]=95
        colors["lightcyan"]=96
        return 1
    elif(mode==COMODE_WIN32):
        wcolorinit()
        colors["white"]=7
        colors["black"]=0
        colors["red"]=4
        colors["green"]=2
        colors["yellow"]=6
        colors["blue"]=1
        colors["magenta"]=5
        colors["cyan"]=3
        colors["lightgray"]=8
        colors["darkgray"]=9
        colors["lightred"]=12
        colors["lightgreen"]=10
        colors["lightyellow"]=14
        colors["lightblue"]=11
        colors["lightmagenta"]=13
        colors["lightcyan"]=15
        return 2
    if(platform.platform().startswith("Windows")):
        wcolorinit()
        colors["white"]=7
        colors["black"]=0
        colors["red"]=4
        colors["green"]=2
        colors["yellow"]=6
        colors["blue"]=1
        colors["magenta"]=5
        colors["cyan"]=3
        colors["lightgray"]=8
        colors["darkgray"]=9
        colors["lightred"]=12
        colors["lightgreen"]=10
        colors["lightyellow"]=14
        colors["lightblue"]=11
        colors["lightmagenta"]=13
        colors["lightcyan"]=15
    else:
        lcolorinit()
        colors["white"]=37
        colors["black"]=30
        colors["red"]=31
        colors["green"]=32
        colors["yellow"]=33
        colors["blue"]=34
        colors["magenta"]=35
        colors["cyan"]=36
        colors["lightgray"]=37
        colors["darkgray"]=90
        colors["lightred"]=91
        colors["lightgreen"]=92
        colors["lightyellow"]=93
        colors["lightblue"]=94
        colors["lightmagenta"]=95
        colors["lightcyan"]=96
    signal.signal(signal.SIGINT,initdt[2])
    signal.signal(signal.SIGTERM,initdt[2])
    signal.signal(signal.SIGILL,initdt[2])
    signal.signal(signal.SIGABRT,initdt[2])

if(__name__=="__main__"):
    init()
    initdt[1](colors["green"],"Color ",end="")
    initdt[1](colors["blue"],"Printer",end="")
    initdt[1](colors["white"],"!",end="\n")
    initdt[1](colors["cyan"],"Usage:",end="\n")
    initdt[1](colors["green"],"\tColor ",end="")
    initdt[1](colors["blue"],"Printer",end="")
    initdt[1](colors["yellow"],"??????????????????????????????????????????????????????Pyhton???",end="\n")
    initdt[2]()
    print("\tinit(mode):init???????????????????????????mode?????????COMODE_DEFAULT(??????????????????),COMODE_LINUX(Linux,UNIX,...??????),COMODE_WIN32(Windows??????)")
    if(platform.platform().startswith("Windows")):
        print("\t??????????????????????????????Windows???????????????????????????cmd????????????(Windows Terminal,VSCode Terminal???)????????????????????????Linux??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????\\0x33[...]????????????")
        init(COMODE_LINUX)
        initdt[1](colors["green"],"\t\tColor ",end="")
        initdt[1](colors["blue"],"Printer",end="")
        initdt[1](colors["white"],"!",end="\n")
        initdt[1](colors["green"],"\t\tColor ",end="")
        initdt[1](colors["blue"],"Printer",end="")
        initdt[1](colors["yellow"],"??????????????????????????????????????????????????????Pyhton???",end="\n")
        initdt[2]()
        init()
    
    print("\n\n\n???init?????????????????????????????????:")
    print("\tinitdt[1](color,text,end=\\n,bold=False,highlight=False,file=sys.stdout")
    print("\tcolor:????????????,?????????????????????????????????")
    initdt[1](colors["white"],"white",end=",")
    initdt[1](colors["black"],"black",end=",")
    initdt[1](colors["white"],"(black)",end=",")
    initdt[1](colors["red"],"red",end=",")
    initdt[1](colors["green"],"green",end=",")
    initdt[1](colors["yellow"],"yellow",end=",")
    initdt[1](colors["blue"],"blue",end=",")
    initdt[1](colors["magenta"],"magenta",end=",")
    initdt[1](colors["cyan"],"cyan",end=",")
    initdt[1](colors["lightgray"],"lightgray",end=",")
    initdt[1](colors["darkgray"],"darkgray",end=",")
    initdt[1](colors["lightred"],"lightred",end=",")
    initdt[1](colors["lightgreen"],"lightgreen",end=",")
    initdt[1](colors["lightyellow"],"lightyellow",end=",")
    initdt[1](colors["lightblue"],"lightblue",end=",")
    initdt[1](colors["lightmagenta"],"lightmagenta",end=",")
    initdt[1](colors["lightcyan"],"lightcyan",end="\n")
    initdt[1](colors["white"],"\tbold:????????????,???????????????(WINAPI?????????)",bold=True)
    initdt[1](colors["green"],"\thighlight:????????????,???????????????(????????????white??????,WINAPI???????????????)",highlight=True)
    print("\tfile:????????????,?????????sys.stdout")
    print("\ninitdt[2]()????????????????????????(???WINAPI??????????????????Linux????????????)")
    initdt[2]()
    print("????????????")
    initdt[1](colors["red"],"\t??????:Python IDLE Shell??????????????????",end="\n")
    import os
    if(platform.platform().startswith("Windows")):
        os.system("pause")
    else:
        os.system("read -p \"Press 'Enter' to continue...\" _________temp_var")

    init(COMODE_WIN32)
    print("Set color by call WINAPI")
    initdt[1](colors["red"],"test")
    initdt[1](colors["green"],"test")
    initdt[1](colors["yellow"],"test")
    initdt[1](colors["blue"],"test")
    initdt[1](colors["magenta"],"test")
    initdt[1](colors["cyan"],"test")
    initdt[1](colors["lightgray"],"test")
    initdt[1](colors["darkgray"],"test")
    initdt[1](colors["lightred"],"test")
    initdt[1](colors["lightgreen"],"test")
    initdt[1](colors["lightyellow"],"test")
    initdt[1](colors["lightblue"],"test")
    initdt[1](colors["lightmagenta"],"test")
    initdt[1](colors["lightcyan"],"test")
    initdt[1](colors["white"],"test")
    initdt[1](colors["black"],"test")
    initdt[2]()
    
    print("Set color by use Linux console color syntax ('\\0x33[...]')")
    init(COMODE_LINUX)
    initdt[1](colors["red"],"test(hignlight)",highlight=True)
    initdt[1](colors["red"],"test(bold)",bold=True)
    initdt[1](colors["red"],"test(nothing)")
    initdt[1](colors["red"],"test(bold,highlight)",bold=True,highlight=True)
    initdt[1](colors["green"],"test")
    initdt[1](colors["yellow"],"test")
    initdt[1](colors["blue"],"test")
    initdt[1](colors["magenta"],"test")
    initdt[1](colors["cyan"],"test")
    initdt[1](colors["lightgray"],"test")
    initdt[1](colors["darkgray"],"test")
    initdt[1](colors["lightred"],"test")
    initdt[1](colors["lightgreen"],"test")
    initdt[1](colors["lightyellow"],"test")
    initdt[1](colors["lightblue"],"test")
    initdt[1](colors["lightmagenta"],"test")
    initdt[1](colors["lightcyan"],"test")
    initdt[1](colors["white"],"test")
    initdt[1](colors["black"],"test")
    initdt[2]()