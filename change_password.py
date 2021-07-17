import requests
import sys


def change_password(old, new):
    response = requests.post(
        'http://127.0.0.1:5000/change_password',
        data={'old_password': old, 'new_password': new})
    print("Old password:", old)
    print("New password:", new)
    print("Result:")
    print(response.status_code)
    print(response.reason)
    print(response.text)


if __name__ == '__main__':
    argv = sys.argv[1:]
    change_password(*argv)
