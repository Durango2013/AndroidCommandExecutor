from fastapi import FastAPI, HTTPException
from typing import Any
from ppadb.client import Client as AdbClient

app = FastAPI()

# Create client for communicating with Android device or emulator running
# Only setup a device or emulator and not both
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
if devices:
    device = devices[0]

@app.get("/", status_code=200)
async def root() -> str:
    """
    Root GET
    """
    return "Hello, World!"

# This will POST endpoint will take a single string representing an ADB shell command
# See the following for supported commands: https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8
# Some test examples:
# curl -X POST "http://localhost:8000/android_cmd/?cmd=ls"  # lists files from Android filesystem root path ("/")
# curl -X POST "http://localhost:8000/android_cmd/?cmd=input%20keyevent%205" # brings up phone app
# curl -X POST "http://localhost:8000/android_cmd/?cmd=dumpsys%20battery" # shows device battery info 
@app.post("/android_cmd/", status_code=201)
async def send_command(cmd: str) -> str:
    result = device.shell(cmd)
    print(result)
    return result 
