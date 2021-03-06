import codecs, os, smtplib, socket
import configparser
import shutil
import requests
import time
import ctypes
import platform
import psutil
import re
import hashlib, base64, uuid
import logging


from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

VER = '1.3'
VER_DATE = '3/31/2018'


def cur_timestamp(fmt='%Y.%m.%d %H:%M:%S'):
    return str(datetime.strftime(datetime.now(), fmt))


def save_log(text, filename='log.txt', new=False, scr=False):
    save_txt(filename, cur_timestamp() + ' ' + text + '\n', rewrite=new, warns=False)
    if scr:
        print(text)


def get_next(lst):
    itm = lst.pop(0)
    lst.append(itm)
    return itm


def cur_dir(name=''):
    name = __file__ if name == '' else name
    dir = os.path.dirname(os.path.abspath(name))
    dir = os.path.join(dir, '')
    return dir


def make_dir(full_path, warns=True):
    try:
        os.makedirs(full_path, exist_ok=True)
    except Exception as err:
        if warns:
            print(err)


def os_join(path, *paths):
    return os.path.join(path, *paths)


def get_filelist(the_pathes, included_ext=['.txt']):
    file_names = [fn for fn in os.listdir(the_pathes)
                  if any(fn.endswith(ext) for ext in included_ext)]
    return file_names


def save_txt(filename, text, rewrite=False, codec='utf-8', warns=True):
    mode = 'w' if rewrite else 'a'
    saved = False
    try:
        with codecs.open(filename, mode, codec) as temp:
            temp.write(text)
            saved = True
    except Exception as err:
        if warns:
            print(err)
    return saved


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


def filesize(file):
    result = -1
    try:
        result = os.stat(file).st_size
    except Exception as err:
        print(err)
    return result


def file_rename(old_name, new_name):
    """
    Sub for file renaming
    :param old_name: old file name with full path
    :param new_name: new filename with full path
    :return: 
    """
    try:
        shutil.move(old_name, new_name)
    except Exception as err:
        print(err)
    return


def file_delete(filename):
    """
    Sub for file delete
    :param filename: full path and filename to delete
    :return: bool True if OK, False if error
    """
    result = False
    try:
        os.remove(filename)
        result = True
    except Exception as err:
        print(err)
    return Result


def file_backup(filename, older_ext='bak', warns=True):
    if is_exists(filename):
        try:
            ext = filename.split('.')[-1]  # get extension
            file_rename(filename, filename.replace(ext, older_ext))
        except Exception as err:
            if warns:
                print(err)


def file_date(filename, fmt='', warns=True):
    file_d = 0
    try:
        mtime = os.path.getmtime(filename)
        file_d = datetime.fromtimestamp(mtime)
        if fmt:
            file_d = datetime.strftime(file_d, fmt)
    except OSError as err:
        if warns:
            print(err)
    return file_d


def delete_folder_content(folder):
    """
    Sub for deletion of all files and subfolders in a selected folder
    :param folder: Full path to the folder, where all data should be removed
    :return: Empty string or Error message
    """
    result = ''
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # it's the same as os.remove()
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as err:
            print(err)
            result = str(err)
    return result


def txt_to_list(txt):
    txt = txt.replace('\r', '') 
    result = txt.split('\n')
    return result


def list_to_txt(lst):
    return '\n'.join(lst)


def are_lists_same(lst1, lst2):
    result = False
    if set(lst1) == set(lst2):
        result = True
    return result


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


def is_pinged_ok(url, timeout=5, ok_statuses=[200, 201]):
    # import requests
    result, status, msg = True, 0, ''
    try:
        r = requests.get(url, timeout=timeout)
        status = r.status_code
        if status not in ok_statuses:
            result = False
    except Exception as err:
        msg = str(err)
        result = False
    return {'result': result, 'status': status, 'msg': msg}


