def get(dict, key):
    try:
        return dict[key]
    except KeyError:
        return dict[int(key)]


class FilterModule:

    def filters(self):
        return {
            'get': get,
        }
