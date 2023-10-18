def determine_paths(self, package_name=None, create_package_dir=False, dry_run=False):
        """Determine paths automatically and a little intelligently"""
        
        # Give preference to the environment variable here as it will not 
        # derefrence sym links
        self.project_dir = Path(os.getenv('PWD') or os.getcwd())
        
        # Try and work out the project name
        distribution = self.get_distribution()
        if distribution:
            # Get name from setup.py
            self.project_name = distribution.get_name()
        else:
            # ...failing that, use the current directory name
            self.project_name = self.project_dir.name
        
        # Descend into the 'src' directory to find the package 
        # if necessary
        if os.path.isdir(self.project_dir / "src"):
            package_search_dir = self.project_dir / "src"
        else:
            package_search_dir = self.project_dir

        created_package_dir = False
        if not package_name:
            # Lets try and work out the package_name from the project_name
            package_name = self.project_name.replace("-", "_")
            
            # Now do some fuzzy matching
            def get_matches(name):
                possibles = [n for n in os.listdir(package_search_dir) if os.path.isdir(package_search_dir / n)]
                return difflib.get_close_matches(name, possibles, n=1, cutoff=0.8)
            
            close = get_matches(package_name)
            
            # If no matches, try removing the first part of the package name
            # (e.g. django-guardian becomes guardian)
            if not close and "_" in package_name:
                short_package_name = "_".join(package_name.split("_")[1:])
                close = get_matches(short_package_name)
            
            if not close:
                if create_package_dir:
                    package_dir = package_search_dir / package_name
                    # Gets set to true even during dry run
                    created_package_dir = True
                    if not dry_run:
                        print("Creating package directory at %s" % package_dir)
                        os.mkdir(package_dir)
                    else:
                        print("Would have created package directory at %s" % package_dir)
                else:
                    raise CommandError("Could not guess the package name. Specify it using --name.")
            else:
                package_name = close[0]
        
        self.package_name = package_name
        self.package_dir = package_search_dir / package_name

        if not os.path.exists(self.package_dir) and not created_package_dir:
            raise CommandError("Package directory did not exist at %s. Perhaps specify it using --name" % self.package_dir)