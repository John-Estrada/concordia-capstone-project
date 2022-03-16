def validate_params_missing(expected_parameters, actual_parameters):
    out = {}
    missing = []
    for param in expected_parameters:
        if param not in actual_parameters:
            missing.append(param)

    if len(missing) > 0:
        out['message'] = 'parameters missing'
        out['missing_parameters'] = missing
    else:
        out['message'] = 'normal'

    return out
