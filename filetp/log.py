from os import devnull
from typing import TextIO
from . import colorout as co
from .files import *
import sys,traceback,time
start_time=time.time()
strings=co.strings
def print_list(extracted_list):#Python3.traceback override
    """Print the list of tuples as returned by extract_tb() or
    extract_stack() as a formatted stack trace to the given file."""
    res=""
    for item in traceback.StackSummary.from_list(extracted_list).format():
        res+=item
    return res
def getexc():
    '''Get more exception infomation'''
    if(sys.exc_info()[0]==None):
        return ""
    res="Traceback(catch):\n"
    res+=print_list(traceback.extract_tb(sys.exc_info()[2]))
    res+=sys.exc_info()[0].__name__+": "+str(sys.exc_info()[1])
    return res
def gettime():
    '''Get program running time'''
    return int((time.time()-start_time)*1000000)
def debugmode(mode:int=0,printmsg:bool=True):
    '''Set debug mode\n(mode:co.COMODE_DEGAULT,co.COMODE_LINUX,co.COMODE_WIN32,\nprintmsg:print "--DEBUG MODE--" or not)'''
    if(printmsg):
        print("--------------------------DEBUG MODE--------------------------")
    co.init(mode)
if(co.LOGFILE):
    try:
        f=open(co.LOGFILE,"w",encoding="utf-8")
    except:
        print(getexc(),file=sys.stderr)
        f=None
else:
    f=None
if(f):
    default_file=f
else:
    default_file=open(devnull)
def set_default_file(file:TextIO):
    '''Set default file to write log'''
    global default_file
    default_file=file
