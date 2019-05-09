from django import template

from comment.forms import CommentForm
from comment.models import Comment


register = template.Library()

@register.inclusion_tag('comment/block.html')
def comment_block(target):
    data = dict()
    data['target'] = target
    data['comment_form'] = CommentForm()
    data['comment_list'] = Comment.get_by_target(target)
    return data 
