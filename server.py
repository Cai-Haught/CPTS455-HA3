import socket
import threading
import os
import time
HOST = "127.0.0.1"
PORT = 8000

def recv_data(conn):
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        if not data:
            break
        if data == "file":
            receive_file_thread = threading.Thread(target=receive_file, args=(conn,))
            receive_file_thread.start()
            receive_file_thread.join()
        else:
            print(f"[client] {data}")


def send_data(conn):
    while True:
        msg = input()
        conn.sendall(msg.encode("utf-8"))
        if msg == "file":
            send_file_thread = threading.Thread(target=send_file, args=(conn,))
            send_file_thread.start()
            send_file_thread.join()

def send_file(conn):
    file_name = input("Enter file name: ")
    conn.sendall(file_name.encode("utf-8"))
    print("file transferring...")
    try:
        f = open(file_name, "r")
        cwd = os.getcwd()
        file_size = str(os.path.getsize(cwd + "\\" + file_name))
        conn.sendall(file_size.encode("utf-8"))
        time.sleep(0.2)
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.sendall(data.encode("utf-8"))
        f.close()
        print("completed")
    except IOError:
        print("Invalid file name")

def receive_file(conn):
    bytes_read = 0
    file_name = "server_" + conn.recv(1024).decode("utf-8")
    f = open(file_name, "w")
    print("receiving file...")
    file_size = conn.recv(1024).decode()
    while bytes_read  < int(file_size):
        data = conn.recv(1024).decode("utf-8")
        f.write(data)  
        bytes_read += 1024
    print("file transfer successful")
    print("new file name", file_name)
    f.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(0)
print(f"Listening on {HOST}:{PORT}")
conn, addr =  s.accept()
print(f"Connected by {addr}")


recv_thread = threading.Thread(target=recv_data, args=(conn,))
send_thread = threading.Thread(target=send_data, args=(conn,))
recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()
conn.close()
print("connection closed")
s.close()


