import json
import socket
from threading import Thread


class Client():

    def __init__(self, s):
        self.socket: socket = s

    def print_choices(self):
        print("\nWelcome to the bank, what do you want to do?")
        print("1. Add an account")
        print("2. View all accounts")
        print("3. View specific account info")

    def orchestrator(self):
        self.print_choices()

        # packar ihop payload
        # payload = self.ptp({"action": 1337, "data": {"test": 1234}})
        choice = int(input("Enter action: "))

        payload = self.ptp({"action": choice})
        self.socket.sendall(payload)  # skickar payload
        response = self.recv_and_convert_to_json()  # väntar på svar och avkodar
        print(response)  # visar datat

        print("PROGRAM IS FINISHED")

    def ptp(self, payload):
        # pack the payload
        stringify = json.dumps(payload)
        encoded = stringify.encode()
        return encoded

    def recv_and_convert_to_json(self):
        received_data = self.socket.recv(1024).decode()
        converted_data = json.loads(received_data)
        return converted_data

    def convert_customer_data(self):
        recvd_data = self.recv_and_convert_to_json()
        print(type(recvd_data))
        i = 1
        for info in recvd_data["accounts"]:
            print(f"Customer #{i}")
            print("Name:", info["name"])
            i = i+1
            print("")


def main():
    HOST = "127.0.0.2"
    PORT = 50009

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # while True:
            client = Client(s)
            client.orchestrator()
            # Thread(target=client.orchestrator, args=()).start()
    except:
        s.close()
        print("something fuckedup")


if __name__ == "__main__":
    main()
