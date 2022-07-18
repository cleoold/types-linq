from enum import Enum, auto


class RankMethods(Enum):
    '''
    ```py
    from types_linq.more import RankMethods
    ```

    Enumeration to select different methods of assigning rankings when breaking
    [ties](https://en.wikipedia.org/wiki/Ranking#Strategies_for_assigning_rankings).

    Revisions
        ~ main: New.
    '''
    dense = auto()
    '''
    Items that compare equally receive the same ranking, and the next items get the immediately
    following ranking. *(1223)*
    '''

    competitive = auto()
    '''
    Items that compare equally receive the same highest ranking, and gaps are left out. *(1224)*
    '''

    ordinal = auto()
    '''
    Each item receives unique rankings. *(1234)*
    '''
