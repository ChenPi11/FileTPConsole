from typing import IO
class WFiles(IO):
    files=[]
    def __init__(self,files=[]):
        self.files=files
    def __enter__(self):
        return self
    def __exit__(self,*a):
        self.close()
    def __del__(self):
        self.close()
    def __str__(self):
        return str(self.files)
    def __repr__(self):
        return "<Files object:"+str(self.files)+">"
    def __iter__(self):
        return iter(self.files)
    def __next__(self):
        return next(self.files)
    def __getitem__(self,index:int):
        return self.files[index]
    def __setitem__(self,index:int,value):
        self.files[index]=value
    def __delitem__(self,index:int):
        del self.files[index]
    def __len__(self):
        return len(self.files)
    def __bool__(self):
        return bool(self.files)
    def __contains__(self,item):
        return item in self.files
    def close(self):
        for file in self.files:
            file.close()
    def add(self,file):
        self.files.append(file)
    def remove(self,file):
        self.files.remove(file)
    def clear(self):
        self.files.clear()
    def read(self,*a,**k):
        raise IOError("Files object can't read")
    def write(self,*a,**k):
        for file in self.files:
            file.write(*a,**k)
    def flush(self):
        for file in self.files:
            file.flush()
    def fileno(self):
        raise IOError("Files object can't fileno")
    def isatty(self):
        raise IOError("Files object can't isatty")
    def readable(self):
        return False
    def writable(self):
        return True
    def seekable(self):
        return True
    def seek(self,*a,**k):
        for file in self.files:
            file.seek(*a,**k)