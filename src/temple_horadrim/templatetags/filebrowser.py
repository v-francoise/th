from django.template.defaulttags import register

@register.inclusion_tag('filebrowser/append.html')
def result_tree_list():
    return {}