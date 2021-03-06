#Library with useful Python functions for common needs 

AndyFX: Created in 2017, updated in 2020

**Usage:**

Install requirements

```

pip install -r requirements.txt

```


**List of functions:**

```python
 cur_timestamp(fmt='%Y.%m.%d %H:%M:%S')
 save_log(text, filename='log.txt', new=False, scr=False)
 get_next(lst)
 cur_dir(name='')
 make_dir(full_path, warns=True)
 os_join(path, *paths)
 get_filelist(the_pathes, included_ext=['.txt'])
 save_txt(filename, text, rewrite=False, codec='utf-8', warns=True)
 load_txt(filename, codec='utf-8', warns=True)
 is_exists(filename)
 filesize(file)
 file_rename(old_name, new_name)
 file_delete(filename)
 file_backup(filename, older_ext='bak', warns=True)
 file_date(filename, fmt='', warns=True)
 delete_folder_content(folder)
 txt_to_list(txt)
 list_to_txt(lst)
 are_lists_same(lst1, lst2)
 gLeft(expression, delimiter)
 gRight(expression, delimiter, only_first=True)
 gMid(expression, delimiter1, delimiter2)
 make_list_unique(lst)
 is_pinged_ok(url, timeout=5, ok_statuses=[200, 201])
 send_mail(toaddr, subject, body, fromaddr, pwd)
 my_ip0()
 my_external_ip()
 find_location_in_registry(prog_name)
 get_free_space_mb(dirname)
 get_pc_stat()
 make_session_id2(st)
 make_session_id(st)
 read_ini(INI_FILE, section, key, default)
 write_ini(INI_FILE, section, key, value)
 txt_lines_from_end(txt, lines_num)
 sep(s, thou=',', dec='.', show_decimals=True)
 to_list(text_or_list, separator=',')
 stamp_to_time(stamp, fmt='%d.%m.%Y %H:%M:%S')
 timeit(method)
 timed(*args, **kw)
 sort_by_key(lst_of_dicts, the_key, reverse=True)
 sort_dict_by_subkey(dict, sub_key)
 def_list(filename, pseudo='', numbers=False)
 test_me(operation, tries=5, loops=100000)
 
 ```