from django.conf.urls import url
from web.views import home
from web.views import user,host,cron,team,command,init,initlog



urlpatterns = [
    url(r'^home/', home.home,name='home'),
    #用户url
    url(r'^user_list/', user.user_list,name='user_list'),
    url(r'^add_user/', user.change_user,name='add_user'),
    url(r'^edit_user/(?P<pk>\d+)', user.change_user,name='edit_user'),
    url(r'^del_user/(\d+)', user.del_user,name='del_user'),

    # 主机url
    url(r'^host_list/', host.host_list,name='host_list'),
    url(r'^add_host/', host.change_host,name='add_host'),
    url(r'^edit_host/(?P<pk>\d+)', host.change_host,name='edit_host'),
    url(r'^del_host/(\d+)', host.del_host,name='del_host'),

    #计划任务url
    url(r'^cron_list/', cron.cron_list,name='cron_list'),
    url(r'^add_cron/', cron.change_cron,name='add_cron'),
    url(r'^edit_cron/(?P<pk>\d+)', cron.change_cron,name='edit_cron'),
    url(r'^del_cron/(\d+)', cron.del_cron,name='del_cron'),

    #项目url
    url(r'^team_list/', team.team_list, name='team_list'),
    url(r'^add_team/', team.change_team, name='add_team'),
    url(r'^edit_team/(?P<pk>\d+)', team.change_team, name='edit_team'),
    url(r'^del_team/(\d+)', team.del_team, name='del_team'),

    #命令url
    url(r'^command_list/', command.command_list, name='command_list'),
    url(r'^add_command/', command.change_command, name='add_command'),

    #初始化url
    url(r'^init_list/', init.init_list,name='init_list'),
    url(r'^add_init/', init.change_init,name='add_init'),
    url(r'^edit_init/(?P<pk>\d+)', init.change_init,name='edit_init'),
    url(r'^detail_init/(?P<pk>\d+)', init.detail_init,name='detail_init'),
    url(r'^del_init/(\d+)', init.del_init,name='del_init'),

    # 增加初始化日志
    url(r'^createlog/', initlog.create_initlog,name='createlog'),

]
