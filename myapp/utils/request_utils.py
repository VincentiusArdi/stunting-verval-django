def get_int(request, key, required=False, default=None):
    val = request.GET.get(key)
    if val is None:
        if required:
            raise ValueError(f"Parameter '{key}' is required.")
        return default
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"Parameter '{key}' must be an integer.")

def get_bool(request, key, required=False, default=None):
    val = request.GET.get(key)
    if val is None:
        if required:
            raise ValueError(f"Parameter '{key}' is required.")
        return default
    return str(val).lower() in {"true", "1", "yes"}

def get_str(request, key, required=False, default=None):
    val = request.GET.get(key)
    if val is None or val.strip() == "":
        if required:
            raise ValueError(f"Parameter '{key}' is required.")
        return default
    return val