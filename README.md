# ftp-FileServer
技術點:

服務端與客戶端使用**socket模塊**函式組合，運用**傳輸層tcp流式套接字**傳輸，將每個功能用**函式**封裝。
   1. 客戶端利用sys.argv綁定用戶啟動程序時命令行參數，並透過**判斷式**判斷服務器發送訊息功能為何。
   2. 服務端使用**os模塊**處理與判斷文件，使用**fork多進程**支援多用戶同時登陸操作，以及使用signal函式避免殭屍進程的產生占用系統資源。
   
-----------------------------------------------------------------------   
# 項目功能:

# 服務端和客戶端兩部分，要求啟動一個服務端，可以同時處理多個客戶端請求

  ![image](https://github.com/dian0624/ftp-FileServer/blob/master/FileServer_image/1583727107550.jpg)

## 1. 可以查看服務端文件庫中所有的普通文件

  ![image](https://github.com/dian0624/ftp-FileServer/blob/master/FileServer_image/54665.jpg)
          
## 2. 客戶端可以下載服務端文件庫的文件到本地

  ![image](https://github.com/dian0624/ftp-FileServer/blob/master/FileServer_image/1583727095154.jpg)   
          
## 3. 可以將本地文件上傳的服務端文件庫

  ![image](https://github.com/dian0624/ftp-FileServer/blob/master/FileServer_image/158372709515456.jpg) 

## 4. 退出


