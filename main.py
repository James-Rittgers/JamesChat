import jameschat
import threading 
import sys

def get_user_input():
    
    while True:
        try:
            input('> ')

        except EOFError:
            print("\nCtrl+C doesn't work :(")

def main():
    print("Welcome to JamesChat!")

    username = input("\n\nEnter username:\n> ")

    choice = input("Enter:\n[1] to host a room\n[2] to join a room\n\n> ")

    if choice == "1":

        this_inst = jameschat.JameschatServer()
        this_inst.set_username(username)
        ip_address = this_inst.ip_address
        port = this_inst.recv_port

        print("Hosting a chat\n")
        print(f"Your IP: {ip_address}\nYour port: {port}")

    elif choice == "2":

        this_inst = jameschat.JameschatClient()
        this_inst.set_username(username)
        ipy = input("Enter server IP\n> ")
        porty = int(input("Enter server port\n> "))

        this_inst.connect_to_server(ipy, porty)
        print("Connection Successful!")

    network_thread = threading.Thread(target=this_inst.run_networking)
    input_thread = threading.Thread(target=get_user_input) 

    input_thread.start()
    network_thread.start()

if __name__ == "__main__":
    main()