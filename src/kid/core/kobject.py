# :coding: utf-8

# Project Modules

# Python Modules


class KObject(object):
    """ Base object framework.
    """
    def __str__(self):
        return self.str_formatter()

    def str_formatter(self, *args, **kwargs):
        """ Returns a reable string base on object name and arguments.

        Args:
            *args:
            **kwargs:

        Returns:
            str
        """
        result = "<{}".format(self.__class__.__name__)

        if args or kwargs:
            result += ": "

        for arg in args:
            if arg == args[-1]:
                if kwargs:
                    result += "{}, ".format(arg)
                else:
                    result += "{}".format(arg)
            else:
                result += "{}, ".format(arg)

        for key in kwargs.keys():
            if key == list(kwargs)[-1]:
                result += "{}: {}".format(key, kwargs[key])
            else:
                result += "{}: {}, ".format(key, kwargs[key])

        result += ">"
        return str(result)

    def is_valid(self):
        """ Returns True if the object has valid components or is usable.

        Returns:
            bool
        """
        raise NotImplemented

    def serialize(self, *args, **kwargs):
        raise NotImplemented

    def deserialize(self, *args, **kwargs):
        raise NotImplemented

    def as_str(self):
        raise NotImplemented

    def as_float(self):
        raise NotImplemented

    def as_int(self):
        raise NotImplemented

    def as_bool(self):
        raise NotImplemented

    def as_list(self):
        raise NotImplemented

    def as_tuple(self):
        raise NotImplemented

    def as_dict(self):
        result = dict()

        for x in self.__dict__.keys():
            result[x] = getattr(self, x)
        return result

    def update(self, *args, **kwargs):
        raise NotImplemented


if __name__ == '__main__':
    obj = KObject()
    print(obj.str_formatter(1, 2, 3, sex=12, ace=5))
