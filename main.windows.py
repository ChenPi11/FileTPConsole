#Main For Windows
'''import argparse
parser = argparse.ArgumentParser(description="")#help msg
parser.add_argument('-gf', '--girlfriend', choices=['jingjing', 'lihuan'])
parser.add_argument('--house', type=int, default=0)
# 3.进行参数解析
args = parser.parse_args() 
print('------args---------',args)
'''
import platform
import ctypes
from cmd import Cmd
from subprocess import *
import sys
import glob
import qrcode
from filetp.filetp import *
from filetp_color import *
from filetp_commands import *
from filetp_consoleui import *
import os
try:#可能是不必要的
    nullio=open(os.devnull,"w+")
except:
    nullio=open("null.tmp","w+")
if(platform.uname()[0]=="Windows"):
    cp=ctypes.windll.kernel32.GetConsoleCP()
    path=os.path.join(os.getenv("SystemRoot"),"System32","chcp.com")#%SystemRoot%\System32\chcp.com
    p=Popen([path,str(cp)],shell=True,stdout=sys.stdout,stderr=nullio,cwd=os.getcwd())#重新加载codepage
    p.wait()
    
def exit():
    #do exit command
    print("\n"+strings.app.terminate)
    Log.info("----------FileTP App Close:time:"+str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))+"----------")
def countdir(path):
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            file_count = file_count + 1
    return file_count
def YN():
    res=input("(Y/N)").lower()=="y"
    return res
def ctrlc(sig, frame):
    print("\n")
def _makefilename(name:str):
    if(" " in str(name)):
        return "\""+str(name)+"\""
    else:
        return str(name)
def ls(path:str,d:DirTree,color=True):
    if(path=="/"):
        if((len(d.root.children)==0) and (len(d.root.value)==0)):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        for i in d.root.children:
            if(color):
                printcolor(colors["blue"],_makefilename(i.name),bold=True,end=" ")
            else:
                print(_makefilename(i.name),end=" ")
        for i in d.value:
            print(_makefilename(str(i)),end=" ")
    else:
        if((len(d.finddir(path.split("/")).children)==0) and (len(d.finddir(path.split("/")).value)==0)):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        path=path.replace("\\","/")
        for i in d.finddir(path.split("/")).children:
            if(color):
                printcolor(colors["blue"],_makefilename(i.name),bold=True,end=" ")
            else:
                print(_makefilename(i.name),end=" ")
        for i in d.finddir(path.split("/")).value:
            print(_makefilename(str(i)),end=" ")
    print()
