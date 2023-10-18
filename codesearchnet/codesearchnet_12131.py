def get(self):
        '''This handles GET requests to the index page.

        TODO: provide the correct baseurl from the checkplotserver options dict,
        so the frontend JS can just read that off immediately.

        '''

        # generate the project's list of checkplots
        project_checkplots = self.currentproject['checkplots']
        project_checkplotbasenames = [os.path.basename(x)
                                      for x in project_checkplots]
        project_checkplotindices = range(len(project_checkplots))

        # get the sortkey and order
        project_cpsortkey = self.currentproject['sortkey']
        if self.currentproject['sortorder'] == 'asc':
            project_cpsortorder = 'ascending'
        elif self.currentproject['sortorder'] == 'desc':
            project_cpsortorder = 'descending'

        # get the filterkey and condition
        project_cpfilterstatements = self.currentproject['filterstatements']

        self.render('cpindex.html',
                    project_checkplots=project_checkplots,
                    project_cpsortorder=project_cpsortorder,
                    project_cpsortkey=project_cpsortkey,
                    project_cpfilterstatements=project_cpfilterstatements,
                    project_checkplotbasenames=project_checkplotbasenames,
                    project_checkplotindices=project_checkplotindices,
                    project_checkplotfile=self.cplistfile,
                    readonly=self.readonly,
                    baseurl=self.baseurl)