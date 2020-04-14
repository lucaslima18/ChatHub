from settings import *

# from functions import *


def getService(SERVICE_TYPE):
    if SERVICE_TYPE == "training" or SERVICE_TYPE == "1":
        print("criar treinos")
        # readIntents()
        # runTraining()

    elif SERVICE_TYPE == "testing" or SERVICE_TYPE == "2":
        print("cirar testes")
        # readIntents()
        # runTesting()

    elif SERVICE_TYPE == "clear" or SERVICE_TYPE == "3":
        sure = input("Tem certeza que deseja deletar? [y/n]\n")

        if sure == "y":
            print("limpando")
            # delete_all()

        elif sure == "n":
            pass

    elif SERVICE_TYPE == "info" or SERVICE_TYPE == "4":
        print("###### INFORMATION ######")
        print(
            "this app is an integration between the chatito phrase creation platform and the bothub artificial intelligence development platform."
        )
        print("to learn more about the project visit: (https://github.com/lucaslima18/ChatHub)")

    elif SERVICE_TYPE == "close" or SERVICE_TYPE == "0":
        print("bye...")
        exit()

    else:
        print(
            "\nThis option is not avaliable, please reload and try one of this options:\n"
        )
        services = ["Training\nTests\nClear\nInfo\nClose\n"]


if SERVICE_TYPE == "null":
    binary_answer = ""
    print("################################")
    print("###### WELCOME TO CHATHUB ######")

    while binary_answer != "n":
        print("############# MENU #############\n")
        services = ["[1] Training", "[2] Tests", "[3] Clear", "[4] Info", "[0] Close\n"]

        for service in services:
            print(f"{service}")

        SERVICE_TYPE = input("please choice the service: ")
        getService(SERVICE_TYPE)
        binary_answer = input("\nwant to do another service? [y/n] ")

else:
    getService(SERVICE_TYPE)
