# Author:ZJF
import urllib.request
file = urllib.request.urlopen("http://www.baidu.com")
data = file.read()
dataline = file.readline()
print(data)
fhandle=open("D:\\python\\web_spider\\Urllib_model\\1.html","wb")
fhandle.write(data)
fhandle.close()