class _ProgressBar:
    file=None
    max=10
    now=0
    flush=True
    def __init__(self,file=default_file,max=0,flush=True):
        '''Init progress bar in console'''
        self.file=file
        self.max=max
        self.now=0
        self.flush=flush
        self.update(0)
    def setProgress(self,now):
        '''Set progress bar'''
        self.now=now
        if(self.now>=self.max):
            self.suc()
            return
        self.update(0)
    def back(self,back=1):
        '''Back progress bar'''
        self.now-=back
        if(self.now<0):
            self.now=0
        self.update(0)
    def update(self,add=1):
        '''Update progress bar'''
        if(co.DEBUG):
            if(self.max==0):
                self.suc()
                return
            if(self.now>=self.max):
                return
            if(self.now+add>=self.max):
                self.now=self.max
            else:
                self.now+=add
            prs=int(self.now/self.max*100)
            string="\r["+"="*(prs//10)+" "*(10-prs//10)+"] "+str(prs)+"% "+str(self.now)+"/"+str(self.max)
            if(prs>=100):
                self.suc()
            elif(prs>=50):
                co.initdt[1](co.colors["lightblue"],string,file=self.file,flush=self.flush,end="        ")
            else:
                co.initdt[1](co.colors["yellow"],string,file=self.file,flush=self.flush,end="        ")
    def error(self,msg:str=""):
        '''Set progress bar in error'''
        co.initdt[1](co.colors["red"],"\r[          ] -% "+str(self.now)+"/"+str(self.max),end="",file=self.file,flush=self.flush)
        if(str(msg)!=""):
            co.initdt[1](co.colors["red"],":"+str(msg),file=self.file,flush=self.flush,end="        ")
    def suc(self,msg:str=""):
        '''Set progress bar in sucess'''
        co.initdt[1](co.colors["green"],"\r[==========] 100% "+str(self.now)+"/"+str(self.max),end="",file=self.file,flush=self.flush)
        if(str(msg)!=""):
            co.initdt[1](co.colors["green"],":"+str(msg),file=self.file,flush=self.flush,end="        ")
    def end(self):
        '''End progress bar'''
        print("",file=self.file,flush=self.flush)
    def __del__(self):
        self.end()
loggers={}
class Logger:
    name=""
    file:TextIO=None
    _flush=False
    format:str=""
    def __init__(self,name:str="SYSTEM",file:TextIO=sys.stderr,format:str="[{lvl} {name} {time}] {msg}",flush:bool=False):
        global loggers
        self.name=str(name)
        self.file=file
        self._flush=flush
        self.format=format
        if(not file.writable()):
            raise TypeError(strings.log.ioserr)
        if(name.upper() in loggers.keys()):
            raise TypeError("Logger "+name+" already exists,use getLogger()")
        loggers[name.upper()]=self
    def __str__(self):
        return self.name
    def __repr__(self):
        return "<Logger object:"+self.name+">"
    def write(self,msg:str):
        try:
            self.file.write(msg)
            if(self._flush):
                self.flush()
        except:
            pass
    def flush(self):
        try:
            self.file.flush()
        except:
            pass
    def log(self,level:str,msg:str,color:str="white",ctl:bool=False):
        '''Print log message to file. msg:message,ctl:iscritical'''
        try:
            co.initdt[1](co.colors[color],self.format.format(lvl=level,name=self.name,time=gettime(),msg=msg),flush=self._flush,end="\n",
                bold=ctl,highlight=ctl,file=self.file)
        except:
            self.write("Error:"+getexc()+"\t,"+str(gettime())+","+level+","+msg+"\n")
    def info(self,msg:str):
        '''Print info log message to file. msg:message'''
        self.log("INFO",str(msg),"white",False)
    def warn(self,msg:str):
        '''Print warning log message to file. msg:message'''
        self.log("WARN",str(msg),"yellow",False)
    def error(self,msg:str):
        '''Print error log message to file. msg:message'''
        self.log("ERROR",str(msg),"red",False)
    def debug(self,msg:str):
        '''Print debug log message to file. msg:message'''
        self.log("DEBUG",str(msg),"blue",False)
    def exception(self,msg:str):
        '''Print exception log message to file. msg:message'''
        self.log("EXCEPTION",str(msg),"lightred",False)
    def fail(self,msg:str):
        '''Print fail log message to file. msg:message'''
        self.log("FAIL",str(msg),"lightred",False)
    def suc(self,msg:str):
        '''Print success log message to file. msg:message'''
        self.log("SUC",str(msg),"green",False)
    def critical(self,msg:str):
        '''Print critical log message to file. msg:message'''
        self.log("CRITICAL",str(msg),"red",True)
    def fatal(self,msg:str):
        '''Print fatal log message to file. msg:message'''
        self.log("FATAL",str(msg),"yellow",True)
    def suc_critical(self,msg:str):
        '''Print success critial log message to file. msg:message'''
        self.log("SUCC",str(msg),"green",True)
    def printerror(self):
        '''Print catched traceback message to file.'''
        e=str(getexc())
        if(e):
            self.error(e)
    def close(self):
        '''Close the logger file'''
        try:
            self.file.close()
            self.file=None
            co.initdt[2]()
        except:
            pass
    def progressBar(self,max:int,flush:bool=True) -> _ProgressBar:
        '''Return a progress bar object'''
        try:
            return _ProgressBar(file=self.file,max=max,flush=flush)
        except:
            pass
Log=Logger("SYSTEM",default_file,flush=False,format="[{lvl} {name} {time}] {msg}")
def getLogger(name:str="SYSTEM",file=default_file,format="[{lvl} {name} {time}] {msg}",flush=False) -> Logger:
    '''Get a logger object by name. name:logger name'''
    global loggers
    if(name.upper() in loggers.keys()):
        l=loggers[name.upper()]
        l.file=file
        l.format=format
        l._flush=flush
        return l
    else:
        l=Logger(name,file=file,flush=flush,format=format)
        return l
if(__name__=="__main__"):
    print("no debug mode")
    log=Logger()
    log.info("test")
    log.warn("test")
    log.error("test")
    log.debug("test")
    log.exception("test")
    log.fail("test")
    log.suc("test")
    log.critical("test")
    log.fatal("test")
    log.suc_critical("test")
    print("debug mode")
    debugmode()
    log.info("test")
    log.warn("test")
    log.error("test")
    log.debug("test")
    log.exception("test")
    log.fail("test")
    log.suc("test")
    log.critical("test")
    log.fatal("test")
    log.suc_critical("test")
    try:
        raise Exception("printerror() test")
    except:
        log.printerror()
    log.info("Let's test the progress bar!")
    p=log.progressBar(100)
    for i in range(100):
        p.update(1)
        time.sleep(0.1)

    time.sleep(1)
    p.error("Err")
    time.sleep(1)
    p.suc("Suc")
    time.sleep(1)
    p.setProgress(50)
    time.sleep(0.5)
    p.setProgress(100)
    time.sleep(0.5)
    p.setProgress(0)
    time.sleep(0.5)
    p.setProgress(100)
    time.sleep(0.5)
    for i in range(100):
        p.back(1)
        time.sleep(0.1)
    
    p.end()
    log.close()