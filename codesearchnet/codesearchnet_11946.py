def drop_views(self, name=None, site=None):
        """
        Drops all views.
        """
        r = self.database_renderer
        result = r.sudo("mysql --batch -v -h {db_host} "
            #"-u {db_root_username} -p'{db_root_password}' "
            "-u {db_user} -p'{db_password}' "
            "--execute=\"SELECT GROUP_CONCAT(CONCAT(TABLE_SCHEMA,'.',table_name) SEPARATOR ', ') AS views "
            "FROM INFORMATION_SCHEMA.views WHERE TABLE_SCHEMA = '{db_name}' ORDER BY table_name DESC;\"")
        result = re.findall(
            r'^views[\s\t\r\n]+(.*)',
            result,
            flags=re.IGNORECASE|re.DOTALL|re.MULTILINE)
        if not result:
            return
        r.env.db_view_list = result[0]
        #cmd = ("mysql -v -h {db_host} -u {db_root_username} -p'{db_root_password}' " \
        r.sudo("mysql -v -h {db_host} -u {db_user} -p'{db_password}' " \
            "--execute=\"DROP VIEW {db_view_list} CASCADE;\"")