#!/usr/bin/python
# -*- encoding: utf-8 -*-
# 代码不区分多少位，只有插件才区分，32位Oracle客户端，就用32位的python打包，同理64位
import cx_Oracle
import traceback
import tkinter
from tkinter import messagebox
from datetime import datetime as dtime

# 查询
def getBySql(conn, cursor, sql):
    result = cursor.execute(sql)
    # data = result.fetchone()      # 取一条
    # data = result.fetchmany(10)   # 取十条
    data = result.fetchall()  # 取上个操作之后的所有记录
    return data

# 字段
def getColumns(table,cursor,conn,user):
    columnSql = '''select 
        t.column_name,t.data_type,t.data_length,t.data_precision,t.data_scale,t.nullable,t.data_default
        from user_tab_cols t
        where t.COLUMN_ID is not null and t.table_name = upper(\'''' + table + '\') order by t.COLUMN_ID'
    columns = getBySql(conn, cursor, columnSql)
    if len(columns) == 0:
        showMsg('error','',*[table,' 没有字段！'])
        return
    tableColumns = []
    for column in columns:
        tableColumns.append(getColumnStr(column))
    columnStr = ',\n'.join(tableColumns)
    createTableStr = 'create table '+ user + '.' + table + '\n(\n' + columnStr + '\n);\n'
    return createTableStr

# 主键
def getPrimary(table,cursor,conn):
    primarySql = '''select 
        col.*
        from user_constraints con, user_cons_columns col
        where con.constraint_name = col.constraint_name and con.constraint_type = 'P' and col.table_name = \'''' + table + '\''
    primarys = getBySql(conn, cursor, primarySql)
    if len(primarys) == 0:
        return ''
    primary = primarys[0]
    global primaryName  # 定义当前模块的全局变量
    primaryName = primary[1]
    primaryStr = '\n alter table ' + table + ' add constraint ' + primary[1] + ' primary key ' + '(' + primary[3] + ');'
    return primaryStr + '\n'

# 索引
def getIndexs(table,cursor,conn):
    indexSql = '''select t.index_name,
        listagg(t.column_name,',') within group(order by t.column_position) as index_column,i.index_type,i.uniqueness
        from user_ind_columns t,user_indexes i 
        where t.index_name = i.index_name and t.table_name = \'''' + table + '\' group by t.index_name,i.index_type,i.uniqueness'
    indexs = getBySql(conn, cursor, indexSql)
    if len(indexs) == 0:
        return ''
    indexStrs = []
    for index in indexs:
        indexPrefix = ''
        iname = index[0]
        icolumns = index[1]
        itype = index[2]
        iunique = index[3]
        if iname == primaryName:
            continue
        if itype == 'BITMAP':
            indexPrefix = ' create bitmap'
        elif itype == 'NORMAL' and iunique == 'UNIQUE':
            indexPrefix = ' create unique'
        elif itype == 'NORMAL' and iunique == 'NONUNIQUE':
            indexPrefix = ' create'
        else:
            showMsg('warn','','不支持索引：' + iname)
            return
        indexStr = '\n' + indexPrefix + ' index ' + iname + ' on ' + table + '(' + icolumns + ');'
        indexStrs.append(indexStr)
    return ''.join(indexStrs) + '\n'
    
# 授权
def getGrants(table,cursor,conn):
    grantSql = '''select t.grantee,t.grantable,
        listagg(t.privilege,',') within group(order by t.privilege ) as operation
        from all_tab_privs_made t where table_name= \'''' + table + '\' group by t.grantee,t.grantable' 
    grants = getBySql(conn, cursor, grantSql)
    if len(grants) == 0:
        return ''
    grantStrs = []
    for grant in grants:
        grantSuffix = ';'
        grantable = grant[1]
        operation = grant[2]
        target = grant[0]
        if grantable == 'YES':
            grantSuffix = ' with grant option;'
        grantStr = '\n grant ' + operation + ' on ' + table + ' to ' + target + grantSuffix
        grantStrs.append(grantStr)
    return ''.join(grantStrs)

