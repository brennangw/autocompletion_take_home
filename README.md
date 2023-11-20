# Autocompletion Take Home

## About
Implementaion of autocompletion functionality for a take home interview.

## Abbrviated Instructions

We've provided you with a term index that takes in a string prefix and returns a list of matching terms. For example, if you query the term index with "m", you'll get the following terms back in response: [median], [maximum], [minimum], [microsoft inc]. You can think of the term index as an in-memory implementation of an Elasticsearch index. You can look at this class in `engine/term_index.py` to see what it does, but you can't make any modifications to it.

Your task is to implement a Python algorithm that inputs a string and returns matching queries. A input string might match 0, 1, or many queries. Each query contains 1 or more terms. The order the queries are returned in doesn't matter.

The scaffolding code has been provided in `engine/autocompleter.py`. Your goal is to make the unit tests pass (`tests/test_autocomplete.py`) by completing this class's implementation. You're not allowed to use any external libraries, and you must come up with the solution by yourself (no LLMs!). Produce Python 3 code that is as clean and idiomatic as you find appropriate, and leverage Python typing where it's useful.

## Given Tip

__Tip: Terms in this exercise will never exceed 3 words, so you can build that assumption into your algorithm.__

## Given Examples

```
Input: "app"
Output: 
  - [apple]

Input: "apple revenue by month"
Output: 
  - [apple] [revenue] [by month]

Input: "apple revenue by month last 12 "
Output:     
  - [apple] [revenue] [by month] [last 12 months]
  - [apple] [revenue] [by month] [last 12 years]
```

(You can find more examples in the unit test file)