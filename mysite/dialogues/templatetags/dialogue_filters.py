from django import template
import re

register = template.Library()

@register.filter
def split_dialogue(value):
    # 首先按换行符分割
    lines = value.split('\n')
    # 清理每行，移除空白行
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return cleaned_lines

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)