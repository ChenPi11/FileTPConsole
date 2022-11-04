from filetp_color import *

KEY_UP="↑"
KEY_DOWN="↓"
KEY_LEFT="←"
KEY_RIGHT="→"
KEY_ENTER="\n"
if(platform.uname()[0]=="Windows"):
    KEY_ENTER="\r"

def getch():
    if(platform.uname()[0]=="Windows"):
        msvcrt=__import__("msvcrt")
        c=msvcrt.getch()
        if(c==b'\x00' or c==b'\xe0'):#a=0,a=224是功能键
            b=msvcrt.getch()
            match b:
                case b'H':
                    return KEY_UP
                case b'P':
                    return KEY_DOWN
                case b'K':
                    return KEY_LEFT
                case b'M':
                    return KEY_RIGHT
                case _:
                    return ""
        return c.decode(errors="ignore")
    else:
        getch=__import__("getch")
        def _getch():
            try:
                return getch.getch()
            except:
                return _getch()
        c=_getch()
        if(c=="\x1b"):
            if(_getch()!="["):
                return "\x1b"
            b=_getch()
            match b:
                case "A":
                    return KEY_UP
                case "B":
                    return KEY_DOWN
                case "D":
                    return KEY_LEFT
                case "C":
                    return KEY_RIGHT
                case _:
                    return b
        return c
def set_window_title(t:str):
    console.set_window_title(t)
def replace_index(old_string, char, index):
    new_string = old_string[:index] + char + old_string[index+1:]
    return new_string
class LoadingBar:
    p=0
    t:Thread=None
    isstart=Event()
    def __init__(self):
        self.p=0
        self.isstart.clear()
    def _start(self):#进度条撞']'上其实是bug
        _mode=False#(0 mode)
        while(self.isstart.is_set()):
            s=" "*20
            s=replace_index(s,"=",self.p)
            if(self.p>=20):
                _mode=False
            if(self.p<=1):
                _mode=True
            if(_mode):
                self.p+=1
            else:
                self.p-=1
            printcolor(co.colors["yellow"],"\r["+s+"]  ",end="",flush=True)
            time.sleep(0.05)
    def start(self):
        if(self.isstart.is_set()):
            return
        self.isstart.set()
        self.t=Thread(target=self._start,daemon=True)
        self.t.start()
    def stop(self):
        self.isstart.clear()
        print("\r                      ",end="\r")
def getext(file:str):
    l=file.split(".")
    if(len(l)>1):
        return l[-1]
    else:
        return ""
def la(path:str,d:DirTree):# like omz la
    if(path=="/"):
        if((len(d.root.children)==0) and (len(d.root.value)==0)):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        for i in d.root.children:
            printcolor(colors["blue"],lang2icon["dir"]+" "+i.name,bold=True)
        for i in d.root.value:
            if(os.access(getext(str(i)),1) or (platform.uname().system=="Windows" and getext(str(i))=="exe")):#can execute
                printcolor(co.colors["green"],lang2icon[ext2lang[getext(str(i))]]+" "+str(i))
            else:
                printcolor(co.colors["white"],lang2icon[ext2lang[getext(str(i))]]+" "+str(i))
    else:
        if(len(d.finddir(path.split("/")).children)==0 and len(d.finddir(path.split("/")).value)==0):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        path=path.replace("\\","/")
        for i in d.finddir(path.split("/")).children:
            printcolor(colors["blue"],lang2icon["dir"]+" "+i.name,bold=True)
        for i in d.finddir(path.split("/")).value:
            if(os.access(getext(str(i)),1) or (platform.uname().system=="Windows" and getext(str(i))=="exe")):#can execute
                printcolor(co.colors["green"],lang2icon[ext2lang[getext(str(i))]]+" "+str(i))
            else:
                printcolor(co.colors["white"],lang2icon[ext2lang[getext(str(i))]]+" "+str(i))

