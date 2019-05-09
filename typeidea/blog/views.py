from datetime import date

from django.core.cache import cache
from django.db.models import F, Q
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

# from comment.forms import CommentForm
# from comment.models import Comment
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

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        # pv_key = 'pv:%s:%s' % (uid, self.request.path)
        # uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        pv_key = 'pv:{}:{}'.format(uid, self.request.path)
        uv_key = 'uv:{}:{}:{}'.format(uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


    # def get_context_data(self, **kwargs):
    #     # 重写get_context_data方法
    #     context = super().get_context_data(**kwargs)
    #     context['comment_form'] = CommentForm
    #     context['comment_list'] = Comment.get_by_target(self.request.path)
    #     return context


# 主页
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


# 搜索页
class SearchView(IndexView):
    # 重写get_context_data方法
    def get_context_data(self):
        context = super().get_context_data()
        context['keyword'] = self.request.GET.get('keyword', '')
        return context

    def get_queryset(self):
        # 重写queryset方法
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


# 根据指定作者显示特定博客
class AuthorView(IndexView):
    def get_queryset(self):
        # 重写queryset方法
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


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
