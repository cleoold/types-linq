class TypesLinqError(Exception):
    '''
    .. code-block:: python

        from types_linq import TypesLinqError

    Types-linq has run into problems.
    '''


class InvalidOperationError(TypesLinqError, ValueError):
    '''
    .. code-block:: python

        from types_linq import InvalidOperationError

    Exception raised when a call is invalid for the object's current state.
    '''


class IndexOutOfRangeError(TypesLinqError, IndexError):
    '''
    .. code-block:: python

        from types_linq import IndexOutOfRangeError

    An `IndexError` with types-linq flavour.
    '''
