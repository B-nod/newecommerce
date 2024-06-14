from django.urls import path
from . import views

urlpatterns=[
    path('addblog/',views.add_blog,name='addblog'),
    path('showblog/',views.show_blog,name='showblog'),
    path('updateblog/<int:blog_id>/',views.update_blog,name='updateblog'),
    path('deleteblog/<int:blog_id>/',views.del_blog,name='deleteblog'),
    path('blogdetail/<int:blog_id>/', views.blog_detail, name='blogdetail'),
    path('blogs/', views.blogpage, name='blogs'),
]