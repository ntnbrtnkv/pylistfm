import glob


class Utils:
    @staticmethod
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c

    @staticmethod
    def insensitive_glob(pattern):
        return glob.glob(pattern, recursive=True)
