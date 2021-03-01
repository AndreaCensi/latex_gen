

def texif(cmd, use, otherwise):
    return "\\ifx %s\\undefined %s\\else %s\\fi" % (cmd, otherwise, use)


def makeupcmd(name):
    return (texif("\\%s" % name, "", "\\newcommand{\\%s}{%s}" % (name, name))
             + '\n')


def makecmd(frag, desired):
    actual = safecmd(desired)
    frag.tex(makeupcmd(actual))
    return '\\' + actual


def safecmd(s):
    rep = {'-': '', '_': '', ':': '', '.': '',
           '0': 'Z', '1': 'O', '2': 't', '3': 'T', '4': 'f',
           '5': 'F', '6': 's', '7': 'S', '8': 'E',
           '9': 'N'}
    for a, b in list(rep.items()):
        s = s.replace(a, b)
    return s
