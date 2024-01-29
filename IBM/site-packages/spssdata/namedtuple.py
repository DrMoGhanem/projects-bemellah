"""factory for making tuples that can be accessed by item name as well as index number.  Used by spssdata module"""
#factory for named tuples

#Licensed Materials - Property of IBM
#IBM SPSS Products: Statistics General
#(c) Copyright IBM Corp. 2005, 2011
#US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
__author__ =  'spss'
__version__=  '1.0.1'


# history
# 07-Oct-2005 Initial version
# 01-Nov-2006 Enhanced for multi-pass cursors


from operator import itemgetter

def _flatten(args):
    "convert to form apropriate for * arguments"
    if not isinstance(args[0], basestring):
        try:
            iter(args[0])       # if a single tuple or list etc was passed, convert to args form
            if len(args) > 1:
                raise TypeError, "too many items in attr names"
            args=tuple(args[0])
        except:
            pass
    return args

    
def MakeNamedTuple(typename, *attrnames):
    """ return an object that is a subclass of tuple where tuple positions have (unique) names
    as listed in attrnames.
    Example: MakeNamedTuple('mytuple', 'x', 'y') or MakeNamedTuple('mytuple', ('x', 'y'))
    allows this:
    t = mytuple(1,2)
    print t.x, t.y
    attrnames may be passed as a single object of type sequence or as positional arguments."""
    # based on recipe 6.7 in Python Cookbook, 2nd ed, which says (p xix)
    #"In general, you may use the code in this book in your programs and documentation
    #You do not need to contact us for permission unless you're reproducing a significant
    #proportion of the code.  For example, writing a program that uses several chunks of code
    #from this book does not require permission."
    
    attrnames = _flatten(attrnames)
    nargs = len(attrnames)

    if nargs != len(set(attrnames)):
        raise TypeError, "duplicate attribute names"
    class namedTuple(tuple):
        __slots__ = ()  # This class variable can be assigned a string, iterable,
                        # or sequence of strings with variable names used by instances.
                        # If defined in a new-style class, __slots__ reserves space for the
                        # declared variables and prevents the automatic creation of
                        # __dict__ and __weakref__ for each instance.
        def __new__(cls, *args):    # Called to create a new instance of class cls.
                                    # __new__() is a static method (special-cased so you need not
                                    # declare it as such) that takes the class of which an instance
                                    # was requested as its first argument.
            args = _flatten(args)
            args = args[:nargs]   #multi-pass cursors may have added variables that should not be included in subsequent retrievals
            if len(args) != nargs:
                raise TypeError, "wrong number of args. Expected:%d, Actual:%d" % (nargs, len(args))
            return tuple.__new__(cls, args)
        def __repr__(self):
            return '%s(%s)' % (typename, ', '.join(map(repr, self)))
        
    for i, attrname in enumerate(attrnames):
        setattr(namedTuple, attrname, property(itemgetter(i)))
    namedTuple.__name__ = typename
    return namedTuple

