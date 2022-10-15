from filetp_color import *
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
        if(len(d.root.children)==0 and len(d.root.value)==0):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        for i in d.root.children:
            printcolor(colors["blue"],lang2icon["dir"]+" "+i.name,bold=True)
        for i in d.value:
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

