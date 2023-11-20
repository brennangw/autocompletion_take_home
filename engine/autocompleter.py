
from .term_index import TermIndex, Term

class Autocompleter:

    def __init__(self, term_index: TermIndex) -> None:
        self.term_index = term_index 

    def suggestions(self, input: str) -> list[list[Term]]:
        # TODO Implement me
        pass 
