# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from config.models import SideBar
from .models import Post, Category, Tag


class CommonViewMixin:
    # 获取侧边栏数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebars'] = SideBar.get_all()
        context.update(Category.get_navs())
        return context


# 博客详情页
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()  # 获取了所有博客数据
    template_name = 'blog/detail.html'  # 指定模板页面
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'  # url传进来的参数


# 主页
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


# 分类页
class CategoryView(IndexView):
    # 重写get_context_data方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')  # 从Url参数里获取category_id参数
        category = get_object_or_404(Category, pk=category_id)
        context['category'] = category
        return context

    def get_queryset(self):
        # 重写queryset方法，重写为根据分类过滤
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

# 标签页
class TagView(IndexView):
    # 重些get_context_data方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')  # 从Url参数里获取tag_id参数
        tag = get_object_or_404(Tag, pk=tag_id)
        context['tag'] = tag
        return context

    def get_queryset(self):
        # 重写queryset方法，重写为根据标签过滤
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


# 改为类视图
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None

#     if tag_id:
#         posts, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         posts, category = Post.get_by_category(category_id)
#     else:
#         posts = Post.latest_posts()

#     context = dict()
#     context['tag'] = tag
#     context['category'] = category
#     context['post_list'] = posts
#     context['sidebars'] = SideBar.get_all()
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context)

# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = dict()
#     context['post'] = post
#     context['sidebars'] = SideBar.get_all()
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
