from __future__ import annotations



def default_stdlib_names() -> FrozenSet[str]:
    """
    Return the default frozenset of known stdlib module and typing names.
    Defined as a function so it is never a module-level variable.
    No global variables, no classes.
    """
    return frozenset({
        "re", "ast", "os", "sys", "io", "abc", "copy", "math",
        "json", "csv", "time", "datetime", "random", "string",
        "pathlib", "shutil", "tempfile", "glob", "fnmatch",
        "functools", "itertools", "operator", "collections",
        "textwrap", "hashlib", "struct", "enum", "dataclasses",
        "contextlib", "warnings", "logging", "traceback",
        "threading", "multiprocessing", "subprocess",
        "typing", "types", "inspect", "importlib",
        "unittest", "pprint", "pickle", "shelve",
        "socket", "http", "urllib", "email",
        "Dict", "List", "Set", "Tuple", "Optional", "Any",
        "Union", "Callable", "Iterator", "Generator",
        "Type", "ClassVar", "Final", "Literal",
        "Path",
    })
