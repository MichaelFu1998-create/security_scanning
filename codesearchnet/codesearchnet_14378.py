def _apply_template(template, target, *, checkout, extra_context):
    """Apply a template to a temporary directory and then copy results to target."""
    with tempfile.TemporaryDirectory() as tempdir:
        repo_dir = cc_main.cookiecutter(
            template,
            checkout=checkout,
            no_input=True,
            output_dir=tempdir,
            extra_context=extra_context)
        for item in os.listdir(repo_dir):
            src = os.path.join(repo_dir, item)
            dst = os.path.join(target, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.copy2(src, dst)