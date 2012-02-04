'''
Created on 25 janv. 2012

@author: Sora
'''
#import Image
#    
#
#im = Image.open("http://localhost:8000/media/uploads/2012/01/25/P1030028_thumb.JPG")
#im.show()
from django.core import urlresolvers
from django.template.context import Context
from django.template.loader import render_to_string
from temple_horadrim.ajax import get_model_fields
from temple_horadrim.models import Dossier, Menu
from temple_horadrim.settings import MEDIA_ROOT, DIRECTORY
import os
import pprint
import re

def test_dajax():
    id = 38
    url = urlresolvers.reverse('admin:temple_horadrim_dossier_changelist')
    url = "%s%s" % ("http://localhost:8000", url)
    #    view = render_block_to_string('test.html', 'result_list')
    menu = Menu.objects.get(pk=id)
    fields = get_model_fields(Dossier)
    results = menu.dossier_set.all()
    context = {
               'result_headers': fields,
               'results': results,
               }
    view = render_to_string('admin/change_sublist_results.html', Context(context))
    print view

url = "http://www.youtube.com/watch?v=HuC2MUmQaG4"

def youtube_extract(url):
    # format long
    regexLong = r'^http:\/\/(www\.)?youtube\.com\/watch\?v=(?P<code>[\w-]+.*)$'
    keyLong = re.sub(regexLong, r'\g<code>', url)
    print " keyLong = %s" % keyLong
#    logger.debug(keyLong)
    # format court
    regexShort = r'^http:\/\/youtu\.be\/(?P<code>[\w-]+.*)'
    keyShort = re.sub(regexShort, r'\g<code>', url)
     
    if(keyLong != url):
        return keyLong
    elif (keyShort != url):
        return keyShort
    else:
        return False

def check_link(url):
    # format long
    regexLong = r'^http:\/\/(www\.)?youtube\.com\/watch\?v=(?P<code>[\w-]+.*)$'
    # format court
    regexShort = r'^http:\/\/youtu\.be\/(?P<code>[\w-]+.*)$'
    
    if(re.search(regexLong, url) or re.search(regexShort, url)):
        return True
    else:
        return False

def clean_code(url):
#    logger.error('Code field value = %s' % self.cleaned_data["code"])
    if check_link(url):
#        logger.info("if link ok")
        print "if link OK"
        url = youtube_extract(url)
        return url
    else:
        print "Error !"
#        raise forms.ValidationError("Error ! Url NOT VALID")    

def test_clean_code():
    print "Final return = %s" % clean_code(url)
    
meta = {'proxy' : True, 'verbose_name' : "Toto"}

for item in meta:
    print "%s = %s" % (item, meta[item])
    
class Test(object):
    def __init__(self):
        self.name = "test"
        self.value = "test value"
    
#pprint.pprint([0,1,2,3])
#value = pprint.pformat(Test())
#print value


def get_path(path):
    """
    Get Path.
    """
    print os.path.join(MEDIA_ROOT, DIRECTORY, path)
    if path.startswith('.'):
        print "1ere condition True"
    if os.path.isabs(path):
        print "2eme condition True"
    if not os.path.isdir(os.path.join(MEDIA_ROOT, DIRECTORY, path)):
        print "3eme condition True"
    
    if path.startswith('.') or os.path.isabs(path) or not os.path.isdir(os.path.join(MEDIA_ROOT, DIRECTORY, path)):
        return None
    print path

get_path('')

    

