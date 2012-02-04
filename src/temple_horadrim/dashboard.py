# -*- coding: utf-8 -*- 
from admin_tools.dashboard import modules
from django.utils.translation import ugettext_lazy as _
from fluent_dashboard.dashboard import FluentIndexDashboard, \
    FluentAppIndexDashboard


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
