import codecs, os


def get_filelist(the_pathes, included_ext=['.txt']):
    file_names = [fn for fn in os.listdir(the_pathes)
                  if any(fn.endswith(ext) for ext in included_ext)]
    return file_names


def save_txt(filename, text, rewrite=False, codec='utf-8', warns=True):
    mode = 'w' if rewrite else 'a'
    try:
        with codecs.open(filename, mode, codec) as temp:
            temp.write(text)
    except Exception as err:
        if warns:
            print(err)


def load_txt(filename, codec='utf-8', warns=True):
    try:
        with codecs.open(filename, 'r', codec) as temp:
            return temp.read()
    except Exception as err:
        if warns:
            print(err)
        return


def is_exists(filename):
    return True if os.path.exists(filename) else False


def txt_to_list(txt):
    txt = txt.replace('\r', '')  # remove \r
    result = txt.split('\n')  # convert to list
    return result


def list_to_txt(lst):
    return '\n'.join(lst)


def gLeft(expression, delimiter):
    r = str(expression).split(delimiter)
    return r[0]


def gRight(expression, delimiter, only_first=True):
    r = str(expression).split(delimiter)
    len_txt = len(r)
    if len_txt >= 2:
        r = r[1] if only_first else r[1:]
    else:
        r = expression
    return r


def gMid(expression, delimiter1, delimiter2):
    return gLeft(gRight(expression, delimiter1), delimiter2)


def make_list_unique(lst):
    set_lst = set(lst)
    return (list(set_lst))


if __name__ == '__main__':
    all = dir(__file__)
    count = len(all)
    print('Functions in file:', count, '\nNames:', all)
    print(__file__)
