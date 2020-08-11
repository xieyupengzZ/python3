# datetime模块，其中包括 date，time，datetime 等类
import datetime


def dateTest():
    print('*' * 20, 'date类', '*' * 20)
    date = datetime.date
    today = date.today()
    print('单独返回每个元素', today.year, today.month, today.day)
    print('直接返回字符串', today.isoformat())
    print(today.ctime())
    print(today.weekday(), '[0-6,0表示星期一]')
    print(today.isoweekday(), '[1-7,1表示星期一]')
    print('距0001年1月1日已经过了多少天', today.toordinal())
    print('距0001年1月1日的天数转换成日期', date.fromordinal(737610))
    print('根据时间戳转换成日期', date.fromtimestamp(1593852969.72))
    print('字符串 → 日期，只能间隔横杆', date.fromisoformat('2020-07-04'))
    print('日期 → 字符串，可间隔任意字符', today.strftime('%Y/%m/%d'),
          today.strftime('%Y%m%d'), today.strftime('%Y@%m@%d'))


def timeTest():
    print('*' * 20, 'time类', '*' * 20)
    time = datetime.time
    now = time(17, 20, 59, 8888)
    print('单独返回每个元素', now.hour, now.minute, now.second, now.microsecond)
    print('直接返回字符串', now.isoformat())
    print('时间 → 字符串，可间隔任意字符', now.strftime('%H-%M-%S'),
          now.strftime('%H/%M/%S'), now.strftime('%H@%M@%S'))


def datetimeTest():
    print('*' * 20, 'datetime类(继承date)', '*' * 20)
    dt = datetime.datetime
    today = dt.today()
    now = dt.now()  # 等同于today
    print('today()', today)
    print('now()', now)
    print('时间戳(秒)', now.timestamp())
    print('单独返回每个元素', today.year, today.month, today.day, today.hour,
          today.minute, today.second, today.microsecond)
    print('星期几', today.isoweekday())
    print('返回日期对象，时间对象', today.date(), today.time())
    print('时间戳 → datetime，', dt.fromtimestamp(now.timestamp()))
    print('字符串 → datetime，时间字符串，日期只能间隔横杆，时间只能间隔冒号',
          dt.fromisoformat('2020-07-04 17:39:30'))
    print('字符串 → datetime，时间字符串和格式字符串，同上',
          dt.strptime('2020-07-04 17:39:30', '%Y-%m-%d %H:%M:%S'))
    print('datetime → 字符串，可间隔任意字符', today.strftime('%Y/%m/%d %H/%M/%S'),
          today.strftime('%Y-%m-%d %H:%M:%S'))
    print('datetime → 字符串，默认间隔是T，可替换；默认是微秒，可替换成毫秒', today.isoformat(),
          today.isoformat(' ', 'milliseconds'))


def timedeltaTest():
    print('*' * 20, 'timedelta类', '*' * 20)
    now = datetime.datetime.now()
    timedelta = datetime.timedelta
    print('两天后', now + timedelta(2))
    print('两天前', now + timedelta(-2))
    print('三小时后', now + timedelta(hours=3))
    print('三小时前', now + timedelta(hours=-3))
    print('四十分钟后', now + timedelta(minutes=40))
    print('一个星期后', now + timedelta(weeks=1))


'''
北京时间是UTC+8:00时区的时间
datetime类型有一个时区属性tzinfo，默认为None，默认不带时区标识
利用带时区的datetime，通过astimezone()方法，可以转换到任意时区

datetime表示的时间需要时区信息才能确定一个特定的时间，否则只能视为本地时间
如果要存储datetime，最佳方法是将其转换为timestamp再存储，timestamp与时区无光
'''


def timezoneTest():
    time = datetime.datetime
    zone = datetime.timezone
    timedelta = datetime.timedelta
    now = time.now()
    print('当前时间', now)
    utcnow = now.utcnow()
    print('utcnow获取UTC+0:00时区的时间', utcnow)
    tz_utc_8 = zone(timedelta(hours=8))  # 创建时区 UTC+8:00
    now = now.replace(tzinfo=tz_utc_8)  # 强制设置时区 UTC+8:00
    print('当前时间加上时区标识', now)
    tz_utc_9 = zone(timedelta(hours=9))  # 带时区的datetime可以转换成任意时区时间（此处是东9区，东京时间）
    now_utc_9 = now.astimezone(tz_utc_9)
    print('转换成UTC+9:00时区的时间', now_utc_9)


if __name__ == '__main__':
    print()
    print('*' * 20, 'datetime模块的类', '*' * 20)
    print(datetime.datetime, datetime.date, datetime.time, datetime.timedelta,
          datetime.timezone, datetime.tzinfo)
    print()
    print('*' * 20, '注意事项', '*' * 20)
    print('时间格式化的时候，python最终调用的都是平台的C函数，不同平台格式的支持可能会有所不同，注意自测')
    print()
    # dateTest()
    # timeTest()
    # datetimeTest()
    # timedeltaTest()
    timezoneTest()