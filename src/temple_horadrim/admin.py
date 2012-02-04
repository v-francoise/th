# -*- coding: utf-8 -*- 
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.utils.log import logger
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm
from temple_horadrim.models import Comment, Dossier, Livre, Menu, Actualite, \
    Video, UserProfile, Profile, Diablo, Starcraft, VideoDiablo, VideoStarcraft, \
    Section
import pprint
import re
    
class ActualiteAdmin(admin.ModelAdmin):
    """
    Admin Model for Article
    """
    fields = ['titre', 'section', 'contenu', 'auteur']
    list_display = ('titre' , 'section', 'date', 'auteur')
    class Meta:
        model = Actualite
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ('titre', 'list_children')
    
    def list_children(self, obj):
        url = urlresolvers.reverse('admin:temple_horadrim_dossier_changelist')
        return '<a href="{0}?menu__id__exact={1}" id="myid">Sous-menus</a>'.format(url, obj.id)
    list_children.allow_tags = True
    list_children.short_description = 'Children'

    class Media:
#        css = {
#            "all": ("my_styles.css",)
#        }
        js = ("temple_horadrim/js/ajax.js",)
    
    class Meta:
        model = Menu

class VideoAdminForm(forms.ModelForm):
    class Meta:
        model = Video
    def check_link(self, url):
        # format long
        regexLong = r'^http:\/\/(www\.)?youtube\.com\/watch\?v=(?P<code>[\w-]+.*)$'
        # format court
        regexShort = r'^http:\/\/youtu\.be\/(?P<code>[\w-]+.*)$'
        
        if(re.search(regexLong, url) or re.search(regexShort, url)):
            return True
        else:
            return False
        
    def youtube_extract(self, url):
        # format long
        regexLong = r'^http:\/\/(www\.)?youtube\.com\/watch\?v=(?P<code>[\w-]+.*)$'
        keyLong = re.sub(regexLong, r'\g<code>', url)
        logger.debug(keyLong)
        # format court
        regexShort = r'^http:\/\/youtu\.be\/(?P<code>[\w-]+.*)$'
        keyShort = re.sub(regexShort, r'\g<code>', url)
         
        if(keyLong != url):
            return keyLong
        elif (keyShort != url):
            return keyShort
        else:
            return False

    def clean_code(self):
        logger.error('Code field value = %s' % self.cleaned_data["code"])
        if self.check_link(self.cleaned_data["code"]):
            logger.info("if link ok")
            print "if link OK"
            self.cleaned_data["code"] = self.youtube_extract(self.cleaned_data["code"])
            return self.cleaned_data["code"]
        else:
            raise forms.ValidationError("Error ! Url not valid !")

class ClipModelAdmin(admin.ModelAdmin):
    form = VideoAdminForm  
    class Meta:
        model = Video

class VideoStarcraftAdmin(admin.ModelAdmin):
    form = VideoAdminForm  
    
    def queryset(self, request):
        return Video.objects.select_related("section").filter(section__id=2)
    
    class Meta:
        model = Video

class VideoDiabloAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    
    def queryset(self, request):
        return Video.objects.select_related("section").filter(section__id=1)
    
    class Meta:
        model = Video
        
class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    
class DossierModelForm(MPTTAdminForm):
    def __init__(self,*args,**kwargs):
        super (MPTTAdminForm,self ).__init__(*args,**kwargs)
        self.section_id = 1 if isinstance(self.instance, Diablo) else 2 if isinstance(self.instance, Starcraft) else 3
        if self.section_id != None:
            self.fields["section"].queryset = Section.objects.filter(pk=self.section_id)
            self.fields["parent"].queryset = Dossier.objects.select_related("section").filter(section__id=self.section_id)
            self.initial["section"] = self.section_id
            
    def clean_section(self):
        if self.section_id != self.cleaned_data["section"].id:
            raise forms.ValidationError("Section not valid ! id = %s & cleaned id = %s" % (self.section_id, self.cleaned_data["section"].id))
        else:
            return self.cleaned_data["section"]
    def clean_parent(self):
        pprint.pprint(self.cleaned_data)
        if type(self.cleaned_data["parent"]) != None:
            if self.cleaned_data["parent"].level >= 1:
                raise forms.ValidationError("Cannot have more than one parent !")
            else:
                return self.cleaned_data["parent"]
        else:
            return self.cleaned_data["parent"]
    class Meta:
        model = Dossier
        
class DiabloAdmin(MPTTModelAdmin):
    form = DossierModelForm
    def __init__(self, model, admin_site):
        MPTTModelAdmin.__init__(self, model, admin_site)
    
    class Meta:
        model = Diablo

    
class StarcraftAdmin(MPTTModelAdmin):
    form = DossierModelForm
    class Meta:
        model = Starcraft

admin.site.unregister(User)

admin.site.register(User, UserProfileAdmin)
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Comment)
#admin.site.register(Menu, MenuAdmin)
admin.site.register(Livre)
admin.site.register(Dossier)
admin.site.register(Actualite, ActualiteAdmin)
admin.site.register(Video, MPTTModelAdmin)
#admin.site.register(Clip, ClipModelAdmin)
admin.site.register(VideoDiablo, VideoDiabloAdmin)
admin.site.register(VideoStarcraft, VideoStarcraftAdmin)
admin.site.register(Diablo, DiabloAdmin)
admin.site.register(Starcraft, StarcraftAdmin)
