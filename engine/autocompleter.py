"""Contains the titular Autocompleter class, which provides autocompletion suggestions."""
from __future__ import annotations
from functools import lru_cache
from re import split as regex_split

from .term_index import TermIndex, Term


class _SuggestionTree:
    """Represents Term suggestions based on a 'word list' and a TermIndex."""

    term: Term
    start_index: int
    end_index: int
    children: list[_SuggestionTree]

    @classmethod
    def root(cls, word_list: list[str], term_index: TermIndex) -> _SuggestionTree:
        """Create the root of a _SuggestionTree and recursively the rest of the tree."""
        return cls(None, 0, 0, word_list, term_index)

    def __init__(
        self,
        term: Term,
        start_index: int,
        end_index: int,
        word_list: [str],
        term_index: TermIndex,
    ) -> _SuggestionTree:
        self.term, self.start_index, self.end_index, self.children = (
            term,
            start_index,
            end_index,
            [],
        )
        # Skip the iteration if out of words to suggest for
        if self.end_index >= len(word_list):
            return
        results = term_index.search(word_list[self.end_index])
        for child_term, child_term_word_count in [
            (result, len(result.value.split(" "))) for result in results
        ]:
            child_start_index = self.end_index
            child_end_index = child_start_index + child_term_word_count
            # If input is not a prefix of the suggestion then skip it
            if not child_term.value.startswith(
                " ".join(word_list[child_start_index:child_end_index])
            ):
                continue
            self.children.append(
                _SuggestionTree(
                    child_term,
                    end_index,
                    end_index + child_term_word_count,
                    word_list,
                    term_index,
                )
            )

    def paths(self) -> list[list[_SuggestionTree]]:
        """List out ancestry paths of the SuggestionTree."""
        # Recursive base case is self being a leaf node
        if not self.children:
            return [[self]]
        # Get paths from the parent to their descendants
        return [
            [self] + child_path
            for child in self.children
            for child_path in child.paths()
        ]


class Autocompleter:
    """Used to generate multiple Term lists to serve as suggestions for autocompletion."""

    # class variables
    suggestion_paths_cache_size = 128

    term_index: TermIndex
    words_split_regex: str

    def __init__(
        self, term_index: TermIndex, words_split_regex=r"\W+"
    ) -> Autocompleter:
        self.term_index = term_index
        self.words_split_regex = words_split_regex

    @lru_cache(maxsize=suggestion_paths_cache_size)
    def _suggestion_paths(self, input_text: str) -> list[list[_SuggestionTree]]:
        """Splits the input text up and returns _SuggestionTree lists
        for autocompletion using the instance's term_index"""
        # Split the input up into "words"
        input_words = regex_split(self.words_split_regex, input_text)
        # Generate term suggestions whose relationships are represented by a tree structure
        root = _SuggestionTree.root(input_words, self.term_index)
        # Get ancestry paths starting at the root's children as the root does not wrap a term
        paths = [path for root_child in root.children for path in root_child.paths()]
        # Filter out paths that do not include a suggestion for each word in the input
        return [path for path in paths if path[-1].end_index >= len(input_words)]

    def suggestions(self, input_text: str) -> list[list[Term]]:
        """Calls _suggestions_paths and rebuilds the results with the suggestions' Terms"""
        suggestion_paths = self._suggestion_paths(input_text)
        # The below stops the return of mutable lists
        # while extracting the terms from the suggestion paths
        return [[node.term for node in path] for path in suggestion_paths]