class ConsoleUI:
    title=""
    endloop:Event=None
    keyevents:ConvDict=None
    lastline=1#上一个创建了组件的行
    def __init__(self):
        self.title=""
        self.endloop=Event()
        self.keyevents=ConvDict({})
        self.keyevents.default=nullfun
    def init(self):
        self.update()
        self.endloop.clear()
    def update(self):
        print("\x1b[44m",end="")
        console.control(Control.home())
        print((" "*int(console.size[0]/2-len(self.title)/2)+self.title),flush=True)
        print(" "*console.size[0]*(console.size[1]-1),end="",flush=True)
        console.control(Control.home())
        print("")
        self.lastline=1
        self.keyevents.clear()
    def settitle(self,t:str):
        self.title=t
        console.set_window_title(t)
        print("\033[s\033[0;0H",end="",flush=True)
        print((" "*int(console.size[0]/2-len(t)/2))+t," "*(console.size[0]-int(console.size[0]/2-len(t)/2)),sep="",flush=True)
        print("\033[u",end="",flush=True)
    def end(self):
        print("\x1b[0m",end="")
        console.clear()
        self.endloop.set()
    def regkeyevent(self,key:str,event):
        self.keyevents[key]=event
    def unregkeyevent(self,key:str):
        self.keyevents[key]=nullfun
    def mainloop(self):
        while(not self.endloop.is_set()):
            c=getch()
            self.keyevents[c]()
LAYOUT_MIDDLE=-1

class ConsoleUILabel:
    ui:ConsoleUI=None
    text:str=""
    line=None
    layout=0
    def __init__(self,ui:ConsoleUI,line=None,text="",layout=0):
        self.ui=ui
        self.init(line,text,layout)
    def init(self,line=None,text="",layout=0):
        self.line=line
        if(self.line==None):
            self.line=self.ui.lastline
            self.ui.lastline+=1
        self.text=text
        self.layout=layout
        self.update()
    def update(self):
        print("\033[s\033["+str(self.line+1)+";0H",end="",flush=True)
        if(self.layout==LAYOUT_MIDDLE):
            print("\x1b[44m"+" "*((console.size[0]-len(self.text))//2),end="",flush=True)
        print(self.text,flush=True)
    def settext(self,text:str):
        self.text=text
        self.update()
    def gettext(self):
        return self.text
class ConsoleUISeperator:
    ui:ConsoleUI=None
    line=None
    def __init__(self,ui:ConsoleUI,line=None):
        self.ui=ui
        self.init(line)
    def init(self,line=None):
        self.line=line
        if(self.line==None):
            self.line=self.ui.lastline
            self.ui.lastline+=1
        self.update()
    def update(self):
        print("\033[s\033["+str(self.line+1)+";0H",end="",flush=True)
        print("-"*console.size[0],end="",flush=True)
class ConsoleUIMenu:
    ui:ConsoleUI=None
    l=[]
    choise=0
    line=None
    layout=0#left
    submit_event=None
    def __init__(self,ui:ConsoleUI,line=None,layout=0):
        self.ui=ui
        self.l=[]
        self.choise=0
        self.submit_event=Event()
        self.init(line,layout)
    def set(self,l=[]):
        self.l=l
    def getchoise(self):
        self.submit_event.wait()
        return self.choise
    def setchoise(self,choise=0):
        self.choise=choise
    def init(self,line=None,layout=0):
        self.line=line
        if(self.line==None):
            self.line=self.ui.lastline
        self.layout=layout
        self.update()
        self.ui.regkeyevent(KEY_UP,self.up)
        self.ui.regkeyevent(KEY_DOWN,self.down)
        self.ui.regkeyevent(KEY_ENTER,self.submit)
    def up(self):
        if(self.choise<=0):
            return
        self.choise-=1
        self.update()
    def down(self):
        if(self.choise>=(len(self.l)-1)):
            return
        self.choise+=1
        self.update()
    def submit(self):
        self.submit_event.set()
    def update(self,start=""):
        self.ui.lastline+=len(self.l)
        print("\033[s\033["+str(self.line+1)+";0H",end="",flush=True)
        for i in range(0,len(self.l)):
            obj=str(self.l[i])
            if(self.layout==-1):#middle
                print("\x1b[44m"+" "*((console.size[0]-len(max(self.l, key=len, default="")))//2),end="",flush=True)#列表求最长,除2
            if(i==self.choise):
                print("\x1b[0m",end="",flush=True)
            else:
                print("\x1b[44m",end="",flush=True)
            print(start,obj,sep="",flush=True)
    def destroy(self):
        self.ui.unregkeyevent(KEY_ENTER)
        self.ui.unregkeyevent(KEY_UP)
        self.ui.unregkeyevent(KEY_DOWN)
        self.ui.update()
class ConsoleUIInput:
    ui:ConsoleUI=None
    msg:str=""
    res:str=""
    def __init__(self,ui,msg=""):
        self.msg=msg
        self.ui=ui
        self.update()
    def update(self):
        self.ui.update()
        print("\033[1;0H",end="",flush=True)
        self.res=input("\x1b[44m"+self.msg)
        self.ui.update()
    def get(self):
        return self.res
        
if(__name__=="__main__"):
    pass