import logging
import logging.handlers
import datetime

'''
使用方法返回日志器
'''
def logger1():
    # 日志器，提供接口给代码调用
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG) # 设置统一的日志级别

    # 处理器1，设置日志位置，日志格式
    rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 处理器2，设置日志位置，日志格式
    f_handler = logging.FileHandler('error.log')
    f_handler.setLevel(logging.ERROR) # 设置自己的日志级别
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    # 一个日志器设置多个处理器
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)

    return logger

def logger2():
    # 日志器，提供接口给代码调用
    logger = logging.getLogger('mylogger2')
    logger.setLevel(logging.DEBUG) # 设置统一的日志级别

    # 处理器1，设置日志位置，日志格式
    rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 处理器2，设置日志位置，日志格式
    f_handler = logging.FileHandler('error.log')
    f_handler.setLevel(logging.ERROR) # 设置自己的日志级别
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    # 一个日志器设置多个处理器
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)

    return logger

'''
把日志器定义为全局属性
'''
#日志器，提供接口给代码调用
logger = logging.getLogger('mylogger3')
logger.setLevel(logging.DEBUG) # 设置统一的日志级别

# 处理器1，设置日志位置，日志格式
rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# 处理器2，设置日志位置，日志格式
f_handler = logging.FileHandler('error.log')
f_handler.setLevel(logging.ERROR) # 设置自己的日志级别
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

# 一个日志器设置多个处理器
logger.addHandler(rf_handler)
logger.addHandler(f_handler)


if __name__ == '__main__':
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')
    pass