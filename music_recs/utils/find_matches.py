import difflib


def find_matches(pattern: str, word_list: list[str]) -> list[str]:
    return difflib.get_close_matches(word=pattern, possibilities=word_list, n=5, cutoff=0.6)
