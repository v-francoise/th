from django.contrib.admin.templatetags.admin_list import result_hidden_fields, \
    result_headers, results
from django.template import Library
from temple_horadrim.models import Dossier
import logging
# import the logging library

# Get an instance of a logger
logger = logging.getLogger(__name__)

register = Library()

@register.inclusion_tag('admin/change_tree_results.html')
def result_tree_list(cl):
    """
    Displays the headers and data list together
    """
    logger.error(cl)
#    logger.error(cl.result_list)
#    logger.error(list(results(cl)))
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl))}
    
@register.inclusion_tag('admin/change_sublist_results.html')
def related_dossiers(menu):
    dossiers = Dossier.objects.filter(menu=menu.id)
    return {
            'menu' : menu,
            'dossiers' : dossiers,
            'dossiers_list' : list(results(dossiers)),
            }