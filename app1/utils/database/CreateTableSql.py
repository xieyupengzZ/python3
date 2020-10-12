#!/usr/bin/python
# -*- encoding: utf-8 -*-
# 针对32位oracle客户端，python32位，cx_oracle插件32位
import cx_Oracle

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
        where t.table_name = \'''' + table + '\' order by t.column_name'
    columns = getBySql(conn, cursor, columnSql)
    if len(columnSql) == 0:
        showMsg('error','',*[table,' 没有字段！'])
        return
    tableColumns = []
    for column in columns:
        tableColumns.append(getColumnStr(column))
    columnStr = ',\n'.join(tableColumns)
    createTableStr = 'create table ' + table + '\n(\n' + columnStr + '\n);\n'
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

    ctypes = ''
    if ctype in type1 or type4(ctype):
        ctypes = ctype
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
        showMsg('info','',*['数据库连接：',connectstr])
        conn = cx_Oracle.connect(connectstr)
        cursor = conn.cursor()
        tables = configs[1].split(',')
        showMsg('info','',*['表：',configs[1]])

        for table in tables:
            user = connectstr[0:connectstr.find('/')]
            user = user.upper()
            print(table)
            startSql = getTableSqlStart(table,user)
            columnSql = getColumns(table,cursor,conn,user)
            if columnSql == 'None':
                return
            primarySql = getPrimary(table,cursor,conn)
            indexSql = getIndexs(table,cursor,conn)
            grantSql = getGrants(table,cursor,conn)
            endSql = getTableSqlEnd(table,user)
            createTableSql = \
                startSql + columnSql + primarySql + indexSql + grantSql + endSql
            with open(table + '.txt','w') as f:
                f.write(createTableSql)

    except Exception as e:
        showMsg('error','',*['执行异常：',str(e)])
        return
    finally:
        cursor.close()
        conn.close()

# 获取配置信息
# 第一行是连接，第二行是要导出的表（以逗号分隔）
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
    title = 'Python自动生成数据库脚本'
    print(''.join(msg))
    # if type == 'info':
    #     messagebox.showinfo(title=title,message=msg)
    # elif type == 'error':
    #     messagebox.showerror(title=title,message=msg)
    # elif type == 'warn':
    #     messagebox.showwarning(title=title,message=msg)
    # else:
    #     messagebox.showinfo(title=title,message=msg)

# 执行入口
if __name__ == "__main__":
    tableSql()
    showMsg('info','','表的创建脚本生成成功！')
    input("等待输入...")