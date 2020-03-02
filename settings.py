import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("--repository_uuid", required=True, type=str)
parser.add_argument("--auth_token", required=True, type=str)
parser.add_argument("--language", required=False,default="pt-br", type=str)
parser.add_argument("--service", required=True, type=str)
arguments = parser.parse_args()

REPOSITORY_UUID = arguments.repository_uuid
LANGUAGE = arguments.language
AUTH_TOKEN = arguments.auth_token

if (
    arguments.service == "clear"
    or arguments.service == "testing"
    or arguments.service == "training"
):
    SERVICE_TYPE = arguments.service

else:
    #deixar textos mais completos aqui
    print("\nThis option is not avaliable, please reload and try one of this options:\n")
    print("clear\ntesting\ntraining\n")
    exit()

