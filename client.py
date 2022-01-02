'''Программа-клиент'''
import json
import socket
import sys
import time

from common.utils import get_message, send_message
from common.variables import *


def create_presence(account_name='Guest'):
    '''
    Фунекция генерирует запрос в присутсвии клиента
    :param account_name:
    :return:
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    '''
    Фукнция разбирает ответ сервера
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    '''Загружаем параметры командной строки'''
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535')
        sys.exit(1)

    # Инициализация сокета и обмена
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
        transport.close()
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера')
        transport.close()


if __name__ == '__main__':
    main()