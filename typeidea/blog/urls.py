from django.urls import path, include

from . import views


urlpatterns = [
	path('', views.post_list, name='post_list_total'),
	path('category/<int:category_id>', views.post_list, name='post_list_category'),
	path('tag/<int:tag_id>', views.post_list, name='post_list_tag'),
	path('post/<int:post_id>', views.post_detail, name='post_detail'),
]
