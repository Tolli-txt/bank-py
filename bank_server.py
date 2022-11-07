'''
Krav för G
TODO: Du kan lägga till en kund i registret - Klar
TODO: Du kan fråga servern om vilka kunder som finns - Klar
TODO: Du kan fråga om detaljer för en specifik kund - Klar
TODO: Du skriver något enhetstest - Försök skriva så många som möjligt,
försök dela upp funktioner om det går?

"bank-server.py" ska vara server
"bank-client.py" ska vara klient
Måste göra så att servern exekverar funktioner 
beroende på input från klient

TODO: Gör om funktionerna för att skicka data till klienten.
ta inspiration från funktionen för att visa alla konton.
'''

import json
import socket
from threading import Thread

from pprint import pprint


class Customer:

    def __init__(self, connection, addr):
        self.connection = connection
        self.addr = addr
        self.accounts_file = "accounts/accounts.json"
        self.accounts_file_test = "accounts/accounts_test.json"

    def recv_and_convert_to_json(self) -> dict:
        received_data = self.connection.recv(1024).decode()
        print(f"Data received from {self.addr}")
        converted_data = json.loads(received_data)
        return converted_data

    def ptp(self, payload):
        # pack the payload
        stringify = json.dumps(payload)
        encoded = stringify.encode()
        return encoded

    def orchestrator(self):
        received_data: dict = self.recv_and_convert_to_json()
        print(received_data)

        if received_data["action"] == 1337:
            print(received_data["data"])
            response = self.ptp(
                {"action": 1337, "data": {"msg": "message received"}})
            self.connection.sendall(response)

        elif received_data["action"] == 2:
            print(received_data["action"])
            all_accounts = self.view_accounts_list()
            response = self.ptp({"action": 2, "data": all_accounts})
            self.connection.sendall(response)

        elif received_data["action"] == 1:
            print(received_data["data"])

    def view_accounts_list(self):
        with open(self.accounts_file_test) as accounts:
            data = json.load(accounts)
        return data

    def add_new_account(self, new_name, new_balance):
        name = new_name
        balance = new_balance
        new_acc_dict = {
            "name": name,
            "balance": balance
        }
        self.write_to_json(new_data=new_acc_dict,
                           filename=self.accounts_file_test)

    def write_to_json(self, new_data, filename):
        with open(filename, "r+") as accounts_open:
            data = json.load(accounts_open)
            data["accounts"].append(new_data)
            accounts_open.seek(0)
            json.dump(data, accounts_open, indent=4)


def main():
    HOST = "127.0.0.2"
    PORT = 50009

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print("Server is running...")
        try:
            while True:
                conn, addr = s.accept()
                print(f"Connection from: {addr}")
                bank1 = Customer(conn, addr)
                bank1.orchestrator()
                # Thread(target=bank1.orchestrator, args=()).start()
        except KeyboardInterrupt:
            s.close()
            exit(1)
        except Exception as e:
            s.close()
            print("Unexpected exception")
            print(e)
            exit(1)


if __name__ == "__main__":
    main()
