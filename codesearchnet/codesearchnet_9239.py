def general_params(cls):
        """ Define all the possible config params """

        params = {}

        # GENERAL CONFIG
        params_general = {
            "general": {
                "min_update_delay": {
                    "optional": True,
                    "default": 60,
                    "type": int,
                    "description": "Short delay between tasks (collect, enrich ...)"
                },
                "update": {
                    "optional": False,
                    "default": False,
                    "type": bool,
                    "description": "Execute the tasks in loop"
                },
                "short_name": {
                    "optional": False,
                    "default": "Short name",
                    "type": str,
                    "description": "Short name of the project"
                },
                "debug": {
                    "optional": False,
                    "default": True,
                    "type": bool,
                    "description": "Debug mode (logging mainly)"
                },
                "logs_dir": {
                    "optional": False,
                    "default": "logs",
                    "type": str,
                    "description": "Directory with the logs of sirmordred"
                },
                "log_handler": {
                    "optional": True,
                    "default": "file",
                    "type": str,
                    "description": "use rotate for rotating the logs automatically"
                },
                "log_max_bytes": {
                    "optional": True,
                    "default": 104857600,  # 100MB
                    "type": int,
                    "description": "Max number of bytes per log file"
                },
                "log_backup_count": {
                    "optional": True,
                    "default": 5,
                    "type": int,
                    "description": "Number of rotate logs files to preserve"
                },
                "bulk_size": {
                    "optional": True,
                    "default": 1000,
                    "type": int,
                    "description": "Number of items to write in Elasticsearch using bulk operations"
                },
                "scroll_size": {
                    "optional": True,
                    "default": 100,
                    "type": int,
                    "description": "Number of items to read from Elasticsearch when scrolling"
                },
                "aliases_file": {
                    "optional": True,
                    "default": ALIASES_JSON,
                    "type": str,
                    "description": "JSON file to define aliases for raw and enriched indexes"
                },
                "menu_file": {
                    "optional": True,
                    "default": MENU_YAML,
                    "type": str,
                    "description": "YAML file to define the menus to be shown in Kibiter"
                },
                "retention_time": {
                    "optional": True,
                    "default": None,
                    "type": int,
                    "description": "The maximum number of minutes wrt the current date to retain the data"
                }
            }
        }
        params_projects = {
            "projects": {
                "projects_file": {
                    "optional": True,
                    "default": PROJECTS_JSON,
                    "type": str,
                    "description": "Projects file path with repositories to be collected group by projects"
                },
                "projects_url": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "Projects file URL"
                },
                "load_eclipse": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Load the projects from Eclipse"
                }
            }
        }

        params_phases = {
            "phases": {
                "collection": {
                    "optional": False,
                    "default": True,
                    "type": bool,
                    "description": "Activate collection of items"
                },
                "enrichment": {
                    "optional": False,
                    "default": True,
                    "type": bool,
                    "description": "Activate enrichment of items"
                },
                "identities": {
                    "optional": False,
                    "default": True,
                    "type": bool,
                    "description": "Do the identities tasks"
                },
                "panels": {
                    "optional": False,
                    "default": True,
                    "type": bool,
                    "description": "Load panels, create alias and other tasks related"
                },
                "track_items": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Track specific items from a gerrit repository"
                },
                "report": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Generate the PDF report for a project (alpha)"
                }
            }
        }

        general_config_params = [params_general, params_projects, params_phases]

        for section_params in general_config_params:
            params.update(section_params)

        # Config provided by tasks
        params_collection = {
            "es_collection": {
                "password": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "Password for connection to Elasticsearch"
                },
                "user": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "User for connection to Elasticsearch"
                },
                "url": {
                    "optional": False,
                    "default": "http://172.17.0.1:9200",
                    "type": str,
                    "description": "Elasticsearch URL"
                },
                "arthur": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Use arthur for collecting items from perceval"
                },
                "arthur_url": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "URL for the arthur service"
                },
                "redis_url": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "URL for the redis service"
                }
            }
        }

        params_enrichment = {
            "es_enrichment": {
                "url": {
                    "optional": False,
                    "default": "http://172.17.0.1:9200",
                    "type": str,
                    "description": "Elasticsearch URL"
                },
                "autorefresh": {
                    "optional": True,
                    "default": True,
                    "type": bool,
                    "description": "Execute the autorefresh of identities"
                },
                "autorefresh_interval": {
                    "optional": True,
                    "default": 2,
                    "type": int,
                    "description": "Set time interval (days) for autorefresh identities"
                },
                "user": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "User for connection to Elasticsearch"
                },
                "password": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "Password for connection to Elasticsearch"
                }
            }
        }

        params_panels = {
            "panels": {
                "strict": {
                    "optional": True,
                    "default": True,
                    "type": bool,
                    "description": "Enable strict panels loading"
                },
                "kibiter_time_from": {
                    "optional": True,
                    "default": "now-90d",
                    "type": str,
                    "description": "Default time interval for Kibiter"
                },
                "kibiter_default_index": {
                    "optional": True,
                    "default": "git",
                    "type": str,
                    "description": "Default index pattern for Kibiter"
                },
                "kibiter_url": {
                    "optional": False,
                    "default": None,
                    "type": str,
                    "description": "Kibiter URL"
                },
                "kibiter_version": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "Kibiter version"
                },
                "community": {
                    "optional": True,
                    "default": True,
                    "type": bool,
                    "description": "Enable community structure menu"
                },
                "kafka": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Enable kafka menu"
                },
                "github-repos": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Enable GitHub repo stats menu"
                },
                "gitlab-issues": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Enable GitLab issues menu"
                },
                "gitlab-merges": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Enable GitLab merge requests menu"
                },
                "mattermost": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Enable Mattermost menu"
                }
            }
        }

        params_report = {
            "report": {
                "start_date": {
                    "optional": False,
                    "default": "1970-01-01",
                    "type": str,
                    "description": "Start date for the report"
                },
                "end_date": {
                    "optional": False,
                    "default": "2100-01-01",
                    "type": str,
                    "description": "End date for the report"
                },
                "interval": {
                    "optional": False,
                    "default": "quarter",
                    "type": str,
                    "description": "Interval for the report"
                },
                "config_file": {
                    "optional": False,
                    "default": "report.cfg",
                    "type": str,
                    "description": "Config file for the report"
                },
                "data_dir": {
                    "optional": False,
                    "default": "report_data",
                    "type": str,
                    "description": "Directory in which to store the report data"
                },
                "filters": {
                    "optional": True,
                    "default": [],
                    "type": list,
                    "description": "General filters to be applied to all queries"
                },
                "offset": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "Date offset to be applied to start and end"
                }
            }
        }

        params_sortinghat = {
            "sortinghat": {
                "affiliate": {
                    "optional": False,
                    "default": "True",
                    "type": bool,
                    "description": "Affiliate identities to organizations"
                },
                "unaffiliated_group": {
                    "optional": False,
                    "default": "Unknown",
                    "type": str,
                    "description": "Name of the organization for unaffiliated identities"
                },
                "matching": {
                    "optional": False,
                    "default": ["email"],
                    "type": list,
                    "description": "Algorithm for matching identities in Sortinghat"
                },
                "sleep_for": {
                    "optional": False,
                    "default": 3600,
                    "type": int,
                    "description": "Delay between task identities executions"
                },
                "database": {
                    "optional": False,
                    "default": "sortinghat_db",
                    "type": str,
                    "description": "Name of the Sortinghat database"
                },
                "host": {
                    "optional": False,
                    "default": "mariadb",
                    "type": str,
                    "description": "Host with the Sortinghat database"
                },
                "user": {
                    "optional": False,
                    "default": "root",
                    "type": str,
                    "description": "User to access the Sortinghat database"
                },
                "password": {
                    "optional": False,
                    "default": "",
                    "type": str,
                    "description": "Password to access the Sortinghat database"
                },
                "autoprofile": {
                    "optional": False,
                    "default": ["customer", "git", "github"],
                    "type": list,
                    "description": "Order in which to get the identities information for filling the profile"
                },
                "load_orgs": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "deprecated": "Load organizations in Sortinghat database",
                    "description": ""
                },
                "identities_format": {
                    "optional": True,
                    "default": "sortinghat",
                    "type": str,
                    "description": "Format of the identities data to be loaded"
                },
                "strict_mapping": {
                    "optional": True,
                    "default": True,
                    "type": bool,
                    "description": "rigorous check of values in identities matching "
                                   "(i.e, well formed email addresses)"
                },
                "reset_on_load": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Unmerge and remove affiliations for all identities on load"
                },
                "orgs_file": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "File path with the organizations to be loaded in Sortinghat"
                },
                "identities_file": {
                    "optional": True,
                    "default": [],
                    "type": list,
                    "description": "File path with the identities to be loaded in Sortinghat"
                },
                "identities_export_url": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "URL in which to export the identities in Sortinghat"
                },
                "identities_api_token": {
                    "optional": True,
                    "default": None,
                    "type": str,
                    "description": "API token for remote operation with GitHub and Gitlab"
                },
                "bots_names": {
                    "optional": True,
                    "default": [],
                    "type": list,
                    "description": "Name of the identities to be marked as bots"
                },
                "no_bots_names": {
                    "optional": True,
                    "default": [],
                    "type": list,
                    "description": "Name of the identities to be unmarked as bots"
                },
                "autogender": {
                    "optional": True,
                    "default": False,
                    "type": bool,
                    "description": "Add gender to the profiles (executes autogender)"
                }
            }
        }

        params_track_items = {
            "track_items": {
                "project": {
                    "optional": False,
                    "default": "TrackProject",
                    "type": str,
                    "description": "Gerrit project to track"
                },
                "upstream_raw_es_url": {
                    "optional": False,
                    "default": "",
                    "type": str,
                    "description": "URL with the file with the gerrit reviews to track"
                },
                "raw_index_gerrit": {
                    "optional": False,
                    "default": "",
                    "type": str,
                    "description": "Name of the gerrit raw index"
                },
                "raw_index_git": {
                    "optional": False,
                    "default": "",
                    "type": str,
                    "description": "Name of the git raw index"
                }
            }
        }

        tasks_config_params = [params_collection, params_enrichment, params_panels,
                               params_report, params_sortinghat, params_track_items]

        for section_params in tasks_config_params:
            params.update(section_params)

        return params