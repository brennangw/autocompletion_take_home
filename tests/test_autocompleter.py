import pytest

from engine.term_index import TermIndex, Term
from engine.autocompleter import Autocompleter

@pytest.fixture
def term_index():
    return TermIndex()


@pytest.mark.parametrize(
    "string,suggestions",
    [
        ("", []),
        ("doesntexist", []),
        ("apple doesntexist", []),
        ("doesntexist apple", []),
        ("a", [["apple"],["average"],["april"]]),
        ("appl", [["apple"]]),
        ("apple revenue eb", [["apple", "revenue", "ebit"], ["apple", "revenue", "ebitda"]]),
        ("apple revenue ebitd", [["apple", "revenue", "ebitda"]]),
        ("apple last", [["apple", "last 5 months"], ["apple", "last 12 months"]]),
        ("apple last 1", [["apple", "last 12 months"]]),
        ("apple last 12 months", [["apple", "last 12 months"]]),
        ("average revenue by month 202", [
            ["average", "revenue", "by month", "2022"], 
            ["average", "revenue", "by month", "2023"]
        ]),
        ("m revenue by month 2023", [
            ["maximum", "revenue", "by month", "2023"], 
            ["minimum", "revenue", "by month", "2023"], 
            ["median", "revenue", "by month", "2023"],
            ["microsoft", "revenue", "by month", "2023"],
            ["march", "revenue", "by month", "2023"],
        ]),
        ("maximum ebit by month 2023", [
            ["maximum", "ebit", "by month", "2023"],
            ["maximum", "ebitda", "by month", "2023"]
        ]),
        ("mi ebit by month 2023", [
            ["minimum", "ebit", "by month", "2023"],
            ["minimum", "ebitda", "by month", "2023"],
            ["microsoft", "ebit", "by month", "2023"],
            ["microsoft", "ebitda", "by month", "2023"]
        ]),
    ],
)
def test_answer(term_index: TermIndex, string: str, suggestions: list[list[str]]):
    autocompleter = Autocompleter(term_index=term_index)

    response = autocompleter.suggestions(string)

    assert { tuple(x) for x in response } == { tuple([Term(value=s) for s in xs]) for xs in suggestions}
