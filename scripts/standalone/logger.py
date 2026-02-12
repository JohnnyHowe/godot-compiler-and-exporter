import builtins

HIDE_REPLACEMENT = "[redacted]"
hide = set()

_original_print = builtins.print


def sensitive_print(*args, **kwargs):
    args = tuple(filter_text(str(a)) for a in args)
    _original_print(*args, **kwargs)


def filter_text(text: str) -> str:
    for to_hide in hide:
        text = text.replace(to_hide, HIDE_REPLACEMENT)

    return text