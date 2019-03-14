import json
import socket
import argparse
from datetime import datetime


def sys_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-addr', default='')
    parser.add_argument('-port', default=7777)

    return parser


def recv_message():
    while True:
        client, address = sock.accept()
        print(f'Client detected {address}')
        data = client.recv(1024)
        request = json.loads(
            data.decode('utf-8')
        )

        send_answer(client, make_answer(request))


def make_answer(user_request):
    if user_request.get('action') == 'status_check':
        response_string = "Ok"

        request_json = json.dumps(
            {
                'response': 200,
                'message': response_string
            }
        )

        return request_json


    elif user_request.get('action') == 'get_time':
        date = datetime.now()
        response_string = date.strftime('%d-%m-%yT%H:%M:%S')

        request_json = json.dumps(
            {
                'response': 200,
                'message': response_string
            }
        )

        return request_json


    elif user_request.get('action') == 'upper_text':
        client_data = user_request.get('data')
        response_string = client_data.upper()
        request_json = json.dumps(
            {
                'response': 200,
                'message': response_string
            }
        )

        return request_json


    else:
        response_string = 'Wrong action error'
        request_json = json.dumps(
            {
                'response': 400,
                'message': response_string
            }
        )

        return request_json


def send_answer(clt, req_json):
    clt.send(req_json.encode('utf-8'))
    clt.close()


if __name__ == "__main__":
    parser = sys_arg_parser()
    args = parser.parse_args()

    sock = socket.socket()
    sock.bind((args.addr, int(args.port)))
    sock.listen(5)
    recv_message()
