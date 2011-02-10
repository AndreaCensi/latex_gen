def latex_escape(s):
    # Do this at the beginning
    s = s.replace('\\', '\\textbackslash ')
    s = s.replace('{', '\\{')
    s = s.replace('}', '\\}')
    s = s.replace('^', '\\^')
    replace = {'_': '\\_', #'\\_', 
               '$': '\\$'
               }
    for k in replace:
        s = s.replace(k, replace[k])
    return s