# 注释
def getComments(table,cursor,conn,user):
    commentSuffix = ';'
    commentStrs = []
    
    # 表名注释
    commmentTabSql = 'SELECT t.COMMENTS FROM USER_TAB_COMMENTS t where table_name = \'' + table + '\''
    tabComments = getBySql(conn,cursor,commmentTabSql)
    if len(tabComments) == 0:
        return ''
    tabComment = ''
    for comment in tabComments:
        if comment[0] is None:
            continue
        tabComment = '\n comment on table ' + user + '.' + table + ' is \'' + comment[0] + '\'' + commentSuffix
    commentStrs.append(tabComment)

    # 字段注释
    commentSql = 'SELECT t.COLUMN_NAME,t.COMMENTS FROM  USER_COL_COMMENTS t where table_name = \'' + table + '\''
    comments = getBySql(conn,cursor,commentSql)
    if len(comments) == 0:
        return ''
    for comment in comments:
        if comment[1] is None:
            continue
        colComment = '\n comment on column ' + table + '.' + comment[0] + ' is \'' + comment[1] + '\'' + commentSuffix
        commentStrs.append(colComment)
    return ''.join(commentStrs) + '\n'

# 字段类型分类如下：
'''
第一类字段：【没有长度标识】
第二类字段：【有长度没精度】
第三类字段：【有精度有小数点】精度为空小数点为0的是Integer，精度不为空但是小数点为空的就是整数，精度和小数点都不为空的就是小数
第四类字段：【名字特别长，多个字符串组成】如：TIMESTAMP(6) WITH TIME ZONE，INTERVAL YEAR(8) TO MONTH
第五类字段：【有长度没精度】但是真实长度是查询出来的一半，目前只发现一个：NVARCHAR2
'''
type1 = ('LONG RAW','NCLOB', 'BINARY_DOUBLE', 'BINARY_FLOAT','DATE', 'BLOB', 'CLOB', 'LONG')
type2 = ('RAW', 'VARCHAR2', 'CHAR')
type3 = ('NUMBER')
type5 = ('NVARCHAR2')
def type4(ctype):
    if ctype.startswith('INTERVAL') or ctype.startswith('TIMESTAMP'):
        return True
    else:
        return False

# 解析字段
def getColumnStr(column):

    cname = column[0]  # 名称
    ctype = column[1]  # 类型
    clength = column[2]  # 长度
    cprecision = str(column[3])  # 精度
    cscale = str(column[4])  # 小数点
    cnull = column[5]  # 是否为空
    cdefault = str(column[6])  # 默认值

    if ctype in type1 or type4(ctype):
        ctype = ctype
    elif ctype in type2:
        ctype = ctype + '(' + str(clength) + ')'
    elif ctype in type5:
        ctype = ctype + '(' + str(int(clength / 2)) + ')'
    elif ctype in type3:
        if cprecision == 'None' and cscale == '0':  # INTEGER
            ctype = 'INTEGER'
        elif cprecision == 'None' and cscale == 'None':  # NUMBER
            ctype = ctype
        elif cprecision != 'None' and cscale == '0':  # NUMBER(x)
            ctype = ctype + '(' + cprecision + ')'
        elif cprecision != 'None' and cscale != 'None':  # NUMBER(x,y)
            ctype = ctype + '(' + cprecision + ',' + cscale + ')'
        else:
            showMsg('warn','','不支持字段类型：' + ctype + ',' + cprecision + ',' + cscale)
            return
    else:
        showMsg('warn','','不支持字段类型：' + ctype)
        return
    cdefaultStr = '' if cdefault == 'None' else 'default ' + cdefault.replace('\n','').replace('\r','')
    cnullStr = '' if cnull == 'Y' else 'not null'
    columns = '  ' + cname + ' ' + ctype + ' ' + cdefaultStr + ' ' + cnullStr
    return columns.rstrip()

