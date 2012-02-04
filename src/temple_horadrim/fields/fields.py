from django import forms
from django.db import models

class YoutubeString(object):
    domain = "www.youtube.com"
    
    def __init__(self,code):
        self.code = code
        self.value = "http://%s/watch?v=%s" % (self.domain, code)
        
    def __unicode__(self):
        return self.value
        
    def __str__(self):
        return self.value
    
class YoutubeCodeField(models.CharField):
    description = "Code de la video youtube"

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(YoutubeCodeField, self).__init__(*args, **kwargs)
    
    def value_to_string(self, obj):
        return obj.value

    def to_python(self, value):
        if isinstance(value, YoutubeString):
            return value.code
        else:
            return YoutubeString(value)