#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, random, string, socket, urllib2, base64, subprocess, ssl

# 格式化读取数组呈现的内容
def byteify(input, encoding='utf-8'):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode(encoding)
    else:
        return input

# 运行 python 脚本
def runpy(ssrfile):
    os.system("python /usr/local/SSR.Go/"+ssrfile+".py")

# 运行 shell 脚本
def runshell(src, cmd):
    setShell="bash "+src+" "+cmd
    print subprocess.call(setShell, shell=True)

# 输出 json 配置参数
def Show_conf(txt, item):
    print (txt+"为：%s") % str(item)
    print ("")

# 生成随机密码
# python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
def Pwd(length):
    salt = '!@#$%^&*()><?'
    chars=string.ascii_letters+string.digits+salt
    return ''.join([random.choice(chars) for i in range(length)]) # 得出的结果中字符会有重复的
    # return ''.join(random.sample(chars, 16))#得出的结果中字符不会有重复的
if __name__=="__main__":
    # 密码的长度为16
    print GenPassword(length)

# 生成随机区间数（端口）
def Port(port1, port2):
        return(random.randint(port1, port2))

# 判断是否为数字的函数（ulits）
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

# 协议、加密方式、混淆模式函数
def Whether(ask, c1, c2, config, describe ,item, cancel, ssrfile):
    print(ask)
    pick = raw_input()
    if pick == c1 or pick == '':
        config(item)
	print ("新的"+ describe + "为：%s") % item
        print ("")
    elif pick == c2:
        print ("已取消" + cancel + ",未执行任何操作")
        runpy(ssrfile)
    else:
        print ("输入不正确，请输入 " + c1 + " 或 " + c2)
        runpy(ssrfile)

# 将 IP 地址转换成 16 进制，再去掉中间的 "." 后转换成 10 进制
def ip_into_int(ip):
    # 如：(((((192 * 256) + 168) * 256) + 1) * 256) + 13 
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

# 判断本机 IP 地址是否是内网IP
def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

# 此方法的原理是利用 UDP 协议来实现的，生成一个 UDP 包，将发送包的 IP 记录在 UDP 协议头中，然后从 UDP 包中获取本机 IP
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

if __name__ == '__main__':
    ip = get_host_ip()

# 如果是内网 IP 需要进行的操作
def look_ip_from():
    context = ssl._create_unverified_context()
    thisip = urllib2.urlopen('https://ipv4.icanhazip.com/', context=context).read()
    thisip = thisip.strip()
    return thisip

# 生成 SSR 链接
def GetSsrUrl(IP, Port, Protocol, Method, Obfs, base64Pwd, SecondPart):
    parts = [IP, Port, Protocol, Method, Obfs, base64Pwd]
    configs = str(':'.join(parts))
    RealSsrUrl = configs + SecondPart
    base64SsrUrl = str(base64.encodestring(RealSsrUrl))
    base64SsrUrl = base64SsrUrl.replace("\n", "")
    SsrUrl = "ssr://" + base64SsrUrl
    return SsrUrl

