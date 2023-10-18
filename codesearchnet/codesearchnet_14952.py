def get_or_create_current_instance(cls):
        """Get the instance model corresponding to the current system, or create a new
        one if the system is new or its properties have changed (e.g. OS from upgrade)."""

        # on Android, platform.platform() barfs, so we handle that safely here
        try:
            plat = platform.platform()
        except:
            plat = "Unknown (Android?)"

        kwargs = {
            "platform": plat,
            "hostname": platform.node(),
            "sysversion": sys.version,
            "database": DatabaseIDModel.get_or_create_current_database_id(),
            "db_path": os.path.abspath(settings.DATABASES['default']['NAME']),
            "system_id": os.environ.get("MORANGO_SYSTEM_ID", ""),
        }

        # try to get the MAC address, but exclude it if it was a fake (random) address
        mac = uuid.getnode()
        if (mac >> 40) % 2 == 0:  # 8th bit (of 48 bits, from left) is 1 if MAC is fake
            hashable_identifier = "{}:{}".format(kwargs['database'].id, mac)
            kwargs["node_id"] = hashlib.sha1(hashable_identifier.encode('utf-8')).hexdigest()[:20]
        else:
            kwargs["node_id"] = ""

        # do within transaction so we only ever have 1 current instance ID
        with transaction.atomic():
            InstanceIDModel.objects.filter(current=True).update(current=False)
            obj, created = InstanceIDModel.objects.get_or_create(**kwargs)
            obj.current = True
            obj.save()

        return obj, created