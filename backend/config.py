import os, json
from pathlib import Path
from constants import ERROR_MESSAGES

try:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv("../.env"))
except ImportError:
    print("dotenv not installed, skipping...")

WEBUI_NAME = "Bulletin Board"

ENV = os.environ.get("ENV", "dev")

try:
    with open(f"../package.json", "r") as f:
        PACKAGE_DATA = json.load(f)
except:
    PACKAGE_DATA = {"version": "0.0.0"}

VERSION = PACKAGE_DATA["version"]

DATA_DIR = str(Path(os.getenv("DATA_DIR", "./data")).resolve())
FRONTEND_BUILD_DIR = str(Path(os.getenv("FRONTEND_BUILD_DIR", "../build")))

try:
    with open(f"{DATA_DIR}/config.json", "r") as f:
        CONFIG_DATA = json.load(f)
except:
    CONFIG_DATA = {}

CACHE_DIR = f"{DATA_DIR}/cache"
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

####################################
# WEBUI_VERSION
####################################

WEBUI_VERSION = os.environ.get("WEBUI_VERSION", "v1.0.0-alpha.100")

####################################
# WEBUI_AUTH (Required for security)
####################################

WEBUI_AUTH = True

####################################
# WEBUI_SECRET_KEY
####################################

WEBUI_SECRET_KEY = os.environ.get(
    "WEBUI_SECRET_KEY",
    os.environ.get(
        "WEBUI_JWT_SECRET_KEY", "t0p-s3cr3t"
    ),  # DEPRECATED: remove at next major version
)

if WEBUI_AUTH and WEBUI_SECRET_KEY == "":
    raise ValueError(ERROR_MESSAGES.ENV_VAR_NOT_FOUND)