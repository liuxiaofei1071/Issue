from django.db import models


issue_status_choices = (
        ('0', '等待发布'),
        ('1', '发布中'),
        ('2', '等待测试'),
        ('3', '测试通过'),
        ('4', '发布成功'),
        ('5', '失败'),
        ('6', '回滚失败'),
        ('7', '回滚成功'),
    )

#用户表
class User(models.Model):
    # 部门
    departments_choices = (
        ('develop', "开发"),
        ('operation', "运维"),
        ('test', "测试"),
    )

    username = models.CharField('用户名',max_length=150)
    password = models.CharField('密码',max_length=18)
    role = models.CharField(verbose_name='角色',choices=(('0','开发'),('1','测试'),('2','运维')),default='0',max_length=10)
    email = models.EmailField(max_length=254,unique=True)
    department = models.CharField('部门',choices=departments_choices,max_length=20)
    phone = models.CharField('手机号',max_length=11,blank=True,null=True)
    is_admin = models.CharField('管理员',choices=(("0",'admin'),('1','普通')),max_length=10,default='1')
    create_time = models.DateTimeField('创建时间',max_length=50,auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.username


#主机表
class Host(models.Model):

    # 主机状态
    hosts_status_choices = (
        ('0', '在线'),
        ('1', '离线'),
        ('2', '维修'),
        ('3', '停用'),
    )

    # 主机环境
    hosts_environment_choices = (
        ('0', '测试'),
        ('1', '开发'),
        ('2', '预生产'),
        ('3', '生产'),
    )
    #主机类型
    Type = (
        ("0", "nginx"),
        ("1", "redis"),
        ("2", "db"),
        ("3", "server"),
    )

    name = models.CharField('主机名称',max_length=254,unique=True)
    ip = models.GenericIPAddressField('主机ip地址')
    version = models.CharField('版本',max_length=132)
    ssh = models.CharField('ssh端口',max_length=16,default=22)
    type = models.CharField('主机类型',max_length=12,choices=Type,default='3')
    status = models.CharField('主机状态',choices=hosts_status_choices,max_length=64,default='0')
    environment = models.CharField('主机环境',choices=hosts_environment_choices,max_length=64,default='3')

    def __str__(self):
        return self.ip

#项目表
class TeamProjt(models.Model):
    # 项目状态
    team_status_choices = (
        ('0', '在用'),
        ('1', '下线'),
    )
    #开发语言
    Language = (
        ("0", 'python'),
        ("1", "java"),
        ("2", 'go'),
        ("3", "php"),
        ("4", "html")
    )

    name = models.CharField('项目名称',max_length=32,unique=True)
    create_time = models.DateTimeField('项目创建时间',max_length=50,auto_now_add=True )
    boss = models.ManyToManyField('User',related_name="boss",verbose_name='负责人')
    tester = models.ManyToManyField('User',related_name="tester",verbose_name='测试人')
    developer = models.ManyToManyField('User',related_name="developer",verbose_name='开发人')
    ops_user = models.ManyToManyField('User',related_name="ops_user",verbose_name='运维人')
    server_host = models.ManyToManyField('Host',related_name="server_host",verbose_name='后端主机')  #后端主机
    nginx_host = models.ManyToManyField('Host',related_name="nginx_host",verbose_name='nginx服务器')
    develop_language = models.CharField('开发语言',max_length=20,choices=Language,default='0')
    team_status = models.CharField(choices=team_status_choices,verbose_name='项目状态',default='0', max_length=2)
    nginx_conf = models.CharField('nginx配置信息',max_length=254,null=True,blank=True)
    git_path = models.CharField(verbose_name='git地址',max_length=200)
    project_path = models.CharField(verbose_name='linux项目路径', max_length=200)
    note = models.CharField('备注',max_length=300,null=True,blank=True)
    domain = models.CharField('域名',max_length=100,null=True,blank=True)

    class Meta:
        ordering = ("-create_time",)
    def __str__(self):
        return self.name

#命令表
class Command(models.Model):
    command = models.CharField(verbose_name="命令", max_length=200)
    result = models.CharField(verbose_name="结果", max_length=2000)
    hosts_list = models.CharField(verbose_name="执行机器", max_length=20000)
    user = models.ForeignKey('User', verbose_name='用户')
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

#计划任务表
class Cron(models.Model):
    name = models.CharField('计划名称',max_length=32,unique=True,)
    time = models.CharField('计划任务执行时间',max_length=32)
    host_list = models.CharField('执行机器', max_length=200)
    job = models.CharField('任务',max_length=120)
    note = models.CharField('备注',max_length=300,null=True,blank=True)
    user = models.ForeignKey('User',verbose_name='创建者')
    linux_user = models.CharField(verbose_name='执行人',null=True,blank=True,default='root',max_length=30)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name

#初始化表
class Init(models.Model):
    name = models.CharField('名称',max_length=30,unique=True)
    function = models.CharField('初始化功能',max_length=200,unique=True)
    playbook = models.CharField('playbook路径',max_length=100)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    create_user = models.ForeignKey('User',verbose_name='创建者')

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name

#更新表
class Issue(models.Model):

    # 备份状态
    backups_status_choiecs = (
        ('0', '已备份'),
        ('1', '未备份'),
    )

    team = models.ForeignKey('TeamProjt',verbose_name='发布项目')
    user = models.ForeignKey('User',verbose_name='发布人')
    type = models.CharField('更新类型',max_length=50,choices=(('0','文件'),('1','git')),default='0')
    status =models.CharField('更新状态',choices=issue_status_choices,max_length=64,default='0')
    backup = models.CharField('备份情况',choices=backups_status_choiecs,max_length=12,default='0')
    backup_path = models.CharField('备份文件地址',max_length=300,null=True,blank=True)
    upload_path = models.CharField('上传文件地址',max_length=300,null=True,blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

#主机发布表
class HostIssue(models.Model):
    host = models.ForeignKey('Host',verbose_name='发布机器')
    issue = models.ForeignKey('Issue',verbose_name='更新')
    team = models.ForeignKey('TeamProjt',verbose_name='发布项目')
    time = models.DateTimeField('主机发布时间',max_length=30)
    status = models.CharField('更新状态',choices=issue_status_choices,max_length=64,default='0',)



#初始化日志表
class InitLog(models.Model):
    init = models.ForeignKey(Init, verbose_name="初始化功能")
    hosts_list = models.ManyToManyField(Host, verbose_name="执行机器")
    user = models.ForeignKey(User, verbose_name="创建者")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ('-create_time',)