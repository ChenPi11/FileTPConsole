import os
from filetp.filetp import *

class Client:
    sk=None
    events:dict={}
    d:DirTree=None
    _not_pause_mainloop:Event=None
    _sending:Event=None
    def __init__(self):
        self.sk=None
        self.events={}
        self.events["onrecvfile"]=nullfun
        self.events["onclose"]=nullfun
        self.d=DirTree()
        self._not_pause_mainloop=Event()
        self._not_pause_mainloop.set()
        self._sending=Event()
    def init(self,ip:str,port:int):
        self.sk=None
        self.sk=FileTP()
        self.sk.connect(ip,port)
        self.d=DirTree()
        self._not_pause_mainloop.set()
    def close(self):
        try:
            try:
                self.events["onclose"]()
            except:
                pass
            self.sk.close()
            self.sk=None
        except:
            pass
    def mainloop(self):
        log=getLogger("MAINLOOP")
        log.info("Start mainloop")
        while(not self.sk.closed):
            try:
                if(not self._not_pause_mainloop.is_set()):
                    log.info("pause and wait")
                    self._not_pause_mainloop.wait()
                _dt=self.sk.recv()
                log.info("Recv:"+_dt)
                dt:dict=json.loads(_dt)
                if(dt["type"]=="file"):
                    log.info("Recv file")
                    self.sendmsg("pause","")
                    self.sk.stat["stat"]=STAT_WAIT
                    self._sending.set()
                    Thread(target=_FileTPDaemon,daemon=True,name="FileTP Daemon").start()
                    self.sk.recvs(config.get("save","."))
                    self._sending.clear()
                    self._sending.clear()
                    log.info("Recv file suc")
                elif(dt["type"]=="pause"):
                    log.info("mainloop paused")
                    self._not_pause_mainloop.clear()
                elif(dt["type"]=="close"):
                    self.close()
                elif(dt["type"]=="msg"):#{type:msg,data:{type:...,title,title2,msg,...}}
                    done=Event()
                    res={}
                    def run(dt:dict,done:Event,res:dict,log:Logger):
                        try:
                            if(dt["data"]["type"]=="info"):
                                #info:data[title,title2,msg]
                                pass
                            elif(dt["data"]["type"]=="warn"):
                                #warn:data[title,title2,msg]
                                pass
                            elif(dt["data"]["type"]=="crit"):
                                #warn:data[title,title2,msg]
                                pass
                            elif(dt["data"]["type"]=="ask"):
                                #warn:data[title,title2,msg]
                                pass
                            elif(dt["data"]["type"]=="input"):
                                #warn:data[title,msg]
                                pass
                            #---------------------------res[data,res]
                            if(dt["data"]["type"]!="input"):
                                res["res"]=dlg.exec_()
                                res["data"]=""
                            else:
                                print("show")
                                r=idlg.show()
                                res["data"]=r[1]
                                res["res"]=r[0]
                            done.set()
                        except:
                            log.printerror()
                            done.set()
                    run(dt,done,res,log)
                    done.wait()
                    log.info("Msgbox done:"+str(res))
                    self.sendmsg("msgres",res)
            except SystemExit:
                raise
            except ConnectionError:
                break
            except AttributeError:
                log.warn(getexc())
                break
            except:
                log.printerror()
        log.info("End mainloop")
    def pausemainloop(self):
        self._not_pause_mainloop.clear()
        #self.sk.sk.sk.setblocking(False)
        #self.sk.sk.sk.abort()
    def resumemainloop(self):
        self._not_pause_mainloop.set()
    def sendmsg(self,mtype:str,data:str):
        self.sk.send(json.dumps({"type":mtype,"data":data}))
    def sendfiles(self):
        log=getLogger("NETWORK")
        log.info("Send files")
        self.sendmsg("file","")
        while(self._not_pause_mainloop.is_set()):
            time.sleep(0.01)
        self.sk.stat["stat"]=STAT_WAIT
        self._sending.set()
        Thread(target=_FileTPDaemon,daemon=True,name="FileTP Daemon").start()
        self.sk.sends(self.d)
        self._sending.clear()
        self.resumemainloop()
    def setdirtree(self,d:DirTree):
        self.d=d
client=Client()

class Server:
    ip:str=""
    port:int=0
    ssk:FileTPServer=None
    log:Logger=None
    def __init__(self):
        self.ip=""
        self.port=0
        self.ssk=None
        self.log=getLogger("SERVER")
    def init(self,ip:str,port:int):
        self.ip=ip
        self.port=port
        self.ssk=None
        self.ssk=FileTPServer()
        self.ssk.ssk.settimeout(6)
        self.ssk.bind(ip,port)
        self.ssk.ssk.settimeout(None)
        self.log.info("Server init")
    def close(self):
        self.log.info("Server close")
        self.ip=""
        self.port=0
        try:
            self.ssk.close()
        except:
            pass
        self.ssk=None
    def accept(self):
        csk=self.ssk.accept(self.ip,self.port)
        self.log.info("Server accept")
        try:
            client.sk.close()
        except:
            pass
        client.sk=csk
        client.sk.sk.settimeout(None)
        self.close()
server=Server()

def _FileTPDaemon():
    pass