# -*- coding: utf-8 -*- 
from ckeditor.fields import RichTextField
from django.contrib.auth.management import create_permissions, \
    _get_all_permissions
from django.contrib.auth.models import User
from django.db import models
from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.utils.encoding import smart_unicode
from filebrowser.fields import FileBrowseField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from temple_horadrim import string_with_title
from temple_horadrim.fields.fields import YoutubeCodeField
import datetime

class UserProfile(models.Model):
    """
    Extension for User
    Adds fields to User
    """
    user = models.OneToOneField(User, parent_link=True, related_name='userprofile')
    avatar = FileBrowseField("Avatar", max_length=200, directory="uploads/image/", format='image', blank=True, null=True)

class Section(models.Model):
    name = models.SlugField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    valide = models.IntegerField()
    auteur = models.CharField(max_length=300)
    message = models.TextField()
    idnews = models.IntegerField()
    date = models.BigIntegerField()
    section = models.IntegerField()
    
    def __unicode__(self):
        return self.message
    
    class Meta:
        db_table = u'comments'
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class Menu(models.Model):
    section = models.ForeignKey(Section,db_column='section')
    titre = models.CharField(max_length=300)
    introduction = models.TextField()
    
    def __unicode__(self):
        return self.titre
    
    class Meta:
        db_table = u'menu'
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class Dossier(MPTTModel):
    section = models.ForeignKey(Section)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    titre = models.CharField(max_length=300)
    # Can be either introduction or content
    content = models.TextField()
    
    def __unicode__(self):
        return self.titre
    
    class MPTTMeta:
        order_insertion_by = ['titre']
        parent_attr = 'parent'

    class Meta:
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")
#        verbose_name = _("Dossier")
#        verbose_name_plural = _("Dossiers")

class Livre(models.Model):
    pseudo = models.CharField(max_length=300)
    message = models.TextField()
    date = models.BigIntegerField()
    
    def __unicode__(self):
        return self.message[:50]
        
    class Meta:
        db_table = u'livre'
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class Actualite(models.Model):
    section = models.ForeignKey(Section,db_column='section')
    titre = models.CharField(max_length=300)
    contenu = RichTextField()
    date = models.DateTimeField()
    auteur = models.ForeignKey(User,db_column='auteur')
    
    def save(self):
        self.date = datetime.datetime.now();
        super(Actualite,self).save()
    
    def __unicode__(self):
        return self.titre
    
    class Meta:
        db_table = u'news'
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class Video(MPTTModel):
    section = models.ForeignKey(Section,db_column='section')
    #Code video Youtube
    code = YoutubeCodeField(max_length=300)
    titre = models.CharField(max_length=300)
    dossier = models.ForeignKey(Dossier)
    details = models.TextField()
    date = models.DateTimeField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.titre

    class MPTTMeta:
        order_insertion_by = ['titre']
        
    class Meta:
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class TypeAwareManager(models.Manager):
    def __init__(self,model, *args, **kwargs):
        super(TypeAwareManager, self).__init__(*args, **kwargs)
        self.type = 1 if model == "dossier_diablo" else 2 if model == "dossier_starcraft" else 3

    def get_query_set(self):
        return super(TypeAwareManager, self).get_query_set().filter(section=self.type)

class Diablo(Dossier):
    """
    Proxy Model 
    Displays Dossiers related to the Diablo section
    """
    objects = TypeAwareManager('dossier_diablo')
    class Meta:
        proxy = True
        verbose_name = "Dossier Diablo"
        verbose_name_plural = "Dossiers Diablo"
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class Starcraft(Dossier):
    """
    Proxy Model 
    Displays Dossiers related to the Starcraft section
    """
    objects = TypeAwareManager('dossier_starcraft')
    class Meta:
        proxy = True
        verbose_name = "Dossier Starcraft"
        verbose_name_plural = "Dossiers Starcraft"
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class VideoStarcraft(Video):
    """
    Proxy Model 
    Displays Videos related to the Starcraft section
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Videos Starcraft"
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class VideoDiablo(Video):
    """
    Proxy Model 
    Displays Videos related to the Diablo section
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Videos Diablo"
        app_label = string_with_title("temple_horadrim", "Temple Horadrim")

class Profile(UserProfile):
    """
    Proxy Model 
    Displays Profile related to the current user
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Profile"
        app_label = "auth"

        
# Hack the postsyncdb signal, so we can fix the misbehavior of the
# content_type
# assignment to the proxy models.
# see http://code.djangoproject.com/ticket/11154

def create_permissions_respecting_proxy(
    app, created_models, verbosity, **kwargs
    ):
    if not kwargs['sender'].__name__ == 'myproject.myapp.models':
        # if not in 'customer' app, then use the original function
        create_permissions(app, created_models, verbosity, **kwargs)
        return

    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth import models as auth_app
    app_models = get_models(app)
    searched_perms = list()
    ctypes = set()
    for klass in app_models:
        # this is where the difference is: the original create_permissions
        # use ctype = ContentType.objects.get_for_model(klass)
        opts = klass._meta
        ctype = ContentType.objects.get_or_create(
            app_label=opts.app_label,
            model=opts.object_name.lower(),
            defaults = {'name': smart_unicode(opts.verbose_name_raw)}
            )
        # end of the modification
        ctypes.add(ctype)
        for perm in _get_all_permissions(klass._meta):
            searched_perms.append((ctype, perm))

    all_perms = set(auth_app.Permission.objects.filter(
            content_type__in=ctypes
            ).values_list("content_type", "codename"))

    for ctype, (codename, name) in searched_perms:
        if(ctype.pk, codename) in all_perms:
            continue
        p = auth_app.Permission.objects.create(
            codename=codename, name=name, content_type=ctype
            )
        if verbosity >=2:
            print "Adding permission '%s'" % p


post_syncdb.disconnect(
    create_permissions,
    dispatch_uid='django.contrib.auth.management.create_permissions',
    )

post_syncdb.connect(
    create_permissions_respecting_proxy,
    dispatch_uid='django.contrib.auth.management.create_permissions',
    )