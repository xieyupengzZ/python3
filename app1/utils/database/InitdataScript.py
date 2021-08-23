#!/usr/bin/python
# -*- encoding: utf-8 -*-

import cx_Oracle
import traceback
import CommonUtils
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
    with open('id_config.txt',encoding='utf-8',mode='r') as f:
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
            CommonUtils.showMsg('error','id_log.txt','配置文件为空！')
            return

        connectstr = configs[0]
        CommonUtils.writelog('info','id_log.txt', *['数据库连接：', connectstr])
        conn = cx_Oracle.connect(connectstr)
        cursor = conn.cursor()
        user = connectstr[0:connectstr.find('/')].lower()

        compliestr = re.compile(r'\s+')
        for i,sqlstr in enumerate(configs):
            if i == 0:
                continue
            sqlstr = compliestr.sub(' ',sqlstr).strip()
            type = sqlstr.split(' ')[0].lower()

            if type == 'select':
                # 把sql语句小写化，注意不要修改条件sql的大小写，因为查询条件是区分大小写的
                whereindex = CommonUtils.searchStr(sqlstr,' where ',re.I)
                if whereindex != -1:
                    whereindex = whereindex + 6
                    beforeWhere = sqlstr[0:whereindex].lower()
                    sqlstr = beforeWhere + sqlstr[whereindex:]
                else:
                    # 没有where条件的情况
                    fromindex = CommonUtils.searchStr(sqlstr,' from ',re.I)
                    if fromindex == -1:
                        CommonUtils.showMsg('warn','id_log.txt', '', *['找不到from关键字：【', sqlstr, '】'])
                        return
                    fromindex = fromindex + 6
                    beforeFrom = sqlstr[0:fromindex].lower()
                    sqlstr = beforeFrom + sqlstr[fromindex:]

                sqlstr = sqlstr.replace(',t.rowid', '').replace('t.rowid,', '')
                selectSql(sqlstr,conn,cursor,user)
            elif type == 'update':
                updateSql(sqlstr,user)
            elif type == 'delete':
                deleteSql(sqlstr,user)
            else :
                CommonUtils.showMsg('warn', 'id_log.txt','', *['只支持select/update/delete，不支持语句：【', sqlstr, '】'])
                return
        for table,sql in outputstr.items():
            with open(table + '.sql','w') as f:
                f.write(sql)
                CommonUtils.writelog('info','id_log.txt',*['成功创建脚本：',table,'.sql'])
        CommonUtils.showMsg('info','id_log.txt', '', '脚本已全部生成！')

    except Exception as e:
        CommonUtils.showMsg('error','id_log.txt','',*['执行异常：',str(e)])
        CommonUtils.showMsg('error','id_log.txt','',*['异常信息：',traceback.format_exc()])
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

    fromindex = CommonUtils.searchStr(sqlstr,' from ',re.I)
    if fromindex == -1:
        CommonUtils.showMsg('warn','id_log.txt', '', *['找不到from关键字，不支持语句：【', sqlstr, '】'])
        return
    whereindex = CommonUtils.searchStr(sqlstr,' where ',re.I)
    if whereindex == -1:
        whereindex = len(sqlstr) + 1
    fromstr = sqlstr[fromindex:whereindex].strip()
    tablestr = fromstr.split(' ')[1].strip()
    tableRename = fromstr.split(' ')[2].strip()
    usertable = tablestr
    userindex = CommonUtils.searchStr(tablestr, user, re.I)
    if userindex == -1:
        usertable = user + '.' + tablestr
        fromstr = fromstr.replace(tablestr,usertable)
    else:
        tablestr = tablestr.split(".")[1]
    if fromstr.find(',') != -1 or fromstr.find('join') != -1:
        CommonUtils.showMsg('warn','id_log.txt','',*['只支持单表查询，不支持语句：【', sqlstr, '】'])
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
        CommonUtils.showMsg('error','id_log.txt', '', *['数据为空：【', sqlstr, '】'])
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
    updateindex = CommonUtils.searchStr(sqlstr,'update ',re.I) + 6
    setindex = CommonUtils.searchStr(sqlstr,' set ',re.I)
    if setindex == -1:
        CommonUtils.showMsg('warn','id_log.txt', '', *['找不到set关键字，不支持语句：【', sqlstr, '】'])
        return
    tablestr = sqlstr[updateindex:setindex].strip()
    tablestr = tablestr.split(' ')[0]
    userindex = CommonUtils.searchStr(tablestr,user,re.I)
    if userindex == -1:
        usertable = user + '.' + tablestr
        sqlstr = sqlstr.replace(tablestr,usertable)
    else:
        tablestr = tablestr.split('.')[1]
    updatestr = '\n' + sqlstr + ';\n\n' + 'commit;' + '\n'
    if outputstr.get(tablestr):  # 如果存在
        outputstr[tablestr] = outputstr[tablestr] + updatestr
    else:
        outputstr[tablestr] = updatestr

def deleteSql(sqlstr,user):
    fromindex = CommonUtils.searchStr(sqlstr,' from ',re.I)
    if fromindex == -1:
        CommonUtils.showMsg('warn', 'id_log.txt', '', *['找不到from关键字，不支持语句：【', sqlstr, '】'])
        return
    fromindex = fromindex + 5
    whereindex = CommonUtils.searchStr(sqlstr,' where ',re.I)
    if fromindex == -1:
        CommonUtils.showMsg('warn', 'id_log.txt', '', *['找不到where关键字，不支持语句：【', sqlstr, '】'])
        return
    tablestr = sqlstr[fromindex:whereindex].strip()
    tablestr = tablestr.split(' ')[0]
    userindex = CommonUtils.searchStr(tablestr,user,re.I)
    if userindex == -1:
        usertable = user + '.' + tablestr
        sqlstr = sqlstr.replace(tablestr,usertable)
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
        CommonUtils.showMsg('error','id_log.txt','',*[table,' 没有字段！'])
        return
    columntype = {}
    columnstr = []
    for column in columns:
        columntype[column[0]]=column[1]
        columnstr.append(column[0])

    return ','.join(columnstr),columntype


# 执行入口
if __name__ == "__main__":
    CommonUtils.writelog('info','id_log.txt',*['————————————————————————'])
    initdataSql()
    # sqlstr = 'select t.* FROM kdbase.upm_dict_items t';
    # fromSearch = re.search(' from ', sqlstr, flags=re.I)
    # print(fromSearch)


