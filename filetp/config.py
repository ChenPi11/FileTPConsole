PORT=15803
SOCKET_BUFSIZ=1000
config={}
DEBUG=False
class strings:
    class log:
        ioserr="加入的对象不是一个可写的文本IO流"
    class dirtree:
        samefileerror="添加的文件或文件夹与之前的名称相同"
        notadir="不是一个有效的文件夹"
        notafile="不是一个有效的文件"
        notaobj="找不着指定的文件或目录"
    class socket2:
        openfileabort="对方打开文件时出错"
        sendfileabort="接收方终止了接收"
        recvfileabort="发送方终止了发送"
        selfabort="自身终止了操作"
    class filetp:
        notfiletp="对方不是FileTP或对方网络速度太慢"
        filetpcloseerror="连接已经断开"
        userabort="用户拒绝了文件传输请求"
        sendabort="对方拒绝了请求"
        versionnotmatch="版本不匹配"
    class app:
        class error:
            fatalmsg="出现了一个严重的错误，导致程序主线程停止工作。"
        class aboutDlg:
            title="关于 - FileTP"
            about="FileTP 是一个文件传输程序，你可以用它在计算机间互相传输文件。\nFileTP 不是 \"FTP\" 并且不支持 \"FTP\"。\nFileTP 是一个免费软件，你可以免费使用它。\nFileTP 可以在 Linux,Windows,Windows NT 上使用，\n适用于手机-电脑中大文件（夹）传输，或者虚拟机-实体机中传输文件。\n\nCopyright (C) 2022  ChenPi11\nhttps://github.com/ChenPi11"
        class messages:
            wait_conn="等待连接:%s..."
            after_conn="连接成功:%s"
            conn_closed="连接已经关闭"
            server_closed="服务器已经关闭"
            parseraddrerror="无效的地址（应该形如\"ip:port\"或\"ip\"）"
            connecting="正在连接:%s..."
            msgfrom="来自 %s 的消息"
            addfilessuc="成功添加了 %s 个文件"
            rmfilessuc="成功移除了项目:%s"
            settimeoutsuc="成功设置了超时时间:%s"
            closed="已关闭"
            unconnect="未连接"
            connected="已连接"
            really_want_close_connection="真的要关闭?"
            
            class helps:
                exit="exit: exit\n\t关闭连接并退出FileTP。"
                quit="quit: quit\n\t关闭连接并退出FileTP。"
                EOF="EOF: EOF\n\t关闭连接并退出FileTP，\n\t也可以Ctrl+D退出。"
                ls="用法: ls [PATH]\n\t列出[PATH]下所有文件(白色)及目录(蓝色)。\n\t如果未指定[PATH]，则默认列出当前目录。"
                dir="用法: dir [PATH]\n\t列出[PATH]下所有文件(白色)及目录(蓝色)。\n\t如果未指定[PATH]，则默认列出当前目录。"
                add="用法: add [PATH]\n\t将[PATH]代表的目录或文件移动到FileTP的文件系统中，\n\t移动到根目录中。\n\t\n\t注: 这里[PATH]指系统路径。"
                cd="用法: cd [PATH]\n\t进入FileTP的文件系统中的某一个目录[PATH]。"
                chdir="用法: chdir [PATH]\n\t进入FileTP的文件系统中的某一个目录[PATH]。"
                rm="用法: rm [PATH]\n\t从FileTP的文件系统中移除[PATH]代表的目录或文件。\n\t\n\t注:不真正删除系统中对应的文件。"
                clear="clear: clear\n\t清除屏幕。"
                cls="cls: cls\n\t清除屏幕。"
                type="用法: type [PATH]\n\t显示FileTP的文件系统中[PATH]代表的文件。"
                dollar="用法: $+[command]\n\t例如: $echo test\n\t执行系统命令。"
                help="help: help\n\t显示此帮助文档"
                #network commands
                connect="用法：connect [IP] [:port]\n\t连接指定的IP地址和端口号\n\t例如：\"connect 127.0.0.1\" 等价于：\"connect 127.0.0.1:15803\"。"
                close="close：close\n\t关闭连接"
                class _help_msg:
                    exit_quit_EOF2="关闭连接并退出FileTP"
                    ls_dir2="列出[PATH]下所有文件(白色)及目录(蓝色)"
                    add2="将[PATH]代表的目录或文件移动到FileTP的文件系统中"
                    cd_chdir2="进入FileTP的文件系统中的某一个目录[PATH]"
                    rm2="从FileTP的文件系统中移除[PATH]代表的目录或文件"
                    clear_cls2="清除屏幕"
                    type2="显示FileTP的文件系统中[PATH]代表的文件"
                    dollar2="执行系统命令"
                    help2="显示此帮助文档"
                    #network commands
                    connect2="连接指定的IP地址和端口号"
                    bind="开放设备作为FileTP服务器"
                    close2="关闭连接"

                    end_help="执行 help [command] 显示命令的详细用法"

        app="FileTP"
        err="错误"
        connect="连接"
        connection="连接"
        label2="连接(应形如\"<ip>\"或\"<ip>:<port>\")"
        disconn="断开连接"
        addfile="添加文件"
        adddir="添加文件夹"
        label3="开放(IP应形如\"<ip>\"或\"<ip>:<port>\")"
        accepting="正在开放..."
        label4="发送/接收状态"
        label5="文件列表"
        send="发送"
        remove="移除"
        file="文件"
        add="添加"
        setting="设置"
        options="选项"
        about="关于"
        about_app="关于应用"
        console="控制台"
        quit="退出"
        help="帮助"
        serverstat="服务器状态"
        clear_server_msg="清除服务器消息"
        clear_console="清除控制台"
        addfiledlgtitle="添加文件"
        adddirdlgtitle="添加文件夹"
        execute="执行"
        recvfilequest="接收到文件传输请求"
        rfquestask="是否接收文件传输请求？"
        cancel="取消"
        pro="FileTP:%s>"
        intro="FileTP Command v1.0"
        unkowncmd="未知的命令:"
        terminate="终止"
        nofiles="没有文件"
        routing_gateway="路由网关"
        routing_NIC="路由NIC名称"
        routing_MAC="路由NIC MAC地址"
        routing_IP="路由IP地址"
        routing_nmask="子网掩码"
        recving="正在接收:%s"
        recv_done="接收完成"
LANGPACK="zh-cn.lang"
CONFFILE="config.cfg"
LOGFILE="FileTP.log"

#-------------------------------------------------------loader----------------------------------------
import os,sys,json
def res(relative_path:str):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def getopt(k,_=None):
    return k.get(k,_)
def config_load():
    global config
    try:
        with open(CONFFILE,"r",encoding="utf-8") as f:
            config=dict(json.load(f))
    except:
        print("Load config file error",CONFFILE,file=sys.stderr)
    try:
        with open(config.get("langpack",LANGPACK),"r",encoding="utf-8") as f:
            for i in f:
                i=i.strip()
                if(i.startswith("#") or i==""):
                    continue
                try:
                    k,v=i.split("=")
                    k=k.strip()
                    v=v.strip()
                    exec("strings.%s=%s"%(k,v))
                except Exception as e:
                    print("Load lang file error",e.__class__.__name__,e,file=sys.stderr)
    except Exception as e:
        print("Load lang file error",e.__class__.__name__,e,file=sys.stderr)

config_load()
