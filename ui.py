"""Console Output Helpers
"""

def line(message, end='\n', pre=' - '):
    return print(pre + message, end=end)

def title():
    block('Virtual Host Helper for XAMPP\n'
        'by: Gerard Balaoro\n\nhttps://github.com/GerardBalaoro/VHoster',
        title='VHOSTER')

def block(contents, title='', padding=1):
    hline = chr(9552)
    vline = chr(9553)
    cor_ur = chr(9559)
    cor_ul = chr(9556)
    cor_dr = chr(9565)
    cor_dl = chr(9562)
    cor_mr = chr(9571)
    cor_ml = chr(9568)

    lines = []
    if not isinstance(contents, list):
        contents = str(contents)
        contents = contents.split('\n')

    def mkline(text, size, l, r):
        return l + text.center(size) + r

    size = len(max(title, max(contents, key=len), key=len)) + padding * 2
    size = 50 if size < 50 else size

    lines.append(mkline(hline * size, size, cor_ul, cor_ur))

    if len(title):
        lines.append(mkline(title, size, vline, vline))
        lines.append(mkline(hline * size, size, cor_ml, cor_mr))

    for line in contents:
        lines.append(mkline(line, size, vline, vline))
        
    lines.append(mkline(hline * size, size, cor_dl, cor_dr))
    print('\n'.join(lines))

