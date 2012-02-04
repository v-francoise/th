#!/usr/bin/env python
import os
import sys

PYTHON_ROOT = 'C:/Python27'
DOCUMENT_ROOT = 'C:/Users/Sora/workspace/temple_horadrim'

# Ce bloc represente les Librairies presentes dans le PYTHONPATH (sous linux, definir cette variable d'environnement)
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/django')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/django_tinymce-1.5.1a2-py2.7.egg')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/pip-1.0.2-py2.7.egg')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/django_flag-0.2.dev10-py2.7.egg')
sys.path.append(PYTHON_ROOT + '/DLLs')
sys.path.append(PYTHON_ROOT + '/Lib')
sys.path.append(PYTHON_ROOT + '/Lib/plat-win')
sys.path.append(PYTHON_ROOT + '/Lib/Lib-tk')
sys.path.append(PYTHON_ROOT + '')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/PIL')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/win32')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/win32/Lib')
sys.path.append(PYTHON_ROOT + '/Lib/site-packages/Pythonwin')
sys.path.append(DOCUMENT_ROOT)  
sys.path.append(DOCUMENT_ROOT + '/src')  
sys.path.append(DOCUMENT_ROOT + '/src/temple_horadrim')  

os.environ['DJANGO_SETTINGS_MODULE'] = 'temple_horadrim.settings'
 
import django.core.handlers.wsgi  

application = django.core.handlers.wsgi.WSGIHandler()

path = DOCUMENT_ROOT
sys.path.append(path)