# 备份数据的语句
def getTableSqlStart(table,user):
    # 用 \ 换行写代码，注意后面不能有空格
    tableSqlStart = \
        'declare\nbegin\n' + \
        '    ' + user + '.kingdom_scr.backup_and_drop_table(\'' + user + '\', \'' + table + '\', \'' + table + '_BAK\');\n' + \
        'end;\n' + \
        '/\n' + \
        '\n'
    return tableSqlStart

# 恢复数据的语句
def getTableSqlEnd(table,user):
    # 用 \ 换行写代码，注意后面不能有空格
    tableSqlEnd = \
        '\n\ndeclare\nbegin\n' + \
        '    ' + user + '.kingdom_scr.recovery_and_drop_baktable(\'' + user + '\', \'' + table + '\', \'' + table + '_BAK\');\n' + \
        'end;\n' + \
        '/\n'
    return tableSqlEnd

# 依次获取表的结构
def tableSql():
    try:
        # connectstr = 'kdas/kdas@10.201.83.93:1521/KDASXD'
        # table = 'PYTHON_TABLE_TEST'
        configs = getConfig()
        if len(configs) == 0:
            showMsg('error','','配置文件为空！')
            return
        
        connectstr = configs[0]
        writelog('info',*['数据库连接：',connectstr])
        conn = cx_Oracle.connect(connectstr)
        cursor = conn.cursor()
        tables = configs[1].split(',')
        writelog('info',*['表：',configs[1]])
        isComment = configs[2].upper()
        isNameUpper = configs[3].upper()

        for table in tables:
            user = connectstr[0:connectstr.find('/')]
            user = user.upper()
            startSql = getTableSqlStart(table,user)
            columnSql = getColumns(table,cursor,conn,user)
            if columnSql is None:
                return
            primarySql = getPrimary(table,cursor,conn)
            indexSql = getIndexs(table,cursor,conn)
            grantSql = getGrants(table,cursor,conn)
            commentSql = ''
            if isComment == 'TRUE':
                commentSql = getComments(table,cursor,conn,user)
            endSql = getTableSqlEnd(table,user)
            createTableSql = \
                startSql + columnSql + commentSql + primarySql + indexSql + grantSql + endSql

            table = table.lower()
            if isNameUpper == 'TRUE':
                table = table.upper()
            with open(table + '.tab','w') as f:
                f.write(createTableSql)
            writelog('info',*['成功创建脚本：',table,'.tab'])
        
        showMsg('info','','脚本已全部生成！')

    except Exception as e:
        showMsg('error','',*['执行异常：',str(e)])
        showMsg('error','',*['异常信息：',traceback.format_exc()])
        return
    finally:
        cursor.close()
        conn.close()

# 获取配置信息
# 第一行是连接，第二行是要导出的表（以逗号分隔），第三行是否导出表注释
def getConfig():
    configs = []
    with open('config.txt','r') as f:
        for config in f.readlines():
            config = config.strip()
            config = config.replace('\n','').replace('\r','')
            if(len(config) == 0):
                continue
            configs.append(config)
    return configs

# 弹窗信息
def showMsg(type,title,*msg):
    writelog(type,*msg)
    title = 'Python自动生成数据库脚本'
    printinfo = ''.join(msg)
    # tkinter的对话窗口必须要有一个主窗口，就像所有控件都需要放在一个窗口上。
    # 建立一个隐形窗口后就不会出现那个影响美观的自带窗口了
    root = tkinter.Tk()
    root.withdraw()
    # messagebox 会引起阻塞，直到弹出框的被点击确定或关闭后
    if type == 'info':
        messagebox.showinfo(title=title,message=printinfo)
    elif type == 'error':
        messagebox.showerror(title=title,message=printinfo)
    elif type == 'warn':
        messagebox.showwarning(title=title,message=printinfo)
    else:
        messagebox.showinfo(title=title,message=printinfo)

# 日志文件
def writelog(type,*msg):
    type = '【' + type.upper() + '】'
    nowtime = '【' + str(dtime.now()) + '】'
    log = nowtime + type + ''.join(msg) + '\n'
    with open('log.txt','a') as f:
        f.write(log)

# 执行入口
if __name__ == "__main__":
    writelog('info',*['————————————————————————'])
    tableSql()