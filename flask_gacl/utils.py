import six, collections

class AnnoyingError(Exception): pass

def implode(arg, iterable):
    return arg.join(iterable)

def trim(arg):
    return arg.strip()

def empty(arg):
    assert isinstance(arg, collections.Iterable)
    return False if arg else True

def is_object(arg):
    return isinstance(arg, object)

def is_list(arg):
    return isinstance(arg, collections.Iterable)

def is_array(arg):
    return isinstance(arg, collections.Iterable)

def in_list(val, lst):
    return val in lst

def is_string(arg):
    return isinstance(value, six.string_types)

def unset(arg):
    del(arg)

def isset(arg):
    """ There's no good reason to support this function.
    Use the following if you must:
    try:
        isset(arg)
    except NameError:
        pass
    """
    pass

def array_search(arg, kv):
    # loathsome
    if hasattr(kv, 'iteritems'):
        iterator = kv.iteritems()
    else:
        iterator = iter(kv)
    for k,v in iterator:
        if v == arg:
            return k
    return False


class Hashed_Cache_Lite(object):
    
    def get(self, *args):
        raise NotImplementedError()
    
    def save(self, *args):
        raise NotImplementedError()
    
    def clean(self, *args):
        raise NotImplementedError()


    