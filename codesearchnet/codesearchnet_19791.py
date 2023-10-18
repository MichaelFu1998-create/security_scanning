def find_imports(self, pbds):
        """Find all missing imports in list of Pbd instances.
        """
        # List of types used, but not defined
        imports = list(set(self.uses).difference(set(self.defines)))
        
        # Clumpsy, but enought for now 
        for imp in imports:
            for p in pbds:
                if imp in p.defines:
                    self.imports.append(p.name)
                    break
        
        self.imports = list(set(self.imports))
        
        for import_file in self.imports:
            self.lines.insert(2, 'import "{}";'.format(import_file))