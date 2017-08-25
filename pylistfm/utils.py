import glob


class Utils:
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c

    def insensitive_glob(pattern):
        return glob.glob(pattern, recursive=True)

