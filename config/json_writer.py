import json
from pathlib import Path

data = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': "./log/XiaoYueLog.log",
            'when': 'midnight',  # 每天午夜轮换
            'interval': 1,      # 间隔一天
            'backupCount': 30  # 保留一个月
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



def write_into_json(json_path: Path, data: dict or list):
    with open(json_path, mode="w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


write_into_json(Path.cwd().joinpath("log_config.json"), data)
