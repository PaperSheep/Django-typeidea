from django.urls import path, include

from . import views


urlpatterns = [
    # 改用类视图
    # path('', views.post_list, name='post_list_total'),
    # path('category/<int:category_id>', views.post_list, name='post_list_category'),
    # path('tag/<int:tag_id>', views.post_list, name='post_list_tag'),
    # path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('', views.IndexView.as_view(), name='post_list_total'),
    path('category/<int:category_id>', views.CategoryView.as_view(), name='post_list_category'),
    path('tag/<int:tag_id>', views.TagView.as_view(), name='post_list_tag'),
    path('post/<int:post_id>', views.PostDetailView.as_view(), name='post_detail'),
]
