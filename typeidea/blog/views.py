from typing import Dict, List, Any, Union

from django.shortcuts import render

from .models import Post, Category


def post_list(request, category_id=None, tag_id=None):
	tag = None
	category = None

	if tag_id:
		posts, tag = Post.get_by_tag(tag_id)
	elif category_id:
		posts, category = Post.get_by_category(category_id)
	else:
		posts = Post.latest_posts()

	context = dict()
	context['tag'] = tag
	context['category'] = category
	context['post_list'] = posts
	context.update(Category.get_navs())
	return render(request, 'blog/list.html', context)

def post_detail(request, post_id=None):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		post = None
	context = dict()
	context['post'] = post
	context.update(Category.get_navs())
	return render(request, 'blog/detail.html', context=context)
