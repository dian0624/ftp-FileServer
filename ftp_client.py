from socket import *
import sys
import time


class FtpClient(object):
	def __init__(self,s):
		self.s = s

	def menu(self):
		print(" --------------------- ")
		print("| "+"1. 查看文件庫內容  "+" |")
		print("| "+"2. 下載文件庫文件  "+" |")
		print("| "+"3. 上傳文件至文件庫"+" |")
		print("| "+"4. 退出            "+" |")
		print(" --------------------- ")
    
	def show_files(self):
		self.s.send(b'L')

		info = self.s.recv(1024).decode()

		if info  == "ok":
			data = self.s.recv(2048).decode()
			files = data.split("#")
			for file in files:
				print(file)
			print("文件展示完畢\n")
		else:
			print(data.decode())

	def download_file(self):
		self.s.send(b'D')

		file_name = input("請輸入想下載的文件名稱：")
		self.s.send(file_name.encode())

		info = self.s.recv(1024).decode()
		if info == 'ok':
			print("開始下載")
			f = open(file_name,'wb')
			while True:
				data = self.s.recv(1024)
				if data == b'##':
					break 
				f.write(data)

			print("下載完成 \n")
			f.close()
		else:
			print("Error")
			return

	def upload_file(self):
		self.s.send(b"U")

		file_name = input("請輸入要上傳的文件名：")
		self.s.send(file_name.encode())
		time.sleep(0.5)

		try:
			f = open(file_name,"rb")
		except Exception as e:
			print("找不到文件,讀取失敗",e)
			return
		
		info =  self.s.recv(1024).decode()
		if info == "ok":
			while True:
				data = f.read(1024)
				if not data :
					time.sleep(0.1)
					self.s.send(b"##")
					break
				self.s.send(data)
			f.close()

			info = self.s.recv(1024)
			print(info.decode())

		else:
			print(info)    

	def client_exit(self):
		self.s.send(b"E")
		self.s.close()
		sys.exit("退出連結")


def main():
	if len(sys.argv) < 3:
		print('argv is error')
		return
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST,PORT) #文件服務器地址

	s = socket()
	try:
		s.connect(ADDR)
	except:
		print("連接服務器失敗")
		return

	fc = FtpClient(s)

	while True:
		fc.menu()
		cmd = input("輸入請求命令>>")
		if not cmd:
			break
		elif cmd == "1":
			fc.show_files()
		elif cmd == "2":
			fc.download_file()
		elif cmd == "3":
			fc.upload_file()
			time.sleep(0.2)
		elif cmd == "4":
			fc.client_exit()
		else:
			print("請輸入正確命令！")
			continue
		s.send(cmd.encode())

	s.close()

if __name__ == '__main__':
	main()

