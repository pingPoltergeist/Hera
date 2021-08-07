import os
import socket
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception as ex:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


port = int(os.environ.get('PORT')) if os.environ.get('PORT') else 5201
PROTOCOL = 'http'
LOCAL_IP = get_ip()
BACK_PORT = port + 1

with open(BASE_DIR / 'front\\.env', 'w', encoding='utf-8') as f:
    print('Writing configurations ...')
    f.write(
        'NEXT_PUBLIC_API={protocol}://{local_ip}:{back_port}/api/v1'.format(
            protocol=PROTOCOL,
            local_ip=LOCAL_IP,
            back_port=BACK_PORT
        ) + '\n' +
        'NEXT_PUBLIC_BACKEND={protocol}://{local_ip}:{back_port}'.format(
            protocol=PROTOCOL,
            local_ip=LOCAL_IP,
            back_port=BACK_PORT
        )
    )

os.chdir(BASE_DIR / 'front')
print('Starting npm build...')
os.system(r'.\venv\npm run build')
print('Build completed :)')
