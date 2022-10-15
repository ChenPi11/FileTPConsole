from .config import *
import sys
sys.setrecursionlimit(65536)
import os
from .log import *
from os.path import *
import platform
def rmnone(lst:list):
    r=[]
    for i in lst:
        if(i):
            r.append(r)
    return r
class File:
    path=""
    relp=""
    def __init__(self, path, relp=""):
        self.path = path
        self.relp = relp
    def __str__(self):
        return os.path.basename(self.path)
    def __repr__(self):
        return self.path
    def __eq__(self, other):
        return self.path == other.path
    def __hash__(self):
        return hash(self.path)
    def isfile(self):
        return os.path.isfile(self.path)
    def isdir(self):
        return os.path.isdir(self.path)
    def islink(self):
        return os.path.islink(self.path)
    def ismount(self):
        return os.path.ismount(self.path)
class TreeNode:
    children=[]
    value=None
    def __iter__(self):
        return self.children.__iter__()
    def __init__(self) -> None:
        self.children:list[TreeNode]=[]    
class DirTreeNode(TreeNode):
    name=""
    path=""
    relpath=""
    value=set()#files
    def __str__(self):
        return self.path
    def __repr__(self):
        return "<DirTreeNode "+str(self)+">"
    def __init__(self,name:str,path:str=name,relp:str=path) -> None:
        super().__init__()
        self.name=name
        self.path=path
        self.relpath=relp
        self.children:list[DirTreeNode]=[]
    def find(self,p:str):
        for i in self.children:
            if(i.name==p):
                return i
        raise ValueError("Not found: "+str(p))
    def findfile(self,p:str):
        p=p.replace("\\","").replace("/","")
        for i in self.value:
            if(str(i)==str(p)):
                return i
        raise ValueError("Not found: "+str(p))
class DirTree:
    log:Logger=None
    root:DirTreeNode=None
    value=set()
    def scan(self):
        res=([],[],[])#files_rel,files_abs,dirs
        def d(t:DirTreeNode):
            for i in t.value:
                res[0].append(os.path.join(t.relpath,i))
                res[1].append(os.path.join(t.path,i))
            for i in t.children:
                res[2].append(i.relpath)
                d(i)
        d(self.root)
        for i in self.value:
            res[0].append(i.relp)
            res[1].append(i.path)
        return res
    def __init__(self,log=getLogger("DIRTREE")) -> None:
        self.root=DirTreeNode("","","")
        self.log=log
    def adddir(self,p:str):
        assert os.path.isdir(p),strings.dirtree.notadir
        pbasename=os.path.basename(p)
        if(not pbasename):
            pbasename=p[0].upper()+"@mnt"
        for i in self.root.children:
            assert not(os.path.basename(i.name)==pbasename),strings.dirtree.samefileerror
        name=os.path.basename(p)
        if(not name):
            name=p[0].upper()+"@mnt"
        dt=DirTreeNode(name,p,os.path.basename(p))
        self.root.children.append(dt)
        def d(t:DirTreeNode,path:str):
            dit=None
            try:
                dit=os.scandir(path)
            except:
                return
            t.value=set()
            for i in dit:
                if(i.is_dir()):
                    t.children.append(DirTreeNode(i.name,i.path,os.path.join(os.path.basename(p),os.path.relpath(i.path,p))))
                else:
                    t.value.add(i.name)
            dit.close()
            for i in t.children:
                d(i,i.path)
        d(dt,p)
    def addfiles(self,files:list[str]):
        ers=0
        for i in files:
            try:
                assert os.path.isfile(i)
                self.value.add(File(str(i),os.path.basename(str(i))))
            except:
                ers+=1
                self.log.error(strings.dirtree.notafile)
        return ers
    def finddir(self,p:list[str]):
        if(len(p)==0):
            return self.root
        else:
            dt=self.root
            for i in p:
                if(i):
                    dt=dt.find(i)
            return dt
    def hasdir(self,p:list[str]):
        try:
            self.finddir(p)
            return True
        except:
            return False
    def hasfile(self,p:list[str]):
        try:
            assert self.findfile(p)!=None
            return True
        except:
            return False
    def hasobject(self,p:list[str]):
        return self.hasdir(p) or self.hasfile(p)
    def findfileinfiles(self,p:str):
        for i in self.value:
            if(i.relp==p):
                return i.path
    def findfile(self,p:list[str]):
        _p:list[str]=[]
        for i in p:
            if(i):
                _p.append(i)
        p=_p
        if(len(p)==1):
            return self.findfileinfiles(p[0])
        if(len(p)==0):
            raise ValueError(strings.dirtree.notafile)
        else:
            dt=self.root
            for i in p[0:-1]:
                if(i):
                    dt=dt.find(i)
            if(platform.platform().lower().startswith("win")):
                return os.path.join(dt.path,dt.findfile(p[-1])).replace("/","\\")
            else:
                return os.path.join(dt.path,dt.findfile(p[-1])).replace("\\","/")


if(__name__=="__main__"):
    import platform
    dt=DirTree()
    if(platform.platform().startswith("Windows")):
        SD=os.getenv("SystemDrive")
        if(SD==None):
            SD="C:\\"
        dt.adddir(os.path.join(SD,"\\Users",os.getlogin(),"Desktop"))
    else:
        dt.adddir("/home/"+os.getlogin())
    r,a,d=dt.scan()
    for i in d:
        print(i)
    for i in range(len(r)):
        co.init()
        co.initdt[1](co.colors["blue"],r[i],end="\t")
        co.initdt[1](co.colors["lightblue"],a[i],end="\n")