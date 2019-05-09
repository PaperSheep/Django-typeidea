from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        if comment_form.is_valid():
            # save方法不会理解将表单数据存储到数据库，而是给你返回一个当前对象。
            # 这时你可以添加表单以外的额外数据，再一起存储
            instance = comment_form.save(commit=False)  # 先暂时返回comment模型的数据
            # 把target录入后再存进数据库里
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = dict()
        context['succeed'] = succeed
        context['form'] = comment_form
        context['target'] = target
        # 数据失败填写错误的时候会跳到单独的页面
        return self.render_to_response(context)
