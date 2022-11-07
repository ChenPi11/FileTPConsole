import builtins
from filetp.filetp import *
import rich
from rich.console import *
from rich.syntax import *
from rich.highlighter import *
from rich.progress import *
import rich.text
co.init(co.COMODE_LINUX)
def printcolor(num,string,bold=False,highlight=False,end="\n",flush=False,file=sys.stdout):
    co.initdt[1](num,string,bold,highlight,end,flush,file)
    resetcolor()
def resetcolor():
    co.initdt[2]()
colors=co.colors

console = rich.get_console()
def printcode(code:str,stype:str):
    syntax = Syntax(code, stype, theme="monokai", line_numbers=True)
    console.print(syntax)
#ext
class ConvDict(dict):
    default=None
    def __getitem__(self, __key):
        return self.get(__key,self.default)
ext2lang=ConvDict({
    #Python
    "py":"python",
    "rpy":"python",
    "pyw":"python",
    "cpy":"python",
    "gyp":"python",
    "gypi":"python",
    "pyi":"python",
    "ipy":"python",
    "pyt":"python",
    "spec":"python",#pyinstaller
    #Java
    "java":"java",
    "class":"java",
    "jav":"java",
    #C++
    "cpp":"c++",
    "cc":"c++",
    "cxx":"c++",
    "c++":"c++",
    "hpp":"c++",
    "hh":"c++",
    "hxx":"c++",
    "h":"c++",
    "ii":"c++",
    #C
    "c":"c",
    "i":"c",
    #C#
    "cs":"cs",
    "csx":"cs",
    "cake":"cs",
    #XML
    "xml":"xml",
    "xsd":"xml",
    "ascx":"xml",
    "atom":"xml",
    "axml":"xml",
    "axaml":"xml",
    "bpmn":"xml",
    "cpt":"xml",
    "csl":"xml",
    "csproj":"xml",
    "cppproj":"xml",
    "pyproj":"xml",
    "ui":"xml",#Qt
    #HTML
    "html":"html",
    "htm":"html",
    "shtml":"html",
    "xhtml":"html",
    "xht":"html",
    "mdoc":"html",
    "jsp":"html",
    "jshtm":"html",
    "asp":"html",
    "aspx":"html",
    #CSS
    "css":"css",
    #Javascript
    "js":"js",
    "es6":"js",
    "mjs":"js",
    "cjs":"js",
    "pac":"js",
    #PHP
    "php":"php",
    "php4":"php",
    "php5":"php",
    "phtml":"php",
    "ctp":"php",
    #Batch
    "bat":"batch",
    "cmd":"batch",
    #sh
    "sh":"sh",
    "bash":"sh",
    "bashrc":"sh",
    "bash_aliases":"sh",
    "bash_profile":"sh",
    "bash_login":"sh",
    "ebuild":"sh",
    "profile":"sh",
    "bash_logout":"sh",
    "xprofile":"sh",
    #VB
    "vb":"vb",
    "brs":"vb",
    "bas":"vb",
    "vba":"vb",
    #VBS
    "vbs":"vbs",
    #text
    "txt":"text",
    "text":"text",
    #vim
    "vim":"vim"
})
ext2lang.default="auto"
'''

'''

lang2icon=ConvDict({
    "python":"🐍",
    "java":"☕",
    "text":"📄",
    "dir":"📂",
    "markdown":"📜"

})
lang2icon.default="📄"

#fix open
richopen=open
open=builtins.open

try:
    with open(config.get("langpack",os.devnull),"r",encoding="utf-8") as f:
        for i in f:
            i=i.strip()
            if(i.startswith("#") or i==""):
                continue
            try:
                k,v=i.split("=")
                k=k.strip()
                v=v.strip()
                #exec("strings.%s=%s"%(k,v))
                lang2icon[k]=v
            except Exception as e:
                pass
except Exception as e:
    pass


