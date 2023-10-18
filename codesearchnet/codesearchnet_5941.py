def get_vpc_flow_logs(vpc, **conn):
    """Gets the VPC Flow Logs for a VPC"""
    fl_result = describe_flow_logs(Filters=[{"Name": "resource-id", "Values": [vpc["id"]]}], **conn)

    fl_ids = []
    for fl in fl_result:
        fl_ids.append(fl["FlowLogId"])

    return fl_ids