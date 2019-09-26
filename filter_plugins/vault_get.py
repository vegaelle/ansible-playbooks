def get_volume(value, ctid):
    for item in value:
        if int(ctid) in map(lambda i: i['ctid'], item['containers']):
            return item


def get_zvolumes(value):
    volumes = []
    for item in value.values():
        for ct in item['containers']:
            for vol in ct['volumes']:
                volumes.append(vol)
    return volumes


def get_containers(value):
    volumes = []
    for item in value.values():
        for ct in item['containers']:
            volumes.append(ct)
    return volumes


class FilterModule:

    def filters(self):
        return {
            'get_volume': get_volume,
            'get_zvolumes': get_zvolumes,
            'get_containers': get_containers,
        }
