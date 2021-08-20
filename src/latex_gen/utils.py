from contextlib import contextmanager

from typing import Dict


def latex_escape(s):
    # Do this at the beginning
    s = s.replace("\\", "\\textbackslash ")
    s = s.replace("{", "\\{")
    s = s.replace("}", "\\}")
    s = s.replace("^", "\\^")
    replace = {"_": "\\_", "$": "\\$"}  # '\\_',
    for k in replace:
        s = s.replace(k, replace[k])
    return s


@contextmanager
def begin_end(stream, env_name, options: Dict[str, str] = None):
    options = options or {}
    stream.write("\\begin{%s}" % env_name)
    if options:
        stream.write("[%s]" % (options))
    stream.write("%\n")

    yield stream
    stream.write("\\end{%s}%%\n" % env_name)
