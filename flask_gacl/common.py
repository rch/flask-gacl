import six, json

class Entry(object):
    
    def __init__(self, entry):
        properties = {'tags','pending'}
        for key in entry.keys():
            if key in properties:
                # custom assignment handled in setters
                if key == 'tags':
                    self.tags = entry[key]
                elif key == 'pending':
                    self.pending = entry[key]
                else:
                    raise ValueError(key)
            else:
                # non-property
                self.__setattr__(key, entry[key])
    
    @property
    def tags(self):
        return self._tags
    
    @tags.setter
    def tags(self, value):
        if isinstance(value, six.string_types):
            self.__setattr__('_tags', set(json.loads(value)))
        else:
            self.__setattr__('_tags', value)
    
    @property
    def pending(self):
        return self._pending
    
    @pending.setter
    def pending(self, value):
        if isinstance(value, six.string_types):
            self.__setattr__('_pending', set(json.loads(value)))
        else:
            self.__setattr__('_pending', value)



class Request(object):
    
    def __init__(self, entry):
        properties = {}
        for key in entry.keys():
            if key in properties:
                # custom assignment handled in setters
                pass
            else:
                # non-property
                self.__setattr__(key, entry[key])  
