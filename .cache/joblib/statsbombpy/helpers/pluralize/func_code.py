# first line: 84
@memory.cache
def pluralize(word):
    word = engine.plural(word)
    word = word.replace("*", "")
    word = word.replace("-", "_")
    word = word.replace(" ", "_")
    word = word.lower()
    return word
