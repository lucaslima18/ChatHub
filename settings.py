import argparse, os
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("--language", required=False,default="pt_br", type=str)
parser.add_argument("--service", required=False, default="null", type=str)
parser.add_argument("--repository_uuid", required=False, default="null", type=str)
arguments = parser.parse_args()

LANGUAGE = arguments.language
SERVICE_TYPE = arguments.service
REPOSITORY_UUID = arguments.repository_uuid
AUTH_TOKEN = ""


