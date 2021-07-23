#!/usr/bin/python
# -*- encoding: utf-8 -*-

import cx_Oracle
import traceback
import CommonUtils
import datetime
import re

outputstr = {}

# 执行查询SQL
def getDataBySql(conn, cursor, sql):
    result = cursor.execute(sql)
    # data = result.fetchone()      # 取一条
    # data = result.fetchmany(10)   # 取十条
    data = result.fetchall()  # 取上个操作之后的所有记录
    return data


# 获取配置信息，第一行是数据库连接
def getConfig():
    configs = []
    with open('config.txt',encoding='utf-8',mode='r') as f:
        for config in f.readlines():
            config = config.strip()
            config = config.replace('\n','').replace('\r','')
            if(len(config) == 0):
                continue
            configs.append(config)
    return configs


def initdataSql():
    try:
        configs = getConfig()
        if len(configs) == 0:
            CommonUtils.showMsg('error', '配置文件为空！')
            return

        connectstr = configs[0]
        CommonUtils.writelog('info', *['数据库连接：', connectstr])
        conn = cx_Oracle.connect(connectstr)
        cursor = conn.cursor()
        user = connectstr[0:connectstr.find('/')].lower()

        compliestr = re.compile(r'\s+')
        for i,sqlstr in enumerate(configs):
            if i == 0:
                continue
            sqlstr = compliestr.sub(' ',sqlstr).strip().lower()
            sqlstr = sqlstr.replace(',t.rowid','').replace('t.rowid,','')
            type = sqlstr.split(' ')[0]
            if type == 'select':
                selectSql(sqlstr,conn,cursor,user)
            elif type == 'update':
                updateSql(sqlstr,user)
            elif type == 'delete':
                deleteSql(sqlstr,user)
            else :
                CommonUtils.showMsg('warn', '', *['只支持select/update/delete，不支持语句：【', sqlstr, '】'])
                return
        for table,sql in outputstr.items():
            with open(table + '.sql','w') as f:
                f.write(sql)
                CommonUtils.writelog('info',*['成功创建脚本：',table,'.sql'])
        CommonUtils.showMsg('info', '', '脚本已全部生成！')

    except Exception as e:
        CommonUtils.showMsg('error','',*['执行异常：',str(e)])
        CommonUtils.showMsg('error','',*['异常信息：',traceback.format_exc()])
        return
    finally:
        cursor.close()
        conn.close()


# 生成查询语句的初始化语句
notsupport = ('INTERVAL')
numbertype = ('NUMBER','BINARY_FLOAT','BINARY_DOUBLE')
def selectSql(sqlstr,conn,cursor,user):
    sqlstrarray = sqlstr.split(';')
    sqlstr = sqlstrarray[0]
    defaultvalue = {}
    for index,value in enumerate(sqlstrarray):
        if index != 0 and len(value) > 0:
            namevalue = value.split('=')
            defaultvalue[namevalue[0].upper()] = namevalue[1]

    fromindex = sqlstr.find('from')
    if fromindex == -1:
        CommonUtils.showMsg('warn', '', *['找不到from关键字，不支持语句：【', sqlstr, '】'])
        return

    whereindex = sqlstr.find('where')
    if whereindex == -1:
        whereindex = len(sqlstr) + 1
    fromstr = sqlstr[fromindex:whereindex]
    tablestr = fromstr.split(' ')[1].strip()
    tableRename = fromstr.split(' ')[2].strip()
    usertable = tablestr
    if tablestr.find(user) == -1:
        usertable = user + '.' + tablestr
        fromstr = fromstr.replace(tablestr,usertable)
    else:
        tablestr = tablestr.split(".")[1]
    if fromstr.find(',') != -1 or fromstr.find('join') != -1:
        CommonUtils.showMsg('warn','',*['只支持单表查询，不支持语句：【', sqlstr, '】'])
        return

    selectindex = sqlstr.find('select') + 6
    columnstr = sqlstr[selectindex:fromindex].strip()
    if len(tableRename) > 0:
        columnstr = columnstr.replace(tableRename + '.','')

    columnstrall, columnType = getColumns(tablestr, cursor, conn)
    if columnstr.find('*') != -1:
        columnstr = columnstrall
    columnarray = columnstr.split(',')

    wherestr = sqlstr[whereindex:]
    deletestr = '\ndelete ' + fromstr + wherestr + ';\n'
    datas = getDataBySql(conn, cursor, sqlstr)
    if len(datas) == 0:
        CommonUtils.showMsg('error', '', *['数据为空：【', sqlstr, '】'])
        return
    insertarray = []
    for data in datas:
        datacopy = list(data)
        for index,value in enumerate(data):
            column = columnarray[index].upper().strip()
            defaultval = defaultvalue.get(column)
            if defaultval is not None:
                datacopy[index] = defaultval
                continue
            type = columnType[column].strip()
            if value is None:
                datacopy[index] = '\'\''
            elif type in numbertype:
                datacopy[index] = str(value)
            elif type == 'DATE':
                datetimestr = datacopy[index].strftime('%Y-%m-%d %H:%M:%S')
                datacopy[index] = 'to_date(\''+datetimestr+'\',\'YYYY-MM-DD HH24:MI:SS\')'
            elif type.startswith('TIMESTAMP'):
                datetimestr = datacopy[index].strftime('%Y-%m-%d %H:%M:%S.%f')
                datacopy[index] = 'to_timestamp(\'' + datetimestr + '\',\'YYYY-MM-DD HH24:MI:SS:FF\')'
            else:
                datacopy[index] = '\'' + str(value) + '\''

        datastr = ', '.join(datacopy)
        insertarray.append('\ninsert into ' + usertable + '(' + columnstr + ') \nvalues (' + datastr +');\n')
    insertstr = ''.join(insertarray)
    insertstr = insertstr + '\ncommit; \n'
    if outputstr.get(tablestr) : # 如果存在
        outputstr[tablestr] = outputstr[tablestr] + deletestr + insertstr
    else:
        outputstr[tablestr] = deletestr + insertstr


