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
        print("data recieved")
        converted_data = json.loads(received_data)
        return converted_data

    def ptp(self, payload):
        # pack the payload
        stringify = json.dumps(payload)
        encoded = stringify.encode()
        return encoded

    def orchestrator(self):
        recieved_data: dict = self.recv_and_convert_to_json()
        print(recieved_data)

        if recieved_data["action"] == 1337:
            print(recieved_data["data"])
            response = self.ptp({"action": 1337, "data": {"msg": "message recieved"}})
            self.connection.sendall(response)




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

