from django.conf.urls import url
from web.views import home
from web.views import user,host,cron,team



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

]