def send_mail(toaddr, subject, body, fromaddr, pwd):
    '''
    Send email from predefined mailbox 

    :param toaddr: email address 'to'
    :param subject: email subject
    :param body: email body
    :param fromaddr: from address
    :param pwd: password to mailbox
    :return:  string '' or error message
    '''
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    res = ''  # default value is empty string
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, pwd)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return res
    except Exception as error:
        res = 'Something wrong with email sending...'
        print(res + '\n' + str(error))
        return res


def my_ip0():
    ret = ''
    try:
        ret = socket.gethostbyname(socket.gethostname())
    except Exception as err:
        print(err)
    finally:
        if ret == '127.0.0.1':
            ret = socket.gethostbyname(socket.getfqdn())
    return ret


# def my_external_ip():
#     ip = ''
#     try:
#         # ip = get('https://api.ipify.org').text
#         ip = ipget.myip()
#     except Exception as err:
#         print(err)
#     return ip


def find_location_in_registry(prog_name):
    # find location of installed program in registry - not for all installations working
    locations = {}
    try:
        import winreg
    except ImportError:
        import _winreg as winreg
    search_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\" + prog_name
    try:
        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, search_path)
        num_values = winreg.QueryInfoKey(handle)[1]
        for i in range(num_values):
            value = winreg.EnumValue(handle, i)
            names = value[0]
            values = value[1]
            keys = value[2]
            print(names)
            print(values)
            print(keys)
            if names == '':
                locations['location'] = values
            elif names == 'Path':
                locations['path'] = values
            elif names == 'SaveURL':
                locations['SaveURL'] = values
            elif names == 'useURL':
                locations['useURL'] = values
    except Exception as err:
        locations['error'] = err.strerror
    return locations


def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    # import ctypes
    # import platform

    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024


def get_pc_stat():
    # import psutil
    result = {}
    try:
        cpu_percent = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory()
        result = {'cpu': cpu_percent, 'memory': mem_usage}
    except Exception as err:
        print(str(err))
    return result


def make_session_id2(st):
    # import hashlib, time, base64
    m = hashlib.md5()
    m.update(
        b'ThiS is s B tTheJdsYsdef9igvcj;fpoqertre{((string d]dpWS{shsvcj;fpoqertreq ((string d sd WS sdue#WERRiwedjcjdhQQWQWWuehrjvcj;fpoqertreq ((string d sd WS sws fddeeuriewhfncsdbvjhwerh00')
    m.update(str(time.time() * time.time()).encode('utf-8'))
    m.update(str(st).encode('utf-8'))
    m.hexdigest()
    result = base64.b64encode(m.digest()).decode('utf-8')
    return result


def make_session_id(st):
    # import base64, uuid
    x = uuid.uuid1()
    print(str(x))

    x = uuid.uuid3(x, 'test')
    print(str(x))

    x = uuid.uuid4()
    print(str(x))

    x = uuid.uuid5(x, 'test')
    print(str(x))

    r_uuid = str(base64.urlsafe_b64encode(uuid.uuid4().bytes))
    return r_uuid.replace('=', '')
    return r_uuid.replace('=', '')


def read_ini(INI_FILE, section, key, default):
    result = default
    try:
        config = configparser.RawConfigParser()
        config.read(INI_FILE)
        result = config.get(section, key)
    except Exception as err:
        pass
    return result


def write_ini(INI_FILE, section, key, value):
    try:
        config = configparser.RawConfigParser()
        # config.add_section(section)
        config.read(INI_FILE)
        config.set(section, key, value)
        # Writing our configuration file to INI_FILE
        with open(INI_FILE, 'w') as configfile:
            config.write(configfile)
    except Exception as err:
        print(err)
    return


def txt_lines_from_end(txt, lines_num):
    pass


def sep(s, thou=',', dec='.', show_decimals=True):
    s = str(s)
    all = s.split('.')
    try:
        integer = all[0]
    except Exception:
        integer = ''

    try:
        decimal = all[1]
    except Exception:
        decimal = ''
    integer = re.sub(r'\B(?=(?:\d{3})+$)', thou, integer)
    if show_decimals:
        return integer + dec + decimal
    else:
        return integer


