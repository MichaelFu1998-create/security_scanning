def records():
    """Load records."""
    import pkg_resources
    from dojson.contrib.marc21 import marc21
    from dojson.contrib.marc21.utils import create_record, split_blob
    from flask_login import login_user, logout_user
    from invenio_accounts.models import User
    from invenio_deposit.api import Deposit

    users = User.query.all()

    # pkg resources the demodata
    data_path = pkg_resources.resource_filename(
        'invenio_records', 'data/marc21/bibliographic.xml'
    )
    with open(data_path) as source:
        with current_app.test_request_context():
            indexer = RecordIndexer()
            with db.session.begin_nested():
                for index, data in enumerate(split_blob(source.read()),
                                             start=1):
                    login_user(users[index % len(users)])
                    # do translate
                    record = marc21.do(create_record(data))
                    # create record
                    indexer.index(Deposit.create(record))
                    logout_user()
            db.session.commit()