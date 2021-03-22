#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Descripttion: 操作oracle数据库
1、安装 cx_Oracle：pip install cx_Oracle -i https://mirrors.aliyun.com/pypi/simple/
2、数据库连接驱动，都依赖于本地的数据库客户端，所以必须先安装对应的数据库客户端
3、Oracle客户端的位数和pl/sql的位数是对应的（32和64）
4、32位的客户端，就用32位的python运行和打包，同理64位
5、除了pip安装，也可以进入阿里云镜像地址：https://mirrors.aliyun.com/pypi/simple/，选择cx_oracle包32位的whl文件下载
6、先安装 pip install wheel，再通过 pip install xxx.whl 的方式安装
7、如果64位的python不能安装32位的包，需要在本地再安装一个32位的python，不冲突（系统变量只配置一个就行，另一个通过进入对应安装目录来使用）
8、在对应python目录下和pip目录下，优先使用该python和pip，系统变量只是为了方便在任何目录下调用程序
version: 1.0
Author: xieyupeng
Date: 2020-09-07 15:16:32
LastEditors: xieyupeng
LastEditTime: 2020-10-13 12:15:47
'''
import cx_Oracle


# cx_Oracle 驱动基本操作
def oracleOp(table,cursor,conn):

    # 字段
    columnSql = '''select 
        t.column_name,t.data_type,t.data_length,t.data_precision,t.data_scale,t.nullable,t.data_default
        from user_tab_cols t
        where t.table_name = upper(\'''' + table + '\') order by t.COLUMN_ID'
    columns = getBySql(conn, cursor, columnSql)
    tableColumns = []
    for column in columns:
        tableColumns.append(getColumnStr(column))
    columnStr = ','.join(tableColumns)
    createTableStr = 'create table ' + table + '(' + columnStr + ');'
    print(createTableStr)

    # 主键
    primarySql = '''select 
        col.*
        from user_constraints con, user_cons_columns col
        where con.constraint_name = col.constraint_name and con.constraint_type = 'P' and col.table_name = \'''' + table + '\''
    primarys = getBySql(conn, cursor, primarySql)
    primary = primarys[0]
    primaryName = primary[1]
    primaryStr = 'alter table ' + table + ' add constraint ' + primary[1] + ' primary key ' + '(' + primary[3] + ');'
    print(primaryStr)

    # 索引
    indexSql = '''select t.index_name,
        listagg(t.column_name,',') within group(order by t.column_position) as index_column,i.index_type,i.uniqueness
        from user_ind_columns t,user_indexes i 
        where t.index_name = i.index_name and t.table_name = \'''' + table + '\' group by t.index_name,i.index_type,i.uniqueness'
    indexs = getBySql(conn, cursor, indexSql)
    indexPrefix = ''
    for index in indexs:
        iname = index[0]
        icolumns = index[1]
        itype = index[2]
        iunique = index[3]
        if iname == primaryName:
            continue
        if itype == 'BITMAP':
            indexPrefix = 'create bitmap'
        elif itype == 'NORMAL' and iunique == 'UNIQUE':
            indexPrefix = 'create unique'
        elif itype == 'NORMAL' and iunique == 'NONUNIQUE':
            indexPrefix = 'create '
        else:
            print('不支持索引：',iname)
            return
        indexStr = indexPrefix + ' index ' + iname + ' on ' + table + '(' + icolumns + ');'
        print(indexStr)

    # 授权
    grantSql = '''select t.grantee,t.grantable,
        listagg(t.privilege,',') within group(order by t.privilege ) as operation
        from all_tab_privs_made t where table_name= \'''' + table + '\' group by t.grantee,t.grantable' 
    grants = getBySql(conn, cursor, grantSql)
    for grant in grants:
        grantSuffix = ';'
        grantable = grant[1]
        operation = grant[2]
        target = grant[0]
        if grantable == 'YES':
            grantSuffix = ' with grant option;'
        grantStr = 'grant ' + operation + ' on ' + table + ' to ' + target + grantSuffix
        print(grantStr)

# 查询
def getBySql(conn, cursor, sql):
    result = cursor.execute(sql)
    # data = result.fetchone()      # 取一条
    # data = result.fetchmany(10)   # 取十条
    data = result.fetchall()  # 取上个操作之后的所有记录
    print(data)
    return data


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
# 判断第四类字段
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
            print('不支持字段类型：', ctype, ',', cprecision, ',', cscale)
            return
    else:
        print('不支持字段类型：', ctype)
        return
    cdefaultStr = '' if cdefault == 'None' else 'default ' + cdefault
    cnullStr = '' if cnull == 'Y' else 'not null'
    return cname + ' ' + ctype + ' ' + cdefaultStr + ' ' + cnullStr

if __name__ == "__main__":
    try:
        conn = cx_Oracle.connect('kdas/kdas@10.201.83.93:1521/KDASXD')
        cursor = conn.cursor()
        oracleOp('PYTHON_TABLE_TEST',cursor,conn)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()