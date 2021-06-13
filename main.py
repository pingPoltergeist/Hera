import os
import socket
from pathlib import Path
from GUI import HeraGUI
import tkinter as tk


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


if __name__ == '__main__':

    LOCAL_IP = get_ip()
    BASE_DIR = Path(os.getcwd())

    window = tk.Tk()
    heraGUI = HeraGUI(
        instance=window,
        base_dir=BASE_DIR,
        ip=LOCAL_IP,
        media_url='media/'
    )
    heraGUI.start_app()
