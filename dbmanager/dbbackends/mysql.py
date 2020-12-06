from .base import CommonBaseCommand


class MysqlDump(CommonBaseCommand):
    """
        Run mysqldump/mysql command to backup and restore database
    """
    backup_cmd = 'mysqldump'
    restore_cmd = 'mysql'

    def _create_dump(self):
        cmd = '{} {} --quick'.format(self.backup_cmd, self.settings['NAME'])
        if self.settings.get('HOST'):
            cmd += ' --host={}'.format(self.settings['HOST'])
        if self.settings.get('PORT'):
            cmd += ' --port={}'.format(self.settings['PORT'])
        if self.settings.get('USER'):
            cmd += ' --user={}'.format(self.settings['USER'])
        if self.settings.get('PASSWORD'):
            cmd += ' --password={}'.format(self.settings['PASSWORD'])
        for rtable in self.req_tables:
            cmd += ' {}'.format(rtable)
        for itable in self.ignore_tabled:
            cmd += ' --ignore-table={}'.format(itable)
        stdout, stderr = self.run_command(cmd)
        return stdout

    def _restore_dump(self, dump_file):
        cmd = '{} {}'.format(self.restore_cmd, self.settings['NAME'])
        if self.settings.get('HOST'):
            cmd += ' --host={}'.format(self.settings['HOST'])
        if self.settings.get('PORT'):
            cmd += ' --port={}'.format(self.settings['PORT'])
        if self.settings.get('USER'):
            cmd += ' --user={}'.format(self.settings['USER'])
        if self.settings.get('PASSWORD'):
            cmd += ' --password={}'.format(self.settings['PASSWORD'])
        dump_file.seek(0)
        stdout, stderr = self.run_command(cmd, stdin=dump_file)
        return stdout, stderr
