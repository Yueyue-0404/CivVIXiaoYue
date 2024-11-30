from basic.bot_process import *


if __name__ == "__main__":
    client = CivVIBot()
    client.run(appid=test_config["appid"], secret=test_config["secret"])
