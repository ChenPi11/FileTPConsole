from threading import *
from .config import *
from .log import *
import socket
nullfun=co.nullfun
_RetAddress = tuple
class SocketAbortError(IOError):
    pass
class _socket(socket.socket):
    _master=None
    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)#ipv4
        self.__abort__=False
        self.setblocking(False)
    def accept(self):#Overriding Python3.10 socket.socket.accept()
        """accept() -> (socket object, address info)

        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
        fd, addr = self._accept()
        sock = _socket(self.family, self.type, self.proto, fileno=fd)#Override
        # Issue #7995: if no default timeout is set and the listening
        # socket had a (non-zero) timeout, force the new socket in blocking
        # mode to override platform-specific socket flags inheritance.
        '''if socket.getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)'''
        sock.setblocking(False)
        return sock, addr
    __send__=socket.socket.send
    __recv__=socket.socket.recv
    def send(self,data:bytes):
        sksend(self,data)
    def recv(self,size:int):
        return skrecv(self,size)
class SocketError(socket.error):
    pass
class SocketClosedError(SocketError):
    pass
def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass
def siz8(d:int,i=256):
    siz=8
    _=d
    r=[]
    while(d!=0):
        r.append(d%i)
        d=d//i
    if(len(r)<siz):
        r.extend([0]*(8-len(r)))
    if(len(r)>siz):
        raise IndexError("too long number:"+str(_)+"\tmax:"+str(dsiz([255]*siz)))
    return bytes(r)
def dsiz(d):
    r=0
    for i in range(0,len(d)):
        r+=d[i]*pow(256,i)
    return r
def list2str(lst,char):
    res=""
    for i in lst:
        res+=i+char
    res=res[0:len(res)-1]
    return res
def skrecv(sk:_socket,siz):
    dt=bytes()
    _=0
    while(siz-len(dt)):
        _dt=sk.__recv__(siz-len(dt))
        if(len(_dt)<1):
            _+=1
            if(_>1024):
                try:
                    sk._master.connected=False
                    sk._master.close()
                except:
                    pass
                raise SocketClosedError("Socket closed")
        dt+=_dt
    sk.settimeout(None)
    return dt
def sksend(sk:_socket,dt):
    l=sk.__send__(dt)
    while(l<len(dt)):
        l+=sk.__send__(dt[l:])
def checkfiler(path):
    try:
        f=open(path,"rb")
        assert f.seekable(),"seek"
        assert f.readable(),"read"
        f.close()
        return True
    except:
        return False
def writefile(path,log,num=0):
    if(num):
        _path=os.path.splitext(path)[0]+" ("+str(num)+")"+os.path.splitext(path)[1]
    else:
        _path=path
    if(os.path.isfile(_path)):
        log.info("File already exists:"+_path)
        return writefile(path,log,num+1)
    else:
        log.info("Open file:"+_path)
        return _path
def checkfilew(path):
    try:
        f=open(path,"r+b")
        assert f.seekable(),"seek"
        assert f.writable(),"write"
        f.close()
        return True
    except:
        return False
class _Socket2Commands:
    no=b"\x00"
    ok=b"\x01"
    err=b"\x02"
'''
s=socket.send
r=socket.recv

connect:
connect
s<ok>#是否支持UTF
r<ok/no>#对方是否支持UTF

accept:
accept
r<ok/no>#对方是否支持UTF
s<ok>#是否支持UTF

send:
s<siz8(size)>
s<data>

recv:
r<siz8(size)>
r<data>

st=send()
rt=recv()

sendfile
s<siz8(siz)>
st<relp>
<----------------------^
s<data>                |
r<ok> -> assert check  |
s<ok/no/err>           |
----------------------->

recvfile
r<siz8(siz)>
rt<relp>
<----------------------^
r<data>                |
s<ok/no/err>           |
r<ok> -> assert check  |
----------------------->
'''
STAT_REDAY=0
STAT_SENDING=1
STAT_RECVING=2
class socket2:
    sk:_socket=None
    addr:_RetAddress=None
    connected:bool=False
    _abort:bool=False
    bufsiz:int=1024*1024*1#1MB
    log:Logger=None
    stat:dict={}#stat,file_size,file_now,file_name,file_onsend,file_onrecv,file_onend
    encoding="utf-8"
    def __str__(self) -> str:
        '''toString'''
        return "<socket2 object "+str(self.sk)+" >"
    def __repr__(self) -> str:
        '''toString'''
        return "<socket2 object "+str(self.sk)+" >"
    def __init__(self,log:Logger=getLogger("SOCKET2"),bufsiz:int=1024*1024*1,c:_socket=None,addr:_RetAddress=("",0)) -> None:
        '''init socket2,bufsiz:sendfile buffer size'''
        self.log=log
        self.bufsiz=bufsiz
        if(c):
            self.sk=c
            self.sk._master=self
            self.connected=True
        else:
            self.sk=_socket()
            self.sk._master=self
        self.addr=addr
        self.sk.settimeout(None)
        self.stat["stat"]=STAT_REDAY
        self.stat["file_size"]=1
        self.stat["file_now"]=0
        self.stat["file_name"]=""
        self.stat["file_onsend"]=nullfun
        self.stat["file_onrecv"]=nullfun
        self.stat["file_onend"]=nullfun
    def listen(self,backlog=10) -> None:
        '''listen'''
        self.sk.listen(backlog)
    def bind(self,ip,port,lbl=10) -> None:
        '''bind socket to address'''
        self.sk.bind((ip,port))
        self.addr=(ip,port)
        self.listen(lbl)
        self.log.info("Binded:"+str(self.addr))
    def connect(self,ip,port) -> None:
        '''connect socket to address,askutf:ask theotherside for utf8'''
        self.sk.connect((ip,port))
        self.addr=(ip,port)
        self.connected=True
        sksend(self.sk,_Socket2Commands.ok)#s<ok>
        sputf=skrecv(self.sk,len(_Socket2Commands.ok))==_Socket2Commands.ok#r<ok/no>
        if(sputf):
            self.encoding="utf-8"
        else:
            self.encoding="GBK"
        self.log.info("Connected:"+str(self.addr)+",fd="+str(self.sk.fileno()))
    def accept(self):
        '''accept connection'''
        sk,addr=self.sk.accept()
        r=socket2(log=self.log,bufsiz=self.bufsiz,c=sk,addr=addr)
        sputf=skrecv(sk,len(_Socket2Commands.ok))==_Socket2Commands.ok#r<ok/no>
        if(sputf):
            r.encoding="utf-8"
        else:
            r.encoding="GBK"
        sksend(sk,_Socket2Commands.ok)#s<ok>
        sk._master=r
        r.connected=True
        self.log.info("Accepted:"+str(addr)+",fd="+str(sk.fileno()))
        return r,addr
    
    def send(self,data:str) -> None:
        '''send data(string)'''
        try:
            data=data.encode(self.encoding)
            ph=siz8(len(data))
            sksend(self.sk,ph)
            sksend(self.sk,data)
        except(ConnectionRefusedError,SocketClosedError):
            self.close()
            raise
    def recv(self) -> str:
        '''recv data(string) from socket'''
        try:
            _=skrecv(self.sk,8)
            ph=dsiz(_)
            dt=skrecv(self.sk,ph)
            if(abs(len(dt)-ph)):
                self.log.warn("OVERFLOW")
            try:
                try:
                    return dt.decode(self.encoding)
                except:
                    try:
                        return dt.decode("utf-8")
                    except:
                        return dt.decode("GBK")
            except:
                self.log.printerror()
                raise
        except(ConnectionRefusedError,SocketClosedError):
            self.close()
            raise
    
    def sendfile(self,path:str,relp:str=None) -> None:
        '''send file'''
        if(relp==None):
            relp=os.path.basename(path)
        try:
            if(not checkfiler(path)):
                self.log.fail("File not found:"+path)
                raise FileNotFoundError("File not found:"+path)
            f=open(path,"rb")
            siz=os.path.getsize(path)
            bufsiz=self.bufsiz
            #f:fd,siz:filesize,relp:relativepath,bufsiz:buffer size
            self.log.info("Reday to sendfile:"+path+",size="+str(siz)+",relp="+relp)
            self.stat["stat"]=STAT_SENDING
            self.stat["file_size"]=siz
            self.stat["file_now"]=0
            self.stat["file_name"]=relp
            try:
                Thread(target=self.stat["file_onsend"]).start()
            except:
                self.log.warn(getexc())
            pb=self.log.progressBar(siz,False)
            #----------------------------------------------------sending
            sksend(self.sk,siz8(siz))#send filesize
            sksend(self.sk,siz8(bufsiz))#send bufsiz
            self.send(relp)#send relativepath
            while(True):
                try:
                    dt=f.read(bufsiz)
                    if(not dt):
                        break
                    sksend(self.sk,dt)#send data
                    self.stat["file_now"]+=len(dt)
                    pb.setProgress(self.stat["file_now"])
                    assert self.sk.recv(1)==_Socket2Commands.ok,strings.socket2.sendfileabort#check ok
                    assert not self._abort,strings.socket2.selfabort
                    sksend(self.sk,_Socket2Commands.ok)#send ok
                except AssertionError as e:
                    self._abort=False
                    sksend(self.sk,_Socket2Commands.no)#send no
                    self.log.fail(str(e))
                    raise
                except:
                    self.log.fail(getexc())
                    pb.error()
                    pb.end()
                    sksend(self.sk,_Socket2Commands.err)
                    raise
            #----------------------------------------------------sending
            pb.suc()
            pb.end()
            self.stat["stat"]=STAT_REDAY
            self.stat["file_size"]=1
            self.stat["file_now"]=0
            self.stat["file_name"]=""
            try:
                Thread(target=self.stat["file_onend"]).start()
            except:
                self.log.warn(getexc())
            f.close()
            self.log.suc("Sendfile success:"+path)
        except(ConnectionRefusedError,SocketClosedError):
            self.close()
            raise
    def recvfile(self,path:str=".") -> str:
        '''recv file'''
        try:
            siz=dsiz(skrecv(self.sk,8))
            bufsiz=dsiz(skrecv(self.sk,8))
            relp=self.recv()
            path=writefile(os.path.join(path,relp),self.log)
            if(co.platform.system().lower().startswith("windows")):#Windows
                path=path.replace("/","\\")
            else:#Linux,Darwin
                path=path.replace("\\","/")
            f=open(path,"wb")
            #f:fd,siz:filesize,relp:relativepath,path:abspath
            self.log.info("Reday to recvfile:"+path+",size="+str(siz)+",relp="+relp)
            self.stat["stat"]=STAT_RECVING
            self.stat["file_size"]=siz
            self.stat["file_now"]=0
            self.stat["file_name"]=relp
            try:
                Thread(target=self.stat["file_onrecv"]).start()
            except:
                self.log.warn(getexc())
            pb=self.log.progressBar(siz,False)
            #----------------------------------------------------recving
            while(True):
                try:
                    if(self.stat["file_now"]+bufsiz>siz):
                        dt=skrecv(self.sk,siz-self.stat["file_now"])
                    else:
                        dt=skrecv(self.sk,bufsiz)
                    if(not dt):
                        break
                    f.write(dt)
                    f.flush()
                    self.stat["file_now"]+=len(dt)
                    pb.setProgress(self.stat["file_now"])

                    sksend(self.sk,_Socket2Commands.ok)#send ok
                    assert self.sk.recv(1)==_Socket2Commands.ok,strings.socket2.recvfileabort#check ok
                    assert not self._abort,strings.socket2.selfabort
                except AssertionError as e:
                    self._abort=False
                    sksend(self.sk,_Socket2Commands.no)
                    self.log.fail(str(e))
                    raise
                except:
                    self.log.fail(getexc())
                    pb.error()
                    pb.end()
                    sksend(self.sk,_Socket2Commands.err)
                    raise
            #----------------------------------------------------recving
            pb.suc()
            pb.end()
            self.stat["stat"]=STAT_REDAY
            self.stat["file_size"]=1
            self.stat["file_now"]=0
            self.stat["file_name"]=""
            try:
                Thread(target=self.stat["file_onend"]).start()
            except:
                self.log.warn(getexc())
            f.close()
            self.log.suc("Recvfile success:"+path)
            return path
        except ConnectionError:
            self.close()
            raise
    def close(self) -> None:
        '''close socket'''
        try:
            self.sk.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.sk.close()
        self.connected=False
    def settimeout(self,timeout:int|None) -> None:
        '''set timeout'''
        self.sk.settimeout(timeout)

if(__name__=="__main__"):
    TEST_IP="localhost"
    def _test_srv_main():
        try:
            debugmode()
            sk=socket2()
            sk.bind(TEST_IP,65533,10)
            c,a=sk.accept()
            c.send("test")
            c.send("测试")
            r=c.recv()
            if(r=="test"):
                co.initdt[1](co.colors["green"],"Server recv:"+str(r))
            else:
                co.initdt[1](co.colors["red"],"Server recv:"+str(r))
            r=c.recv()
            if(r=="测试"):
                co.initdt[1](co.colors["green"],"Server recv:"+str(r))
            else:
                co.initdt[1](co.colors["red"],"Server recv:"+str(r))
            
            c.sendfile("testfile.txt")

            c.close()
            sk.close()
            Log.suc("Test success")
            co.initdt[2]()
            os.system("pause")
        except:
            Log.printerror()
            co.initdt[2]()
            os.system("pause")
    def _test_cli_main():
        try:
            debugmode()
            sk=socket2()
            sk.connect(TEST_IP,65533)
            r=sk.recv()
            if(r=="test"):
                co.initdt[1](co.colors["green"],"Client recv:"+str(r))
            else:
                co.initdt[1](co.colors["red"],"Client recv :"+str(r))
            r=sk.recv()
            if(r=="测试"):
                co.initdt[1](co.colors["green"],"Client recv:"+str(r))
            else:
                co.initdt[1](co.colors["red"],"Client recv:"+str(r))
            sk.send("test")
            sk.send("测试")

            sk.recvfile(".")

            sk.close()
            Log.suc("Test success")
            co.initdt[2]()
            os.system("pause")
        except:
            Log.printerror()
            co.initdt[2]()
            os.system("pause")
    if(len(sys.argv)>1):
        if(sys.argv[1]=="-___test-___srv"):
            _test_srv_main()
        else:
            #os.system("start "+sys.argv[0]+" -___test-___srv")
            _test_cli_main()
    else:
        #os.system("start "+sys.argv[0]+" -___test-___srv")
        _test_cli_main()
