from django import template


register = template.Library()


@register.filter()
def censor(value):
    bad_words = ('компания','компании')
    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

    specialsimbols=('!', ',', '.', ':', ';')

    for word in value.split():
        if word[len(word)-1] in specialsimbols:
            word = word[:len(word)-1]
        if word.lower() in bad_words:
            value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}{word[-1]}")
    return value