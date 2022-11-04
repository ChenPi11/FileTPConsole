from .socket2 import *
from .socket2 import _Socket2Commands
from .dirtree import *

class _FileTPCommand:
    version=siz8(2)#version 2
    no=_Socket2Commands.no
    ok=_Socket2Commands.ok
    ask=b'\x03'
    answer=b'\x04'
    fileSystemSplit="*"
'''
accept
s<ask>
r<ans>
r<ver>
s<ok/no>
s<msg>

connect
r<ask>
s<ans>
s<ver>
r<ok>
r<msg>

sends
s<ask>
s<dirsize>
r<ok>
s<dirs>
s<filecount>
<-----------^
r<ok>       |
sendfile    |
------------>

recvs
r<ask>
r<dirsize>
s<ok>
r<dirs>
r<filecount>
<-----------^
s<ok>       |
recvfile    |
------------>
'''
class FileTPServer:
    ssk:socket2=None
    log:Logger=None
    binded=False
    def __init__(self,log:Logger=getLogger("FILETP")):
        sk2log=getLogger("SOCKET2",file=log.file,format=log.format,flush=log.flush)
        self.ssk=socket2(sk2log)
        self.log=log
        self.binded=False
    def bind(self,ip:str,port:int):
        self.ssk.bind(ip,port)
        self.binded=True
    def accept(self,ip:str,port:int):
        if(not self.binded):
            self.ssk.bind(ip,port)
        self.binded=True
        c,a=self.ssk.accept()
        try:
            c.settimeout(6)
            c.sk.send(_FileTPCommand.ask)
            assert c.sk.recv(len(_FileTPCommand.answer))==_FileTPCommand.answer,strings.filetp.notfiletp
            assert c.sk.recv(8)==_FileTPCommand.version,strings.filetp.versionnotmatch
            c.sk.send(_FileTPCommand.ok)
            c.settimeout(None)
            self.log.info("Accepted: %s:%d"%(a[0],a[1]))
            return FileTP(self.log,c,a)
        except Exception as e:
            try:
                c.sk.send(_FileTPCommand.no)
                c.send(str(e))
            except:
                self.log.printerror()
            raise
    def close(self):
        self.binded=False
        self.ssk.close()
        self.log.info("FileTPServer closed")

