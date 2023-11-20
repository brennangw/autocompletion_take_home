
from dataclasses import dataclass

@dataclass(frozen=True)
class Term:
    value: str

class TermIndex:

    all_terms: list[Term] = [
        Term(value="apple"),
        Term(value="microsoft"),
        Term(value="tesla"),
        Term(value="average"),
        Term(value="median"),
        Term(value="minimum"),
        Term(value="maximum"),
        Term(value="by revenue"),
        Term(value="by price"),
        Term(value="by ebitda"),
        Term(value="by ebit"),
        Term(value="by month"),
        Term(value="revenue"),
        Term(value="ebit"),
        Term(value="ebitda"),
        Term(value="february"),
        Term(value="march"),
        Term(value="april"),
        Term(value="2022"),
        Term(value="2023"),
        Term(value="last 5 months"),
        Term(value="last 12 months")
    ]

    def search(self, string: str) -> list[Term]:
        if len(string) == 0:
            return []
        return [s for s in TermIndex.all_terms if s.value.startswith(string)]