def to_list(text_or_list, separator=','):
    if isinstance(text_or_list, str):
        return text_or_list.split(separator)
    elif isinstance(text_or_list, list):
        return text_or_list
    else:
        return []


def stamp_to_time(stamp, fmt='%d.%m.%Y %H:%M:%S'):
    stamp = float(stamp)
    dt = datetime.fromtimestamp(stamp)
    if fmt:
        return dt.strftime(fmt)
    else:
        return dt
    return


def timeit(method):
    '''
    Timeit function for usage as a decorator
    :param method: 
    :return: 
    '''

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(method.__module__ + '.{}(): {:2.2f} ms'.format(method.__name__, (te - ts) * 1000))
        return result

    return timed


def sort_by_key(lst_of_dicts, the_key, reverse=True):
    return sorted(lst_of_dicts, key=lambda r: r[the_key], reverse=reverse)


def sort_dict_by_subkey(dict, sub_key):
    return sorted(dict.keys(), key=lambda x: (dict[x][sub_key], dict[x]))


def def_list(filename, pseudo='', numbers=False):
    try:
        version = VER
    except NameError:
        version = ''

    try:
        ver_date = ' from {}'.format(VER_DATE)
    except NameError:
        ver_date = ''

    print('Functions in "{}" [ver.{}{}]:'.format(filename if pseudo == '' else pseudo, version, ver_date))
    # import re
    pattern = re.compile("de" + "f (.*)\:")
    counter = 1
    for i, line in enumerate(open(filename)):
        for match in re.finditer(pattern, line):
            print('{:<5}'.format(counter) if numbers else '', match.groups()[0])
            counter += 1


def test_me(operation, tries=5, loops=100000):
    all = []
    print('Start speed test for {} loops in {} tries:'.format(loops, tries))
    print('Operation: {}'.format(operation))
    for outer in range(1, tries + 1):
        ts = time.time()
        for inner in range(1, loops + 1):
            # >----- function to test start ----->
            result = eval(operation)
            # c = "Andy and {} = {}".format(a, b)
            # c = "Andy and " + a + " = " + b
            # <----- function to test end   -----<
        te = time.time()
        t = (te - ts) * 1000
        all.append(t)

    for i, t in enumerate(all):
        print('try {}: {:2.2f} ms'.format(i + 1, t))
    sum_ = sum(all)
    avg_ = sum_ / len(all)
    min_, max_ = min(all), max(all)
    ampl = max_ - min_
    print('Avg time: {:2.2f} ms, per one loop: {:2.8f} ms'.format(avg_, avg_ / loops))
    out = 'Min time: {:2.2f} ms, max time: {:2.2f} ms, amplitude: {:2.2f} ms'.format(min_, max_, ampl)
    a_ = len(out) - 2
    l_ = a_ * '-'
    a_pos = int((avg_ / max_) * a_)
    print(out)
    t_ = l_[:a_pos - 1] + 'X' + l_[a_pos:]
    print('|{}|'.format(t_))
    print('Total   time: {:2.2f} ms'.format(sum_))
    print('Operation result: {}\n'.format(result))

def set_logger(log_file,
               min_level=logging.DEBUG,
               file_log_level=logging.INFO,
               screen_log_level=logging.WARNING, delete_previous_log=False):
    """
    Create logger & set parameters needed
    :param log_file: str log file name 
    :param min_level: optional = minimum logging level
    :param file_log_level: optional = level for save to file 
    :param screen_log_level: optional = level to show on a screen
    :return: logger object  
    """
    if delete_previous_log:
        file_delete(log_file)

    the_logger = logging.getLogger()
    the_logger.setLevel(min_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(log_file)
    fh.setLevel(file_log_level)
    fh.setFormatter(formatter)
    the_logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(screen_log_level)
    ch.setFormatter(formatter)
    the_logger.addHandler(ch)
    return the_logger

if __name__ == '__main__':
    def_list(__file__)
    # test_me('"Andy and {} = {}".format("Julia", "Love")')
    # test_me('"Andy and " + "Julia" + " = " + "Love"')
