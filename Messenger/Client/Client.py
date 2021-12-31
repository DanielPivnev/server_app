import time
from socket import AF_INET, SOCK_STREAM, socket

from Messenger.Common.Settings import DEFAULT_PORT, ACTION, ACCOUNT_NAME, TIME, USER, PRESENCE, DEFAULT_IP_ADDR, \
    RESPONSE, EMAIL, PASSWORD, AUTHENTICATE, REGISTER
from Messenger.Common.Utils import receive, send


def create_presence(account_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return response


def registration(account_name, email, password1, client):
    data = {
        ACTION: REGISTER,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            EMAIL: email,
            PASSWORD: password1
        }
    }

    send(client, data)


def authentication(account_name, password, client):
    data = {
        ACTION: AUTHENTICATE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD: password
        }
    }

    send(client, data)


def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

    while receive(client)[RESPONSE] != 200:
        presence_message = create_presence()
        send(client, presence_message)

    print('Presence: 200 OK')

    answer = {}
    flag = True
    while flag:
        choice = int(input('If you want to login enter 1 or if you do not have an account enter 2 for registration: '))

        if choice == 1:
            account_name = input('Username: ')
            password = input('Password: ')

            authentication(account_name, password, client)
            answer = receive(client)

            flag = False

        elif choice == 2:
            account_name = input('Username: ')
            email = input('E-mail: ')
            password1 = input('Password: ')
            password2 = input('Password (again): ')

            while password1 != password2:
                password1 = input('Password: ')
                password2 = input('Password (again): ')

            registration(account_name, email, password1, client)
            answer = receive(client)

            flag = False
        else:
            print('Please enter just 1 or 2.')

    client.close()


if __name__ == '__main__':
    main()
