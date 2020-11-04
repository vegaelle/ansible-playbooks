def hex_int(value):
    return '{:0>2}'.format(hex(int(value))[2:])


class FilterModule:

    def filters(self):
        return {
            'hex': hex_int,
        }

