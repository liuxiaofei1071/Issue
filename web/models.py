from django.db import models


#部门
departments_choices = (
    ('develop',"开发"),
    ('operation',"运维"),
    ('test',"测试"),
)

#主机状态
hosts_status_choices =(
    ('online','在线'),
    ('offline','离线'),
    ('maintain','维修'),
    ('stop_use','停用'),
)

#主机环境
hosts_environment_choices = (
    ('test','测试'),
    ('developing','开发'),
    ('pre_production ','预生产'),
    ('production ','生产'),
    )

#项目状态
team_status_choices = (
    ('in_use','在用'),
    ('off_line','下线'),
)

#发布状态
issue_status_choices = (
    ('wait_issue','等待发布'),
    ('issueing','发布中'),
    ('wait_test','等待测试'),
    ('pass_test','测试通过'),
    ('issue_success','发布成功'),
    ('roll_back','回滚'),
)

#备份状态
backups_status_choiecs = (
    ('yes','已备份'),
    ('no','未备份'),
)

#用户表
class User(models.Model):
    username = models.CharField('用户名',max_length=15)
    password = models.CharField(max_length=18)
    role = models.ManyToManyField("Role")
    email = models.EmailField(max_length=254,unique=True)
    department = models.CharField('部门',choices=departments_choices,max_length=20)
    create_time = models.DateTimeField('创建时间',max_length=50)

#角色表
class Role(models.Model):
    name = models.CharField('角色名称',max_length=30)

#主机表
class Host(models.Model):
    name = models.CharField('主机名称',max_length=254)
    ip = models.CharField('ip',max_length=16)
    version = models.CharField('版本',max_length=132)
    ssh = models.CharField('ssh端口',max_length=16)
    type = models.CharField('主机类型',max_length=12)
    hosts_status = models.CharField('主机状态',choices=hosts_status_choices,max_length=64)
    hosts_environment = models.CharField('主机环境',choices=hosts_environment_choices,max_length=64)
    inits = models.ForeignKey('Init')

#项目表
class TeamProjt(models.Model):
    name = models.CharField('项目名称',max_length=32)
    create_time = models.DateTimeField('项目创建时间',max_length=50)
    '''多对多关系'''
    principal = models.ManyToManyField('User',related_name="负责人",verbose_name='负责人')
    tester = models.ManyToManyField('User',related_name="测试人",verbose_name='测试人')
    developer = models.ManyToManyField('User',related_name="开发人",verbose_name='开发人')
    server_host = models.ManyToManyField('Host',related_name="其他服务器",verbose_name='其他服务器')
    nginx_host = models.ManyToManyField('Host',related_name="nginx服务器",verbose_name='nginx服务器')
    develop_language = models.CharField('开发语言',max_length=20)
    team_status = models.CharField(choices=team_status_choices,verbose_name='项目状态',max_length=64)
    nginx_conf = models.CharField('nginx配置信息',max_length=254)
    project_path = models.CharField(verbose_name='linux项目路径',max_length=60)
    git_path = models.CharField(verbose_name='git地址',max_length=80)
    note = models.CharField('备注',max_length=300)

#命令表
class Command(models.Model):
    command_name = models.CharField('执行命令名称',max_length=120)
    result = models.CharField('执行结果', max_length=120)
    operator = models.ForeignKey('User',verbose_name='执行人')
    host_list = models.ForeignKey('Host',verbose_name='主机列表')


#定时任务表
class Cron(models.Model):
    cron_name = models.CharField('任务名称',max_length=32)
    time = models.DateTimeField('时间',max_length=30)
    job = models.CharField('任务',max_length=120)
    note = models.CharField('备注',max_length=300)
    linux_user = models.CharField('linux用户',max_length=16)
    operator = models.ForeignKey('User',verbose_name='执行人')

#初始化表
class Init(models.Model):
    init_name = models.CharField('初始化名称',max_length=30)
    system = models.CharField('系统名称',max_length=50)
    init_function = models.CharField('初始化功能',max_length=200)
    playbook = models.CharField('playbook',max_length=20)
    init_time = models.DateTimeField('初始化时间',max_length=20)

#发布表
class Issue(models.Model):
    issuer = models.ForeignKey('User',verbose_name='发布人')
    version_num = models.CharField('版本号',max_length=50)
    issue_team = models.ForeignKey('TeamProjt',verbose_name='发布项目')
    issue_status =models.CharField('发布状态',choices=issue_status_choices,max_length=64)
    file_dir = models.CharField('部署发布系统',max_length=50)
    backups = models.CharField('备份情况',choices=backups_status_choiecs,max_length=64)
    backup_path = models.CharField('备份地址',max_length=30)

#主机发布表
class HostIssue(models.Model):
    hosts = models.ForeignKey('Host',verbose_name='主机信息')
    innues = models.ForeignKey('Issue',verbose_name='发布信息')
    time = models.DateTimeField('主机发布时间',max_length=30)
    host_issue_status = models.CharField('主机发布状态',choices=issue_status_choices,max_length=64)



