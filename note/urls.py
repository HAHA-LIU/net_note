from django.conf.urls import url
from . import views
urlpatterns = [
    #127.0.0.1:8000/note/   显示用户所有笔记页面
    url(r'^$',views.list_view),
    #127.0.0.1:8000/note/index    主页
    url(r'^index$',views.note_index),
    # url(r'^index/$',views.note_index),  # 302 加斜杠
    # 127.0.0.1:8000/note/add
    url(r'^add',views.add_view),   # 增加
    url(r'^mod/(\d+)',views.mod_view),  # 修改
    url(r'^con/(\d+)',views.con_view),  # 查看
    url(r'^del/(\d+)',views.del_view),
    url(r'^page_test',views.page_test)
]