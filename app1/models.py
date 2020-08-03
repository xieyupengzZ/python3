from django.db import models

'''
    常用字段类型：
    BooleanField:   布尔类型字段
    CharField:      字符串类型字段
    TextField:      文本字段
    DateTimeField:  日期字段
    DecimalField:   (精确)小数字段
    FloatField:     (浮点数）小数字段
    IntegerField:   整数字段
    SmallIntegerField:小整数字段
    EmailField:     Email字段
    FileField:      文件字段（保存和处理上传的文件）
    Imagefield:     图片字段（保存和处理上传的图片）
    IPAddressField: IP字段
    URLField:       网页地址字段
    
    常用字段选项：
    null(null=True|False)：      数据库字段的设置是否可以为空（数据库进行验证）
    blank(blank=True|False)：    字段是否为空django会进行校验（表单进行验证）
    choices：                    轻量级的配置字段可选属性的定义
    default：                    字段的默认选项
    help_text：                  字符按文字帮助
    primary_key(True|False)：    一般不需要定义是否为主键，如果没有指明主键的话，django胡自动添加一个默认主键：id=models.AutoField(primary_key=True)
    unique：                     是否唯一（对于数据表而言）
    verbose_name：               字段的详细名称，若不指定该属性，默认使用字段的属性名称
    
'''

class messageQueue(models.Model):
    ename=models.CharField('英文名',max_length=50) # 默认 null=False 必填
    cname=models.CharField('中文名',max_length=10,null=True,default='')
    compan=models.CharField('公司',max_length=50,null=True,default='')

    # 设置扩展属性
    class Meta:

        # 数据库中生成的表名称 默认 app名称 + 下划线 + 类名
        db_table = "message_queue"

        # 对象默认的顺序,它是一个字符串的列表或元组。每个字符串是一个字段名，前面带有可选的“-”
        # 前缀表示倒序,前面没有“-”的字段表示正序。
        # Ordering = ['-order_date']

        # admin中显示的表名称
        verbose_name = '消息队列'

        # verbose_name加s
        verbose_name_plural = '消息队列'

        # 联合索引
        index_together = [
            ("ename", "cname"),   # 应为两个存在的字段
        ]

        # 联合唯一索引
        unique_together = (("ename", "cname"),)   # 应为两个存在的字段