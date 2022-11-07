import json
import socket
from threading import Thread
from pprint import pprint


class Client():

    def __init__(self, s):
        self.socket: socket = s
        self.client_accounts_file = 'accounts/client_accounts.json'
        self.client_new_acc_file = 'accounts/client_new_account.json'

    def print_choices(self):
        print("\nWelcome to the bank, what do you want to do?")
        print("1. Add an account")
        print("2. View all accounts")
        print("3. View specific account info")

    def orchestrator(self):
        self.print_choices()

        # packar ihop payload
        # payload = self.ptp({"action": 1337, "data": {"test": 1234}})
        action = int(input("Enter action: "))

        payload = self.ptp({"action": action})
        self.socket.sendall(payload)  # skickar payload

        response = self.convert_customer_data()  # väntar på svar och avkodar
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

    def dump_to_json(self):
        new_data = self.recv_and_convert_to_json()
        with open(self.client_accounts_file, "r+") as clients:
            data = json.load(clients)
            data = []
            data.append(new_data)
            clients.seek(0)
            new_info = json.dump(data, clients, indent=4)
        return new_info

    def handle_response(self, server_data):
        server_data = self.recv_and_convert_to_json()
        if server_data[""]:
            pass

    def new_account_input(self):
        name_input = input("Enter customers name: ")
        balance_input = int(input("Enter account balance: "))
        both_inputs = name_input + balance_input
        payload = self.ptp(both_inputs)
        return payload

    def new_account_dump(self):
        new_acc = self.new_account_input()
        with open(self.client_new_acc_file, "w") as f:
            data = json.load(f)
            data.append(new_acc)
        # lägg till något sätt att lägga in som dict

    def convert_customer_data(self):
        data = self.dump_to_json()
        # recvd_data = self.socket.recv(1024).decode()
        # converted_data = json.loads(recvd_data)
        # print(type(converted_data))
        # i = 1
        # for info in data["data"]["accounts"]:
        #     print(f"Customer #{i}")
        #     print(f"Name:", info["name"])
        #     i = i+1
        #     print("")
        print(type(data))
        # pprint(data)

    def handle_send_choice(self, choice):
        if choice == 1:
            self.new_account_input()
        elif choice == 2:
            payload = self.ptp({"action": choice})
            self.socket.sendall(payload)
        return choice


def main():
    HOST = "127.0.0.2"
    PORT = 50009

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # while True:
        client = Client(s)
        client.orchestrator()

    # client.orchestrator()
    # Thread(target=client.orchestrator, args=()).start()


if __name__ == "__main__":
    main()

    # def cases(self, argument):
    #     case_choice = argument
    #     match case_choice:
    #         case "all accounts":
    #             return self.convert_customer_data()
    #         case "specific account":
    #             pass

    # def handle_response(self, argument):
    #     if argument["action"] == 1:
    #         self.convert_customer_data()
    #     elif argument["data"] == "nothing":
    #         pass
    #     return


# def main():
#     HOST = "127.0.0.2"
#     PORT = 50009

#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((HOST, PORT))
#             # while True:
#             client = Client(s)
#             client.orchestrator()

#         # client.orchestrator()
#         # Thread(target=client.orchestrator, args=()).start()
#     except:
#         s.close()
#         print("something fuckedup")