def updateSql(sqlstr,user):
    updateindex = sqlstr.find('update') + 6
    setindex = sqlstr.find('set')
    if setindex == -1:
        CommonUtils.showMsg('warn', '', *['找不到set关键字，不支持语句：【', sqlstr, '】'])
        return
    tablestr = sqlstr[updateindex:setindex].strip()
    tablestr = tablestr.split(' ')[0]
    if tablestr.find(user) == -1:
        usertable = user + '.' + tablestr
        sqlstr.replace(tablestr,usertable)
    else:
        tablestr = tablestr.split('.')[1]
    updatestr = '\n' + sqlstr + ';\n\n' + 'commit;' + '\n'
    if outputstr.get(tablestr):  # 如果存在
        outputstr[tablestr] = outputstr[tablestr] + updatestr
    else:
        outputstr[tablestr] = updatestr


def deleteSql(sqlstr,user):
    fromindex = sqlstr.find('from') + 4
    whereindex = sqlstr.find('where')
    if fromindex == -1:
        CommonUtils.showMsg('warn', '', *['找不到from关键字，不支持语句：【', sqlstr, '】'])
        return
    tablestr = sqlstr[fromindex:whereindex].strip()
    tablestr = tablestr.split(' ')[0]
    if tablestr.find(user) == -1:
        usertable = user + '.' + tablestr
        sqlstr.replace(tablestr,usertable)
    else:
        tablestr = tablestr.split('.')[1]
    deletestr = '\n' + sqlstr + ';\n\n' + 'commit;' + '\n'
    if outputstr.get(tablestr):  # 如果存在
        outputstr[tablestr] = outputstr[tablestr] + deletestr
    else:
        outputstr[tablestr] = deletestr

# 获取表字段
# 返回逗号分隔的字段字符串 和 字段类型映射
def getColumns(table,cursor,conn):
    columnSql = '''select 
        t.column_name,t.data_type from user_tab_cols t
        where t.COLUMN_ID is not null and t.table_name = upper(\'''' + table + '\') order by t.COLUMN_ID'
    columns = getDataBySql(conn, cursor, columnSql)
    if len(columns) == 0:
        CommonUtils.showMsg('error','',*[table,' 没有字段！'])
        return
    columntype = {}
    columnstr = []
    for column in columns:
        columntype[column[0]]=column[1]
        columnstr.append(column[0])

    return ','.join(columnstr),columntype


# 执行入口
if __name__ == "__main__":
    CommonUtils.writelog('info',*['————————————————————————'])
    initdataSql()



