from django.core.management.base import BaseCommand
#from djutils.queue.decorators import periodic_command, crontab
import os
import popen2
import time
#
#@periodic_command(crontab(hour='0', minute='0'))
class Command(BaseCommand):
    help_text = "Backup database. Only Mysql and Postgresql engines are implemented"

    def handle(self, *args, **options):
        from django.conf import settings

        self.engine = settings.DATABASES["default"]["ENGINE"]
        self.db = settings.DATABASES["default"]["NAME"]
        self.user = settings.DATABASES["default"]["USER"]
        self.passwd = settings.DATABASES["default"]["PASSWORD"]
        self.host = settings.DATABASES["default"]["HOST"]
        self.port = settings.DATABASES["default"]["PORT"]

        backup_dir = '../../resources/backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        outfile = os.path.join(backup_dir, 'backup_%s_%s.sql' % (time.strftime('%d-%m-%y'), time.strftime('%Hh%M')))

        if self.engine == 'django.db.backends.mysql':
            print 'Doing Mysql backup to database %s into %s' % (self.db, outfile)
            self.do_mysql_backup(outfile)
        elif self.engine in ('postgresql_psycopg2', 'postgresql'):
            print 'Doing Postgresql backup to database %s into %s' % (self.db, outfile)
            self.do_postgresql_backup(outfile)
        else:
            print 'Backup in %s engine not implemented' % self.engine

    def do_mysql_backup(self, outfile):
        args = []
        if self.user:
            args += ["--user=%s" % self.user]
        if self.passwd:
            args += ["--password=%s" % self.passwd]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        args += [self.db]

        os.system('mysqldump %s > %s' % (' '.join(args), outfile))

    def do_postgresql_backup(self, outfile):
        args = []
        if self.user:
            args += ["--username=%s" % self.user]
        if self.passwd:
            args += ["--password"]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        if self.db:
            args += [self.db]
        pipe = popen2.Popen4('pg_dump %s > %s' % (' '.join(args), outfile))
        if self.passwd:
            pipe.tochild.write('%s\n' % self.passwd)
            pipe.tochild.close()