import argparse, os
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--language", required=False,default="pt-br", type=str)
parser.add_argument("--service", required=False, default="null", type=str)
arguments = parser.parse_args()

LANGUAGE = arguments.language
SERVICE_TYPE = arguments.service
REPOSITORY_UUID = "c4bf350f-e678-490e-b5ca-c0a2b1b52b93"
AUTH_TOKEN = load_dotenv(AUTH_TOKEN)

print(AUTH_TOKEN)


