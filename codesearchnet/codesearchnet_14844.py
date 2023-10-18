def downgrade():
    """alexm: i believe this method is never called"""
    with op.batch_alter_table(t2_name) as batch_op:
        batch_op.drop_column('do_not_use')

    with op.batch_alter_table(t1_name) as batch_op:
        batch_op.drop_column('enabled')