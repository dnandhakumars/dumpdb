from .base import CommonBaseCommand


class MysqlDump(CommonBaseCommand):
    """
        Run mysqldump command to backup and restore database
    """
    dump_cmd = 'mysqldump'
    restore_cmd = 'mysql'

    def _create_dump(self):
        cmd = '{} {} --quick'.format(self.dump_cmd, self.settings['NAME'])
        if self.settings.get('HOST'):
            cmd += ' --host={}'.format(self.settings['HOST'])
        if self.settings.get('PORT'):
            cmd += ' --port={}'.format(self.settings['PORT'])
        if self.settings.get('USER'):
            cmd += ' --user={}'.format(self.settings['USER'])
        if self.settings.get('PASSWORD'):
            cmd += ' --password={}'.format(self.settings['PASSWORD'])
        for table in self.exclude:
            cmd += ' --ignore-table={}.{}'.format(self.settings['NAME'], table)
        stdout, stderr = self.run_command(cmd)
        return stdout

    def _restore_dump(self, dump):
        cmd = '{} {}'.format(self.restore_cmd, self.settings['NAME'])
        if self.settings.get('HOST'):
            cmd += ' --host={}'.format(self.settings['HOST'])
        if self.settings.get('PORT'):
            cmd += ' --port={}'.format(self.settings['PORT'])
        if self.settings.get('USER'):
            cmd += ' --user={}'.format(self.settings['USER'])
        if self.settings.get('PASSWORD'):
            cmd += ' --password={}'.format(self.settings['PASSWORD'])
            
        stdout, stderr = self.run_command(cmd, stdin=dump)
        return stdout, stderr
