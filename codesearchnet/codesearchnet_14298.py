def parse_json_path(path):
    """
    Parse a string as a JSON path
    An implementation of "steps to parse a JSON encoding path"
    http://www.w3.org/TR/html-json-forms/#dfn-steps-to-parse-a-json-encoding-path
    """

    # Steps 1, 2, 3
    original_path = path
    steps = []

    # Step 11 (Failure)
    failed = [
        JsonStep(
            type="object",
            key=original_path,
            last=True,
            failed=True,
        )
    ]

    # Other variables for later use
    digit_re = re.compile(r'^\[([0-9]+)\]')
    key_re = re.compile(r'^\[([^\]]+)\]')

    # Step 4 - Find characters before first [ (if any)
    parts = path.split("[")
    first_key = parts[0]
    if parts[1:]:
        path = "[" + "[".join(parts[1:])
    else:
        path = ""

    # Step 5 - According to spec, keys cannot start with [
    # NOTE: This was allowed in older DRF versions, so disabling rule for now
    # if not first_key:
    #     return failed

    # Step 6 - Save initial step
    steps.append(JsonStep(
        type="object",
        key=first_key,
    ))

    # Step 7 - Simple single-step case (no [ found)
    if not path:
        steps[-1].last = True
        return steps

    # Step 8 - Loop
    while path:
        # Step 8.1 - Check for single-item array
        if path[:2] == "[]":
            path = path[2:]
            steps.append(JsonStep(
                type="array",
                key=0,
            ))
            continue

        # Step 8.2 - Check for array[index]
        digit_match = digit_re.match(path)
        if digit_match:
            path = digit_re.sub("", path)
            steps.append(JsonStep(
                type="array",
                key=int(digit_match.group(1)),
            ))
            continue

        # Step 8.3 - Check for object[key]
        key_match = key_re.match(path)
        if key_match:
            path = key_re.sub("", path)
            steps.append(JsonStep(
                type="object",
                key=key_match.group(1),
            ))
            continue

        # Step 8.4 - Invalid key format
        return failed

    # Step 9
    next_step = None
    for step in reversed(steps):
        if next_step:
            step.next_type = next_step.type
        else:
            step.last = True
        next_step = step

    return steps