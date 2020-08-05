'''
Excel读写

xlrd：       读，xls，xlsx
xlwings：    读，xls，xlsx
pandas：     读，xls，xlsx

xlwt：       写，xls           【优点】：支持xls；
                              【弱点】：功能很弱，可能因为Excel2013本身功能就弱；
xlsxwriter： 写，xlsx          【优点】：功能强大，可以设置各种格式；支持大数据写入（每次内存中只保留一行的数据，写入文件后，再继续读取下一行到内存，这样就不会内存溢出了）
                              【缺点】：不支持xls；

openpyxl：   读写，xlsx        【优点】：能读能写；功能比xlwt强，比xlsxwriter弱；【弱点】：不支持xls；

MicrosoftExcelAPI：           【优点】：很强大，直接和Excel进程通信，可以做任何在Excel能做的事；
                              【弱点】：很慢；平台限制，版本限制，问题较多；
'''

import xlrd,xlwt
import datetime

def excel_xlrd():

    # 表格类型：0. empty（空的）,1 string（text）, 2 number, 3 date, 4 boolean, 5 error， 6 blank（空白表格）

    # 1 打开Excel
    filePath = '';
    excel = xlrd.open_workbook(filePath)

    # 2 工作表相关
    sheet = excel.sheets()[0]            # 根据索引获取工作表
          # excel.sheet_by_index(0)
          # excel.get_sheets(0)
          # excel.sheet_by_name('one')   # 根据工作表名字获取工作表
    names = excel.sheet_names()          # 所有工作表的名字

    # 3 操作行
    rows = sheet.nrows                                         # 有效行数
    cells = sheet.row(0)                                       # 该行所有单元格对象组成的列表
          # sheet.row_slice(0)                                 # 该行所有单元格对象组成的列表
          # sheet.row_types(0, start_colx=0, end_colx=None)    # 该行中所有单元格的数据类型组成的列表
          # sheet.row_values(0, start_colx=0, end_colx=None)   # 该行中所有单元格的数据组成的列表
          # sheet.row_len(0)                                   # 返回该行的有效单元格长度

    # 4 操作列
    cols = sheet.ncols                                         # 有效列数
          # sheet.col(0, start_rowx=0, end_rowx=None)          # 该列所有单元格对象组成的列表
          # sheet.col_slice(0, start_rowx=0, end_rowx=None)    # 该列所有单元格对象组成的列表
          # sheet.col_types(0, start_rowx=0, end_rowx=None)    # 该列中所有单元格的数据类型组成的列表
          # sheet.col_values(0, start_rowx=0, end_rowx=None)   # 该列中所有单元格的数据组成的列表

    # 5 操作单元格
    cell = sheet.cell(0,0)               # 单元格对象
          # sheet.cell_type(0,0)         # 单元格中的数据类型
          # sheet.cell_value(0,0)        # 单元格中的数据

    # 6 异常报错
    # open()函数，文件名若包含中文，有时候会报错
    # xlrd.open_workbook()函数，文件名若包含中文，有时候会报错
    # 获取sheet时若包含中文，有时候会报错
    # 解决办法：编码文件名 filename.decode('utf-8')

def xlrdMain():

    filePath = 'C:\\Users\\Administrator\\Desktop\\python\\文件xlrd.xlsx';
    excel = xlrd.open_workbook(filePath)
    sheet = excel.sheets()[0]

    names = excel.sheet_names()
    print('工作表格：',names)

    rows = sheet.nrows
    print('第一个表格行数：',rows)
    cellsType = sheet.row_types(0, start_colx=0, end_colx=None)
    print('第一行数据类型：',cellsType)
    cellsValue = sheet.row_values(0, start_colx=0, end_colx=None)
    print('第一行数据：',cellsValue)

    cellRow = sheet.row(0)
    print('第一行单元格',cellRow)

    clos = sheet.ncols
    print('第一个表格列数：',clos)
    closType = sheet.col_types(0, start_rowx=0, end_rowx=None)
    print('第一列数据类型：',closType)
    closValue = sheet.col_values(0, start_rowx=0, end_rowx=None)
    print('第一列数据：',closValue)

    cellCol = sheet.col(0, start_rowx=0, end_rowx=None)
    print('第一列单元格',cellCol)


def excel_xlwt():

    filePath = 'C:\\Users\\Administrator\\Desktop\\python\\文件xlwt.xlsx';

    # 1 创建workbook和worksheet
    workbook = xlwt.Workbook('utf-8')
    worksheet = workbook.add_sheet('one')

    # 2 设置字体
    style = xlwt.XFStyle()                          # 初始化样式
    font = xlwt.Font()                              # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True                                # 黑体
    font.underline = True                           # 下划线
    font.italic = True                              # 斜体字
    style.font = font                               # 设定样式
    worksheet.write(0, 0, '谢宇鹏正在学Python', style)

    # 3 单元格设置
    worksheet.col(0).width = 10000                                           # 列宽
    style1 = xlwt.XFStyle()
    style1.num_format_str = 'D-MMM-YY h:mm:ss'                              # 日期格式: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
    worksheet.write(1, 0, datetime.datetime.now(), style1)

    link = xlwt.Formula('HYPERLINK("http://www.google.com";"Google")')      # 超链接
    worksheet.write(2, 0, link)

    worksheet.col(2).width = 10000
    worksheet.write_merge(0, 2, 2, 2, '张胖胖正在生气',style)                 # 合并单元格

    style2 = xlwt.XFStyle()
    alignment = xlwt.Alignment()                                            # 对其方式
    alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style2.alignment = alignment
    worksheet.write(3, 0, '阿鹏鹏正在想办法', style2)

    borders = xlwt.Borders()                    # 边框
    borders.left = xlwt.Borders.DASHED          # 线条 NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED
    borders.right = xlwt.Borders.DASHED
    borders.top = xlwt.Borders.DASHED
    borders.bottom = xlwt.Borders.DASHED
    borders.left_colour = 0x40                  # 颜色
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40
    style3 = xlwt.XFStyle()
    style3.borders = borders
    worksheet.write(5, 0, '叮...买礼物', style3)

    pattern = xlwt.Pattern()                            # 背景
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN        # 线条 NO_PATTERN, SOLID_PATTERN
    pattern.pattern_fore_colour = 5                     # 颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style4 = xlwt.XFStyle()
    style4.pattern = pattern
    worksheet.write(7, 0, '买什么礼物呢', style4)

    # 4 保存
    workbook.save(filePath)

if __name__ == '__main__':
    pass
