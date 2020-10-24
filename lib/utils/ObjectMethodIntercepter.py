from copy import copy

class ObjectMethodIntercepter:
    def __init__(self, obj_to_intercept, new_obj):
        self.obj_to_intercept = obj_to_intercept
        self.new_obj = new_obj

    # def __repr__(self):
    #     return self.obj_to_intercept.__repr__()

    # def __format__(self):
    #     return self.obj_to_intercept.__format__()

    # def __str__(self):
    #     return self.obj_to_intercept.__str__()
    
    @staticmethod
    def get_attr_for_obj_to_intercept_if_needed(obj):
        if isinstance(obj, ObjectMethodIntercepter):
            return object.__getattribute__(obj, 'obj_to_intercept')
        else:
            return obj

    @staticmethod
    def get_attr_for_new_obj_if_needed(obj):
        if isinstance(obj, ObjectMethodIntercepter):
            return object.__getattribute__(obj, 'new_obj')
        else:
            return obj

    def __getattribute__(self, name):
        if name in ['obj_to_intercept', 'new_obj']:
            return object.__getattribute__(self, name)
            
        obj_to_intercept_attr =  object.__getattribute__(self.obj_to_intercept, name)
        new_obj_attr =  object.__getattribute__(self.new_obj, name)
        if hasattr(obj_to_intercept_attr, '__call__'):
            def _(*args, **kwargs):
                def __dictionary_map_values(d, func):
                    return {k: func(v) for k, v in d.items()}
                
                args_obj_to_intercept = tuple(map(ObjectMethodIntercepter.get_attr_for_obj_to_intercept_if_needed, args))
                args_obj_new = tuple(map(ObjectMethodIntercepter.get_attr_for_new_obj_if_needed, args))
                
                kwargs_obj_to_intercept = __dictionary_map_values(kwargs, ObjectMethodIntercepter.get_attr_for_obj_to_intercept_if_needed)
                kwargs_obj_new = __dictionary_map_values(kwargs, ObjectMethodIntercepter.get_attr_for_new_obj_if_needed)
                
                a = obj_to_intercept_attr(*args_obj_to_intercept, **kwargs_obj_to_intercept)
                b = new_obj_attr(*args_obj_new, **kwargs_obj_new)
                return ObjectMethodIntercepter(a, b)
            return _
        else:           
            return ObjectMethodIntercepter(obj_to_intercept_attr, new_obj_attr)
    
    def __getitem__(self, key):
        a = self.obj_to_intercept[ObjectMethodIntercepter.get_attr_for_obj_to_intercept_if_needed(key)]
        b = self.new_obj[ObjectMethodIntercepter.get_attr_for_new_obj_if_needed(key)]
        return ObjectMethodIntercepter(a, b)
    
    def __setitem__(self, key, newvalue):
        self.obj_to_intercept[key] = ObjectMethodIntercepter.get_attr_for_obj_to_intercept_if_needed(newvalue)
        self.new_obj[key] = ObjectMethodIntercepter.get_attr_for_new_obj_if_needed(newvalue)
        return ObjectMethodIntercepter(self.obj_to_intercept, self.new_obj)

    def __getattr__(self, attribute_name):
        a = self.obj_to_intercept[attribute_name]
        b = self.new_obj[attribute_name]
        return ObjectMethodIntercepter(a, b)
    
    def __copy__(self):
        return ObjectMethodIntercepter(copy(self.obj_to_intercept), copy(self.new_obj))
    
    def __add__(self, r):
        a = self.obj_to_intercept + ObjectMethodIntercepter.get_attr_for_obj_to_intercept_if_needed(r)
        b = self.new_obj + ObjectMethodIntercepter.get_attr_for_new_obj_if_needed(r)
        return ObjectMethodIntercepter(a, b)
