def verify_editor(self):
        """Verify if the software used in the changeset is a powerfull_editor.
        """
        powerful_editors = [
            'josm', 'level0', 'merkaartor', 'qgis', 'arcgis', 'upload.py',
            'osmapi', 'Services_OpenStreetMap'
            ]
        if self.editor is not None:
            for editor in powerful_editors:
                if editor in self.editor.lower():
                    self.powerfull_editor = True
                    break

            if 'iD' in self.editor:
                trusted_hosts = [
                    'www.openstreetmap.org/id',
                    'www.openstreetmap.org/edit',
                    'improveosm.org',
                    'strava.github.io/iD',
                    'preview.ideditor.com/release',
                    'preview.ideditor.com/master',
                    'hey.mapbox.com/iD-internal',
                    'projets.pavie.info/id-indoor',
                    'maps.mapcat.com/edit',
                    'id.softek.ir'
                    ]
                if self.host.split('://')[-1].strip('/') not in trusted_hosts:
                    self.label_suspicious('Unknown iD instance')
        else:
            self.powerfull_editor = True
            self.label_suspicious('Software editor was not declared')