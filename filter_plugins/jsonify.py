import json


def hostvars_tojson(value):
    data = {}
    for k, v in value.items():
        data[k] = v
    json_data = json.dumps(data)
    return json_data


class FilterModule:

    def filters(self):
        return {
            'hostvars_tojson': hostvars_tojson,
        }
