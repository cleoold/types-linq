class TypesLinqError(Exception):
    '''
    Types-linq has run into problems.
    '''


class InvalidOperationError(TypesLinqError, ValueError):
    '''
    Exception raised when a call is invalid for the object's current state.
    '''


class IndexOutOfRangeError(TypesLinqError, IndexError):
    '''
    An `IndexError` with types-linq flavour.
    '''
