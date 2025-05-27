#!/usr/bin/env python3

import sys

# TODO: When a list is returned it should be encapsulated in a dict_dot.List.
#       This to make the use of a.b.c[2].d.e
#       How to do with tuple and set?!
# TODO: Explain the implications of encapsulating a dict containing Map
#       object(s).
# TODO: Explain how bool works. E.g always return False for non-existant keys,
#       but depends no existing keys.
#       Empty dicts, lists, sets, stringts, zero values etc. for which bool
#       returns False.
# TODO: Explain classmethod exists. Used to check existance of a key/hierarchy.
# TODO: 'in' can be used instead of 'exists', e.g. 'ok' in e.reply


# Map is a dictionary object that doesn't thows exceptions for non-existing
# names. Reduces the number of conditionals when an empty string is expected
# for non-existing values.
#
# It also reduces the number of lines to set a hierarchy of values compared
# to ordinary dictionaries, which makes it suitable for handling configuation
# without a lot of syntactical noice.
#
# An example:
#  > a = Map()       # Creates an empty Map
#  > str(a)
#  '{}'              # a is an "existing" Map()
#
#  > a.b             # Acessing a non-existing attribute
#  Map <non-existing>
#  > str(a.b)        # "non-existing" attributes a str-ed to empty strings
#  ''
#  > bool(a.b)       # "non-existing" attributes are bool-ed to False
#  False
#
#  > int(a.b)        # "non-existing" attributes are int-ed to 0
#  0                 # This differs from other types but makes it easier when
#                    # handling config
#
#  > a.b.c.d.e = 1   # You can set a hierarchy in one go
#  > str(a)
#  "{'b': Map {'c': Map {'d': Map {'e': 1}}}}"
#
#  > a.i.h.w.d.f.g   # You can access a "non-existing" hierarchy in one go
#  Map <non-existing>
#
#  > d_dict = { 'e': 2 }
#  > d_dict
#  {'e': 2}
#  > a = Map({'b': { 'c': { 'd': d_dict }}}) # You can provide a hierarhcy of
#                                              ordinary dicts when initializing
#                                              a Map
#  > a                                  # The ordinary dict(s) are preserved
#  Map {'b': {'c': {'d': {'e': 2}}}}    # When accessed and modified by Map
#
#  > a.b.c.d.e = 42
#  > a
#  Map {'b': {'c': {'d': {'e': 42}}}}
#
#  > d_dict
#  {'e': 42}
#
#  > a.b.c.d                   # This is the "same" as d_dict, but when accessed
#  Map {'e': 42}               # using dot notiation is encapsulated in a Map
#                              # object, which is not the same object.
#  > a.b.c.d == d_dict
#  False
#
#  a.b.c.d.data == d_dict      # The data member is the same object
#  True

# 
# bkptr is a helper argument and used to be able to set a value in a
# 'non-existant' hierarchy.

