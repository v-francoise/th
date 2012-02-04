from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from temple_horadrim.models import Dossier
import logging

# import the logging library

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_model_fields(model):
    return model._meta.fields

@dajaxice_register
def get_children_dajax(request, parent_id):
    dajax = Dajax()
    fields = get_model_fields(Dossier)
    results = Dossier.objects.filter(menu__id=parent_id)
    context = {
               'result_headers': fields,
               'results': results,
               }
    view = render_to_string('admin/change_sublist_results.html', RequestContext(request,context))
    dajax.assign("#myid", "innerHTML", view)
    return dajax.json()

@dajaxice_register
def get_children(request, parent_id):
#    view = render_block_to_string('test.html', 'result_list')
    fields = get_model_fields(Dossier)
    results = Dossier.objects.filter(menu__id=parent_id)
    context = {
               'result_headers': fields,
               'results': results,
               }
    view = render_to_string('admin/change_sublist_results.html', RequestContext(request,context))
    return simplejson.dumps({'value':'%s' % view})