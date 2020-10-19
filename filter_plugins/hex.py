def hex_int(value):
    return hex(int(value))[2:]


class FilterModule:

    def filters(self):
        return {
            'hex': hex_int,
        }

