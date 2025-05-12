import jameschat


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

        while True:
            print("\n Allowing Connection...")
            this_inst.allow_connection()
            print("Connection Successful!")

    elif choice == "2":

        this_inst = jameschat.JameschatClient()
        this_inst.set_username(username)
        ipy = input("Enter server IP\n> ")
        porty = int(input("Enter server port\n> "))

        this_inst.connect_to_server(ipy, porty)
        print("Connection Successful!")


if __name__ == "__main__":
    main()