class Map:
    def __init__(self, data=None, bkptr=None):
        if bkptr is not None:
            self.__dict__['__bkptr__'] = bkptr
        if isinstance(data, dict):
            self.__dict__['data'] = data
        elif data is None:
            self.__dict__['data'] = {}
        else:
            raise TypeError("Argument is not a dictionary")
    def __contains__(self, name):
        return name in self.data
    def __getitem__(self, name):
        return self.data[name]
    def __setitem__(self, name, value):
        self.__setattr__(name, value)
    def __getattr__(self, attr):
        # Remove unwanted IPython stuff
        if attr in ['_ipython_canary_method_should_not_exist_', '_repr_mimebundle_']:
            return None
        a = self.data.get(attr)
        if a == None:
            return Map(bkptr=(attr, self))
        if isinstance(a, dict):
            return Map(a)
        return a
    def __setattr__(self, name, value):
        self.data[name] = value
        if '__bkptr__' in self.__dict__:
            self.__bkptr__[1].__setattr__(self.__bkptr__[0], self)
            del self.__dict__['__bkptr__']
    def __delattr__(self, name):
        if name in self.data:
            del self.data[name]
    def __repr__(self):
        if '__bkptr__' in self.__dict__:
            return "Map <non-existing>"
        return "Map {}".format(repr(self.data))
    def __str__(self):
        if '__bkptr__' in self.__dict__:
            return ""
        return str(self.data)
    def items(self):
        return self.data.items()
    def keys(self):
        return self.data.keys()
    def __int__(self):
        return len(self.data)
    def __bool__(self):
        return bool(self.data)
    def clear(self):
        self.__dict__['data'] = {}
    def update(self, other):
        if isinstance(other, Map):
            other = other.data
        self.data.update(other)
    def merge(self, other):
        for k in other.keys():
            o = other[k]
            if k in self.data:
                t = self.data[k]
                if type(self.data[k]) != type(o):
                    raise TypeError("Different data types {} != {}".format(type(t), type(o)))
                if type(o) in [list, tuple]:
                    t += o
                elif type(o) == set:
                    t.union(o)
                elif type(o) in [dict]:
                    t.update(o)
                elif type(o) in [Map]:
                    t.merge(o)
                else:
                    t=o
            else:
                t=o
            self.data[k] = t
    def as_dict(self):
        return to_generic(self.data)

        print("as_dict", d)
        return d

# Iterate structure and convert Map -> dict
# Lists and dicts are copied
# All other objects are referensed
# TODO: Both lists and dicts is kept as is, as they are preserved.
def to_generic(e):
    if isinstance(e, Map):
        return e.as_dict()
    elif isinstance(e, list):
        return [to_generic(le) for le in e]
    elif isinstance(e, set):
        return {to_generic(se) for se in e}
    elif isinstance(e, dict):
        if bool(e):
            return {k: to_generic(v) for k,v in e.items()}
        return ""
    return e


# TODO: Use assert to validate function...
def main():
    d = Map({
        'desc': "This is just a test",
        'kalle': {
            'touched': True,
            'value': 1
        },
        'olle': {
            'touched': False,
            'value': 4
        }
    })


    print("d.desc", d.desc)                    # "This is just a test"
    print("d.kalle", d.kalle)                  # { 'touched': True, 'value': 1 }
    print("d.kalle.touched", d.kalle.touched)  # True
    print("repr d.ulrik", repr(d.ulrik))       # Undefined
    print("d.ulrik: '{}'".format(d.ulrik))     # Undefined
    print("d.ulrik.stridsman: '{}'".format(d.ulrik.stridsman))  # Undefined

    d.ulrik = { 'value': 12 }
    u = d.ulrik
    u.gurka = 13
    u.l = [1,2,3]
    print("d.ulrik: '{}'".format(d.ulrik))
    print("d.ulrik.l: '{}'".format(d.ulrik.l))
    print("d.ulrik.l[0]: '{}'".format(d.ulrik.l[0]))
    print("d.ulrik.value: '{}'".format(d.ulrik.value))

    d.v = 1
    d.v = 2

    print(d)

    print("="*40)
    for (k,v) in d.items():
        print(k, v)

    print("="*40)
    print("Merge tests")
    print()

    a = Map()
    b = Map()
    a.q = 1
    a.w = 2
    b.x = 10
    b.y = 11
    a.merge(b)
    print(a)

    a = Map()
    b = Map()
    a.r = 1
    a.s = 2
    a.w = 2
    a.x.c = 2
    a.x.d = 20
    b.x.a = 10
    b.x.b = 12
    b.x.d = 21
    b.y = 11
    a.merge(b)
    print(a)

    a = Map()
    b = Map()
    a.r = 1
    a.s = 2
    a.w = 2
    a.x = dict(a=1, b=2)
    b.x = dict(c=3, d=3)
    b.y = 11
    a.merge(b)
    print(a)

if __name__ == '__main__':
    main()
