from django.conf.urls import url
from web.views import home
from web.views import user



urlpatterns = [
    url(r'^home/', home.home,name='home'),

    url(r'^user_list/', user.user_list,name='user_list'),
    url(r'^add_user/', user.change_user,name='add_user'),
    url(r'^edit_user/(?P<pk>\d+)', user.change_user,name='edit_user'),
    url(r'^del_user/(\d+)', user.del_user,name='del_user'),
]
