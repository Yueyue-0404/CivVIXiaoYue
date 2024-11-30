from basic.bot_process import *
from botpy import errors
import datetime, traceback

if __name__ == "__main__":
    client = CivVIBot()
    client.run(appid=test_config["appid"], secret=test_config["secret"])
