def scanning_template(self):
        "Path to {ScanningTemplate}name.xml of experiment."
        tmpl = glob(_pattern(self.path, _additional_data, _scanning_template,
                        extension='*.xml'))
        if tmpl:
            return tmpl[0]
        else:
            return ''