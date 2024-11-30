"""
这是个yaml写入器
"""
import yaml

command_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # 日志格式
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
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
            'propagate': False,
        },
    },
}

with open('log_config.yaml', 'w') as f:
    yaml.dump(command_dict, f)
