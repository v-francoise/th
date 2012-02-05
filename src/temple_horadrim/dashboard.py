# -*- coding: utf-8 -*- 
from admin_tools.dashboard import modules
from django.utils.translation import ugettext_lazy as _
from fluent_dashboard import appsettings
from fluent_dashboard.dashboard import FluentIndexDashboard, \
    FluentAppIndexDashboard
from fluent_dashboard.modules import AppIconList


class CustomFluentIndexDashboard(FluentIndexDashboard):
    def __init__(self, **kwargs):
        super(CustomFluentIndexDashboard, self).__init__(**kwargs)
        self.children.append(modules.Group(
            title="Sections",
            display="tabs",
            draggable=False,
            deletable=False,
            children=[
                modules.AppList(
                    title=_(u'Général'),
                    models=(
                            'temple_horadrim.models.Livre',
                            'temple_horadrim.models.Comment',
                            'temple_horadrim.models.Actualite',
                            ),
                ),
                modules.AppList(
                    title='Section Diablo',
                    models=(
                            'temple_horadrim.models.Diablo',
                            'temple_horadrim.models.VideoDiablo',
                            )
                ),
                modules.AppList(
                    title='Section Starcraft',
                    models=(
                            'temple_horadrim.models.Starcraft',
                            'temple_horadrim.models.VideoStarcraft',
                            )
                ),
            ]
        ))
        self.children.append(modules.LinkList(
            children=(
                        {
                            'title': 'File Browser',
                            'url': '/admin/filebrowser/',
                            'external': False,
                            'description': 'Python programming language rocks !',
                        },
                      ),
        ))


class CustomFluentAppIndexDashboard(FluentAppIndexDashboard):
    def __init__(self, app_title, models, **kwargs):
        super(CustomFluentAppIndexDashboard, self).__init__(app_title, models, **kwargs)
        self.children.append(modules.Group(
            title="Sections",
            display="tabs",
            draggable=False,
            deletable=False,
            children=[
                modules.AppList(
                    title=_(u'Général'),
                    models=(
                            'temple_horadrim.models.Livre',
                            'temple_horadrim.models.Comment',
                            'temple_horadrim.models.Actualite',
                            ),
#                    exclude=(
#                            'temple_horadrim.models.Dossier',
#                            'temple_horadrim.models.Clip',
#                            'temple_horadrim.models.Video',
#                            'contrib.admin.auth.Profile',
#                            )
                ),
                modules.AppList(
                    title='Section Diablo',
                    models=(
                            'temple_horadrim.models.Diablo',
                            'temple_horadrim.models.ClipDiablo',
                            'temple_horadrim.models.VideoDiablo'
                            )
                ),
                modules.AppList(
                    title='Section Starcraft',
                    models=(
                            'temple_horadrim.models.Starcraft',
                            'temple_horadrim.models.ClipStarcraft',
                            'temple_horadrim.models.VideoStarcraft'
                            )
                )
            ]
        ))
        
class CustomAppIconList(AppIconList):
    def __init__(self, *args, **kwargs):
        super(CustomAppIconList, self).__init__(*args, **kwargs)
    def init_with_context(self, context):
        """
        Initializes the icon list.
        """
        super(AppIconList, self).init_with_context(context)
        apps = self.children
        path_levels = context['request'].META['SCRIPT_NAME'].rstrip('/').count('/')

        # Standard model only has a title, change_url and add_url.
        # Restore the app_name and name, so icons can be matched.
        for app in apps:
            app_name = app['url'].strip('/').split('/')[-1]   # /admin/appname/
            app['name'] = app_name

            for model in app['models']:
                try:
                    model_name = model['change_url'].strip('/').split('/')[1 + path_levels]   # admin/appname/modelname
                    model['name'] = model_name
                    model['icon'] = self.get_icon_for_model(app_name, model_name) or appsettings.FLUENT_DASHBOARD_DEFAULT_ICON
#                    raise ImproperlyConfigured("DEBUG : app_name = %s and model_name = %s" % (app_name, self.children))
                except ValueError:
                    model['icon'] = appsettings.FLUENT_DASHBOARD_DEFAULT_ICON

                # Automatically add STATIC_URL before relative icon paths.
                model['icon'] = self.get_icon_url(model['icon'])
                model['app_name'] = app_name