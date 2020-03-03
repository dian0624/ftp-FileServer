from socket import *
import os,sys
import signal
import time 

file_path = "/home/ubuntu/aaa/"
HOST = ""
PORT = 8888
ADDR = (HOST,PORT)


class FtpServer(object):
    def __init__(self,c):
        self.c = c

    def show_files(self):
        file_list = os.listdir(file_path)
        if not file_list:
            self.c.send('文件庫文為空'.encode())
            return 
        else:
            self.c.send(b'ok')
            time.sleep(0.1)

        files = ''
        for file in file_list:
            if file[0] !='.' and \
            os.path.isfile(file_path + file) :
                files = files + file + "#"
        self.c.sendall(files.encode())

    def download_file(self):
        file_name = self.c.recv(1024).decode()
        try:
            f = open("%s"%(file_path+file_name),'rb')
        except:
            self.c.send("文件不存在".encode())
            return
        self.c.send(b"ok")
        time.sleep(0.1)

        while True:
            data = f.read(1024)
            if not data :
                time.sleep(0.1)
                self.c.send(b'##')
                break
            self.c.send(data)
        print("文件發送完畢")

    def upload_file(self):
        file_name = self.c.recv(1024).decode()
        try:
            f = open(file_path+file_name,"wb")
        except:
            self.c.send("文件上傳失敗！".encode())
            return
        self.c.send(b'ok')

        while True:
            data = self.c.recv(1024)
            if data == b"##":
                break
            f.write(data)
        f.close()

        self.c.send("文件已收到\n".encode())
        print("文件接收成功")


def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("Listen the port 8888....")

    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            sys.exit("服務器退出")
        except Exception as e:
            print("**Error:",e)
            continue
        print("已連接客戶端:",addr)
            
        pid = os.fork()
        if pid == 0 :
            s.close()
            
            fs = FtpServer(c)
            while True:
                data = c.recv(1024).decode()
                if not data or data == "E":
                    sys.exit("客戶端退出")
                elif data == "L":
                    fs.show_files()
                elif data == "D":
                    fs.download_file()
                elif data == "U":
                    fs.upload_file()
        else:
            c.close()
            continue

if __name__ == "__main__":
    main()