STAT_CHECKING=3
STAT_WAIT=4
class FileTP:
    stat=socket2.stat
    sk:socket2=None
    addr:tuple=("",0)
    log:Logger=None
    _abort:bool=False
    closed:bool=False
    def __init__(self,log:Logger=getLogger("FILETP"),c:socket2=None,a:tuple=("",0)):
        if(c):
            self.sk=c
            self.closed=False
        else:
            self.sk=socket2(getLogger("SOCKET2"))
            self.closed=False
        self.addr=a
        self.log=log
        self.stat["stat"]=STAT_REDAY
        self.stat["file_size"]=1#socket2
        self.stat["file_now"]=0#socket2
        self.stat["file_name"]=""#socket2
        self.stat["file_onsend"]=nullfun#socket2
        self.stat["file_onrecv"]=nullfun#socket2
        self.stat["file_onend"]=nullfun#socket2
        self.stat["oncheck"]=nullfun#filetp
        self.stat["filecount"]=1#filetp
        self.stat["filenow"]=0#filetp
        self.stat["fileerrs"]=[]#filetp
        def default_quest(*a,**kw):
            return True
        self.stat["onquest"]=default_quest#filetp

    def connect(self,ip:str,port:int):
        self.sk.connect(ip,port)
        self.sk.settimeout(6)
        assert self.sk.sk.recv(len(_FileTPCommand.ask))==_FileTPCommand.ask,strings.filetp.notfiletp
        self.sk.sk.send(_FileTPCommand.answer)
        self.sk.sk.send(_FileTPCommand.version)
        if(self.sk.sk.recv(1)!=_FileTPCommand.ok):
            msg=self.sk.recv()
            raise Exception(msg)
        self.sk.settimeout(None)
        self.addr=(ip,port)
        self.closed=False
        self.log.info("Connected to %s:%d"%(ip,port))
    def send(self,data):
        try:
            self.sk.send(data)
        except SocketClosedError:
            self.closed=True
            raise
    def recv(self):
        try:
            return self.sk.recv()
        except SocketClosedError:
            self.closed=True
            raise
    def sends(self,d:DirTree):
        try:
            _r,_a,ds=d.scan()
            self.stat["filecount"]=len(_r)
            self.stat["filenow"]=0
            self.stat["stat"]=STAT_CHECKING
            try:
                self.stat["oncheck"]()
            except:
                self.log.printerror()
            r=[];a=[]
            for i in range(len(_a)):
                if(checkfiler(_a[i])):
                    r.append(_r[i])
                    a.append(_a[i])
                else:
                    self.stat["fileerrs"].append(_a[i])
                self.stat["filenow"]=self.stat["filenow"]+1
            self.stat["stat"]=STAT_WAIT
            self.stat["filecount"]=len(r)
            self.stat["filenow"]=0
            dirsize=sum(map(lambda x:os.path.getsize(x),a))
            self.sk.sk.send(_FileTPCommand.ask)#s <ask>
            sksend(self.sk.sk,siz8(dirsize))#s <dirsize>
            assert self.sk.sk.recv(len(_FileTPCommand.ok))==_FileTPCommand.ok,strings.filetp.sendabort#r <ok>
            self.send(list2str(ds,char=_FileTPCommand.fileSystemSplit))#s <dirs>
            self.sk.sk.send(siz8(len(r)))#s <filecount>
            self.stat["stat"]=STAT_SENDING
            for i in range(len(r)):
                self.stat["file_name"]=r[i]
                self.stat["file_now"]=i
                try:
                    assert self.sk.sk.recv(len(_FileTPCommand.ok))==_FileTPCommand.ok,strings.filetp.sendabort#r <ok>
                    self.sk.sendfile(a[i],r[i])#s <file>
                except SocketClosedError:
                    self.closed=True
                    self.log.printerror()
                    self.stat["fileerrs"].append(r[i])
                except:
                    self.log.printerror()
                    self.stat["fileerrs"].append(r[i])
                self.stat["filenow"]+=1
            self.log.suc("Send files suc:"+str(len(r))+","+str(len(self.stat["fileerrs"]))+" errors")
        except SocketClosedError:
            self.closed=True
            raise
    def recvs(self,path="."):
        try:
            assert self.sk.sk.recv(len(_FileTPCommand.ask))==_FileTPCommand.ask,strings.filetp.notfiletp#r <ask>
            dirsize=dsiz(self.sk.sk.recv(8))#r <dirsize>
            try:
                quest=self.stat["onquest"](dirsize)
            except:
                self.log.printerror()
                quest=False#abort
            if(quest):
                self.sk.sk.send(_FileTPCommand.ok)#s <ok>
            else:
                self.sk.sk.send(_FileTPCommand.no)
                raise AssertionError(strings.filetp.userabort)
            ds=self.recv().split(_FileTPCommand.fileSystemSplit)#r <dirs>
            for i in ds:
                try:
                    if(not os.path.isdir(i)):
                        os.makedirs(os.path.join(path,i))
                        self.log.info("mkdir "+os.path.join(path,i))
                    else:
                        self.log.info("dir "+os.path.join(path,i)+" exists")
                except:
                    self.log.fail("mkdir "+os.path.join(path,i)+" failed")
            filecount=dsiz(self.sk.sk.recv(8))#r <filecount>
            self.stat["stat"]=STAT_RECVING
            for i in range(filecount):
                if(self._abort):
                    self.send(_FileTPCommand.no)
                    raise AssertionError(strings.filetp.userabort)
                else:
                    try:
                        self.sk.sk.send(_FileTPCommand.ok)
                        self.sk.recvfile(path)
                    except SocketClosedError:
                        self.closed=True
                        self.log.printerror()
                        self.stat["fileerrs"].append(r[i])
                    except:
                        self.log.printerror()
                        self.stat["fileerrs"].append(self.stat["file_name"])
                self.stat["filenow"]+=1
            self.log.suc("Recv files suc:"+str(filecount)+","+str(len(self.stat["fileerrs"]))+" errors")
        except SocketClosedError:
            self.closed=True
            raise
    def close(self):
        self.closed=True
        self.sk.close()

def filetp_test():
    TEST_IP="localhost"
    def _FileTP_srv_main():
        debugmode()
        log=getLogger("FILETP")
        s=FileTPServer(log)
        c=s.accept(TEST_IP,15803)
        d=DirTree()
        d.adddir("E:\\IMAGES")
        c.sends(d)
        
        c.close()
        s.close()
    def _FileTP_cli_main():
        debugmode()
        log=getLogger("FILETP")
        f=FileTP(log)
        f.connect(TEST_IP,15803)
        f.recvs()
        f.close()
    if(len(sys.argv)>1):
        if(sys.argv[1]=="-___test-___srv"):
            _FileTP_srv_main()
        else:
            _FileTP_cli_main()
    else:
        os.system("start py -m filetp.filetp"+" -___test-___srv ; pause")
        _FileTP_cli_main()

if(__name__=="__main__"):
    filetp_test()