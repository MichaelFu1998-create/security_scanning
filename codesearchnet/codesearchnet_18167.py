def publish(context):
    """Saves changes and sends them to GitHub"""

    header('Recording changes...')
    run('git add -A')

    header('Displaying changes...')
    run('git -c color.status=always status')

    if not click.confirm('\nContinue publishing'):
        run('git reset HEAD --')
        abort(context)

    header('Saving changes...')
    try:
        run('git commit -m "{message}"'.format(
            message='Publishing {}'.format(choose_commit_emoji())
        ), capture=True)
    except subprocess.CalledProcessError as e:
        if 'nothing to commit' not in e.stdout:
            raise
        else:
            click.echo('Nothing to commit.')

    header('Pushing to GitHub...')
    branch = get_branch()
    run('git push origin {branch}:{branch}'.format(branch=branch))

    pr_link = get_pr_link(branch)
    if pr_link:
        click.launch(pr_link)