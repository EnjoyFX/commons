import codecs, os, smtplib, socket
import configparser
import shutil
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def version():
    return '1.1 from 1/10/2018'


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
    :return: 
    """
    try:
        os.remove(filename)
    except BaseException as err:
        print(err)
    return


def file_backup(filename, older_ext='bak', warns=True):
    if is_exists(filename):
        try:
            ext = filename.split('.')[-1]  # get extension
            file_rename(filename, filename.replace(ext, older_ext))
        except BaseException as err:
            if warns:
                print(err)


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
    txt = txt.replace('\r', '')  # remove \r
    result = txt.split('\n')  # convert to list
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


def send_mail(toaddr, subject, body, fromaddr='vba.app@gmail.com', pwd=''):
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
    except BaseException as error:
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
    import ctypes
    import platform
    import sys

    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024


def get_pc_stat():
    import psutil
    result = {}
    try:
        cpu_percent = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory()
        result = {'cpu': cpu_percent, 'memory': mem_usage}
    except Exception as err:
        print(str(err))
    return result


def make_session_id2(st):
    import hashlib, time, base64
    m = hashlib.md5()
    m.update(
        b'ThiS is s B tTheJdsYsdef9igvcj;fpoqertre{((string d]dpWS{shsvcj;fpoqertreq ((string d sd WS sdue#WERRiwedjcjdhQQWQWWuehrjvcj;fpoqertreq ((string d sd WS sws fddeeuriewhfncsdbvjhwerh00')
    m.update(str(time.time() * time.time()).encode('utf-8'))
    m.update(str(st).encode('utf-8'))
    m.hexdigest()
    result = base64.b64encode(m.digest()).decode('utf-8')
    return result


def make_session_id(st):
    import base64, uuid
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
    except BaseException as err:
        print(err)
    return


def def_list(filename, pseudo=''):
    print('Functions in', filename if pseudo == '' else pseudo)
    import re
    pattern = re.compile("de" + "f (.*)\:")
    for i, line in enumerate(open(filename)):
        for match in re.finditer(pattern, line):
            print(match.groups()[0])


if __name__ == '__main__':
    def_list(__file__)