def dir_(path:str,d:DirTree,color=True):
    if(path=="/"):
        if(len(d.root.children) and len(d.root.value)==0):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        for i in d.root.children:
            if(color):
                printcolor(colors["blue"],i.name,bold=True)
            else:
                print(i.name)
        for i in d.value:
            print(str(i))
    else:
        if(len(d.finddir(path.split("/")).children)==0 and len(d.finddir(path.split("/")).value)==0):
            print('\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["lightgray"]),"3","1","2"]), strings.app.nofiles))
            return
        path=path.replace("\\","/")
        for i in d.finddir(path.split("/")).children:
            if(color):
                printcolor(colors["blue"],str(i.name),bold=True)
            else:
                print(i.name)
        for i in d.finddir(path.split("/")).value:
            print(str(i))
    print()
def parse_addr(addr:str):
    args=addr.split(":")
    if(len(args)>1):
        try:
            ip=args[0]
            port=int(args[1])
            return ip,port
        except:
            raise AssertionError(strings.app.messages.parseraddrerror)
    else:
        return addr,PORT
def _connected(c:Client):
    try:
        return not c.sk.closed
    except:
        return False
class ClientCmd(Cmd):
    def _make_qrcode(self,msg):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=1,border=1)
        qr.add_data(msg)
        qr.make()
        im=qr.make_image(fill_color='black', back_color='white')
        for i in range(0,im.size[0],2):
            for j in range(im.size[1]):
                mode=0#0b00,0b01,0b10,0b11
                if(im.getpixel((i,j))):
                    mode+=0b10
                if(i<im.size[0]-1):
                    if(im.getpixel((i+1,j))):
                        mode+=0b01
                match(mode):#please run on Python3.10.x or later
                    case 0:#00
                        print(" ",end='')
                    case 1:#01
                        print("▄",end='')
                    case 2:#10
                        print("▀",end='')
                    case _:#11
                        print("█",end='')
            print()#\n
        im.close()
    def do_test(self,arg):
        print("do_test() called                 [  OK  ]")
        self.c.sk.recvs("build")
        
    log=getLogger("CMD")
    prompt = strings.app.pro
    intro = strings.app.intro
    cd="/"
    d:DirTree=None
    c:Client=None
    timeout=6
    def chdirupdate(self):
        if(self.d.hasdir(self.cd.split("/"))):
            cd='\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["blue"]),"1"]), self.cd)
            self.prompt=strings.app.pro % cd
        else:
            self.do_chdir("/")
    def __init__(self):
        super().__init__()
        self.cd="/"
        cd='\x1b[%sm%s\x1b[0m' % (';'.join([str(colors["blue"]),"1"]), self.cd)
        self.prompt = strings.app.pro % cd
        self.intro = strings.app.intro
        self.d=DirTree()
        self.timeout=6
        setattr(self,"help_$",self._help_dollar)
    def on_ctrl_c(self):
        pass    
    def do_exit(self, arg):
        exit()
        return True
    def do_quit(self, arg):
        self.do_exit(arg)
    def do_EOF(self, line):
        exit()
        return True
    def do_ls(self,arg):
        try:
            path=(os.path.normpath(os.path.join(self.cd,arg))).replace("\\","/").split("/")
            if(arg):
                if(self.d.hasdir(path)):
                    ls(arg,self.d)
                else:
                    printcolor(colors["red"],strings.dirtree.notadir)
            else:
                ls(self.cd,self.d)
        except:
            printcolor(colors["red"],strings.app.err+":"+getexc())
            Log.printerror()
    def do_dir(self,arg):
        try:
            dir_(self.cd,self.d)
        except:
            printcolor(colors["red"],strings.app.err+":"+getexc())
            Log.printerror()
    def do_la(self,arg):
        try:
            la(self.cd,self.d)
        except:
            printcolor(colors["red"],strings.app.err+":"+getexc())
            Log.printerror()
    def do_add(self,path):
        try:
            if(path):
                if(os.path.isdir(path)):
                    self.d.adddir(path)
                    printcolor(colors["green"],strings.app.messages.addfilessuc % str(countdir(path)))
                    Log.info("Add dir:"+path)
                else:
                    files=glob.glob(path)
                    print(files)
                    if(len(files)):
                        self.d.addfiles(files)
                        printcolor(colors["green"],strings.app.messages.addfilessuc % str(len(files)))
                    else:
                        printcolor(colors["red"],strings.dirtree.notafile)
                        Log.fail(strings.dirtree.notafile)
            else:
                self.help_add()
        except AssertionError as e:
            printcolor(colors["red"],str(e))
        except:
            Log.printerror()
            printcolor(colors["red"],getexc())
    def do_cd(self,path):
        Log.info("Chdir:"+path)
        if(path):
            path=(os.path.normpath(os.path.join(self.cd,path))).replace("\\","/").split("/")
            try:
                self.d.finddir(path)
                self.cd="/".join(path)
                self.chdirupdate()
            except ValueError:
                printcolor(colors["red"],strings.dirtree.notadir)
            except:
                printcolor(colors["red"],strings.app.err+":"+getexc())
                Log.printerror()
        else:
            print(self.cd)
    def do_chdir(self,path):
        self.do_cd(path)
    def rmdir(self,path:str):
        Log.info("Rm dir: "+path)
        paths=path.replace("\\","/").split("/")
        _d=self.d.root
        _f=None
        for i in paths:
            if(i):
                _f=_d
                _d=_d.find(i)
        _f.children.remove(_d)
        if(not self.d.hasdir(self.cd.split("/"))):
            self.do_cd("/")
    def rmfile(self,path:str):
        Log.info("Rm file: "+path)
        paths=path.replace("\\","/").split("/")
        _d=self.d.root
        for i in paths[0:-1]:
            if(i):
                _d=_d.find(i)
        _d.value.remove(paths[-1])
    def do_rm(self,path:str):
        try:
            if(path):
                path=(os.path.normpath(os.path.join(self.cd,path))).replace("\\","/").split("/")
                if(self.d.hasdir(path)):
                    if(YN()):
                        self.rmdir("/".join(path))
                    else:
                        printcolor(colors["red"],strings.app.terminate)
                        return
                elif(self.d.hasfile(path)):
                    if(YN()):
                        self.rmfile("/".join(path))
                    else:
                        printcolor(colors["red"],strings.app.terminate)
                else:
                    raise ValueError(strings.dirtree.notaobj)
            else:
                pass#help_rm
            printcolor(colors["green"],strings.app.messages.rmfilessuc % "/".join(path))
        except ValueError as e:
            printcolor(colors["red"],strings.app.err+":"+str(e))
        except:
            Log.printerror()
            printcolor(colors["red"],strings.app.err+":"+getexc())
    def do_clear(self,arg:str):
        if(platform.system().lower()=="windows"):
            os.system("cls")
        elif(platform.system().lower()=="linux"):
            os.system("clear")
        else:
            print("\033c")
    def do_cls(self,arg:str):
        self.do_clear(arg)
    def do_cat(self,path:str):
        self.do_type(path)
    def do_type(self,path:str):
        try:
            path=(os.path.normpath(os.path.join(self.cd,path))).replace("\\","/").split("/")
            assert self.d.hasfile(path),strings.dirtree.notafile
            filep=str(self.d.findfile(path))
            assert os.path.isfile(filep),strings.dirtree.notafile+":"+str(filep)
            f=open(filep,encoding="utf-8",errors="ignore")
            data=f.read(1024*1024*900)
            f.close()
            ext=os.path.splitext(filep)[1].replace(".","")
            printcode(data,ext2lang[ext])
        except (AssertionError,ValueError,UnicodeError) as e:
            printcolor(colors["red"],str(e))
        except:
            printcolor(colors["red"],getexc())
    def do_help(self,arg):
        if(len(arg)):
            cmd=arg
            if(hasattr(self,"help_"+cmd)):
                getattr(self,"help_"+cmd)()
            else:
                printcolor(colors["red"],strings.app.unkowncmd+arg)
        else:
            help_msg="add          "+strings.app.messages.helps._help_msg.add2+"\n"+ \
                     "cd/chdir     "+strings.app.messages.helps._help_msg.cd_chdir2+"\n"+ \
                     "clear/cls    "+strings.app.messages.helps._help_msg.clear_cls2+"\n"+ \
                     "$            "+strings.app.messages.helps._help_msg.dollar2+"\n"+ \
                     "exit/quit    "+strings.app.messages.helps._help_msg.exit_quit_EOF2+"\n"+ \
                     "help         "+strings.app.messages.helps._help_msg.help2+"\n"+ \
                     "ls/dir       "+strings.app.messages.helps._help_msg.ls_dir2+"\n"+ \
                     "rm           "+strings.app.messages.helps._help_msg.rm2+"\n"+ \
                     "cat/type     "+strings.app.messages.helps._help_msg.type2+"\n"+ \
                     "connect      "+strings.app.messages.helps._help_msg.connect2+"\n"+ \
                     "close        "+strings.app.messages.helps._help_msg.close2+"\n"+ \
                     strings.app.messages.helps._help_msg.end_help
            printcolor(colors["white"],help_msg,bold=True)
    
    #network
    def do_connect(self,arg):
        if(_connected(self.c)):
            print(strings.app.messages.helps.connect)
            return
        if(not arg):
            self.help_connect()
            return
        l=LoadingBar()
        try:
            self.c=Client()
            addr=parse_addr(arg)
            printcolor(colors["yellow"],strings.app.messages.connecting % (str(addr[0])+":"+str(addr[1])))
            l.start()
            self.c.init(addr[0],addr[1])
            printcolor(colors["green"],"\r"+strings.app.messages.after_conn % (str(addr[0])+":"+str(addr[1])))
            l.stop()
        except (AssertionError,OSError) as e:
            l.stop()
            self.c.close()
            printcolor(colors["red"],str(e))
        except:
            l.stop()
            self.c.close()
            printcolor(colors["red"],getexc())
    def do_bind(self,arg):
        if(_connected(self.c)):
            print(strings.app.messages.connected)
            return
        print("test,arg=",arg)
        self._make_qrcode(arg)
    def do_close(self,arg):
        try:
            if(not _connected(self.c)):
                print(strings.app.messages.unconnect)
                return
            printcolor(colors["yellow"],strings.app.messages.really_want_close_connection,end="")
            if(YN()):
                self.c.close()
                printcolor(colors["green"],strings.app.messages.closed)
                self.c=None
            else:
                printcolor(colors["red"],strings.app.terminate)
        except:
            printcolor(colors["red"],getexc())
    
    def help_exit(self,*args):
        print(strings.app.messages.helps.exit)
    def help_quit(self,*args):
        print(strings.app.messages.helps.quit)
    def help_EOF(self,*args):
        print(strings.app.messages.helps.EOF)
    def help_ls(self,*args):
        print(strings.app.messages.helps.ls)
    def help_dir(self,*args):
        print(strings.app.messages.helps.dir)
    def help_add(self,*args):
        print(strings.app.messages.helps.add)
    def help_cd(self,*args):
        print(strings.app.messages.helps.cd)
    def help_chdir(self,*args):
        print(strings.app.messages.helps.chdir)
    def help_rm(self,*args):
        print(strings.app.messages.helps.rm)
    def help_clear(self,*args):
        print(strings.app.messages.helps.clear)
    def help_cls(self,*args):
        print(strings.app.messages.helps.cls)
    def help_type(self,*args):
        print(strings.app.messages.helps.type)
    def help_cat(self,*args):
        self.help_type(*args)
    def help_help(self,*args):
        print(strings.app.messages.helps.help)
    def _help_dollar(self):
        print(strings.app.messages.helps.dollar)
    #network commands help
    def help_connect(self,*args):
        print(strings.app.messages.helps.connect)
    def help_close(self,*args):
        print(strings.app.messages.helps.close)
    def default(self, line):
        arg = line.strip()
        if(arg.encode("utf-8")[0]==4):#Ctrl+D
            exit()
            return True
        if(line.startswith("$")):
            res=os.system(line[1:])
            if(res!=0):
                print(str(res)+":",end="")
        else:
            print(strings.app.unkowncmd+arg)
    def keyboard_interrupt(self):#Ctrl+C
        ctrlc(None,None)
    def emptyline(self):
        pass
def main(args):
    try:
        try:
            Log.info("----------FileTP "+main_thread().name+" Start: argv="+str(sys.argv)+
                     ",cwd="+str(os.getcwd())+
                     ",mainthread_ident="+str(main_thread().ident)+
                     ",pid:"+str(os.getpid())+
                     ",time="+str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))+
                     "----------"
                     )
        except:
            pass
        clientcmd=ClientCmd()
        clientcmd.chdirupdate()
        clientcmd.cmdloop()
    except:
        print("\n"+strings.app.error.fatalmsg.replace("{msg}",getexc()))
        Log.fatal("----------UNHANDLED EXCEPTION!!!!!!!----------")
        Log.printerror()
        
        exit()
        sys.exit(-1)
if(__name__=="__main__"):
    main(sys.argv)
    sys.exit(0)