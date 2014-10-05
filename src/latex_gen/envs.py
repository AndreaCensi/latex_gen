from .utils import latex_escape


def env(name, content, param=None):
    s = '\\begin{%s}' % name
    if param:
        s += ('{%s}' % param)
#    s += '%%\n%s%%\n' % content
    s += content
    s += ('\\end{%s}' % name)
    return s


def minipage(width, content):
    return env('minipage', content, param=width)


def verbatim(content):
    return env('verbatim', content)


def enclose(name, content):
    return '\\%s{%s}' % (name, content)


def protect(content):
    return '{%s}' % content


def small(content):
    return protect(enclose('small', content))


def texttt(content):
    return enclose('texttt', content)


def emph(content):
    return enclose('emph', content)


def verbatim_soft(content):
    return texttt(latex_escape(content))


def color_rgb(x, col):
    return (protect('\\color[rgb]{%s,%s,%s}%s' %
                    (col[0], col[1], col[2], x)))


def fbox(x):
    return enclose('fbox', x)


def hspace(x):
    return '\\hspace{%s}' % x

