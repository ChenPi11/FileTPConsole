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
    def adddir(self,path:str):
        Log.info("Add dir: "+path)
        self.d.adddir(path)
    def addfiles(self,paths:list[str]):
        Log.info("Add files: "+str(paths))
        self.d.addfiles(paths)
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
    def rmfile(self,path:str):
        Log.info("Rm file: "+path)
        paths=path.replace("\\","/").split("/")
        _d=self.d.root
        for i in paths[0:-1]:
            if(i):
                _d=_d.find(i)
        _d.value.remove(paths[-1])
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
        self.d=None
        self.d=DirTree()
    def list(self):
        sr=self.d.scan()
        return sr[0],sr[2]

client=Client()