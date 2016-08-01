
def dict_filter(d, keys):
    return dict((k, v) for k, v in d.items() if k in keys)
