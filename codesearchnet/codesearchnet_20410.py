def create_project(self):
        """
        Creates a base Flask project

        """
        if os.path.exists(self._py):
            prj_dir = os.path.join(self._app_dir, self._project_name)
            if os.path.exists(prj_dir):
                if self._force:
                    logging.warn('Removing existing project')
                    shutil.rmtree(prj_dir)
                else:
                    logging.warn('Found existing project; not creating (use --force to overwrite)')
                    return
            logging.info('Creating project')
            os.makedirs(prj_dir)
            # create the flask project stub
            app = """#!/usr/bin/env python\n"""\
            """from flask import Flask\n"""\
            """app = Flask(__name__)\n\n"""\
            """@app.route(\"/\")\n"""\
            """def hello():\n"""\
            """    return \"Hello from Flask...\"\n\n"""\
            """if __name__==\"__main__\":\n"""\
            """    app.run()\n\n"""
            with open(os.path.join(prj_dir, 'app.py'), 'w') as f:
                f.write(app)
        else:
            logging.error('Unable to find Python interpreter in virtualenv')
            return