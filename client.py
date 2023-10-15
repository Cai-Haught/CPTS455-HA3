import socket
import threading
import os
import time
HOST = "127.0.0.1"
PORT = 8000

def recv_data(s):
    while True:
        response = s.recv(1024)
        response = response.decode("utf-8")
        if not response:
            break
        if response == "file":
            receive_file_thread = threading.Thread(target=receive_file, args=(s,))
            receive_file_thread.start()
            receive_file_thread.join()
        else:
            print(f"[server] {response}")

def send_data(s):
    while True:
        msg = input()
        s.sendall(msg.encode("utf-8"))
        if msg == "file":
            send_file_thread = threading.Thread(target=send_file, args=(s,))
            send_file_thread.start()
            send_file_thread.join()
        

def send_file(s):
    file_name = input("Enter file name: ")
    s.sendall(file_name.encode("utf-8"))
    print("file transferring...")
    try:
        f = open(file_name, "r")
        cwd = os.getcwd()
        file_size = str(os.path.getsize(cwd + "\\" + file_name))
        s.sendall(file_size.encode("utf-8"))
        time.sleep(0.2)
        while True:
            data = f.read(1024)
            if not data:
                break
            s.sendall(data.encode("utf-8"))
        f.close()
        print("completed")
    except IOError:
        print("Invalid file name")

def receive_file(s):
    bytes_read = 0
    file_name = "client_" + s.recv(1024).decode("utf-8")
    f = open(file_name, "w")
    print("receiving file...")
    file_size = s.recv(1024).decode()
    while bytes_read  < int(file_size):
        data = s.recv(1024).decode("utf-8")
        f.write(data)  
        bytes_read += 1024
    print("file transfer successful")
    print("new file name", file_name)
    f.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

recv_thread = threading.Thread(target=recv_data, args=(s,))
send_thread = threading.Thread(target=send_data, args=(s,))
recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()
s.close()


