from django.urls import path

from . import views


urlpatterns = [
    # 改用类视图
    # path('', views.post_list, name='post_list_total'),
    # path('category/<int:category_id>', views.post_list, name='post_list_category'),
    # path('tag/<int:tag_id>', views.post_list, name='post_list_tag'),
    # path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('', views.IndexView.as_view(), name='post_list_total'),  # 主页(博客列表)
    path('category/<int:category_id>', views.CategoryView.as_view(), name='post_list_category'),  # 分类页
    path('tag/<int:tag_id>', views.TagView.as_view(), name='post_list_tag'),  # 标签页
    path('post/<int:post_id>', views.PostDetailView.as_view(), name='post_detail'),  # 详情页
    path('search/', views.SearchView.as_view(), name='search'),  # 搜索页
    path('author/<int:owner_id>', views.AuthorView.as_view(), name='author'),  # 作者博客页
]
