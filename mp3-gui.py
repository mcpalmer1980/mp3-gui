#!bin/python
import os, sys, pickle, time
import PySimpleGUI as sg
from mutagen.easyid3 import EasyID3 as ID3
from shutil import copy

## G L O B A L  V A L U E S
tools = ('Sync to Dest', 'Remove Extras', 'Verify Filenames', 'Show Artists',
        'Show Albums', 'Show non-MP3s', 'Make Artist Playlist', 'Make Album Playlists',
        'Fix Playlist', 'Change Theme')
themes = sg.theme_list()


def main():
    options = load_options()
    window = main_window()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print.window = window
        print(f'{event}: {values}')

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        elif event == 'Clear':
            print.buffer = ''
        elif event == "Change Theme":
            window = theme_menu(window)
        elif event == "Sync to Dest":
            sync_menu()

        window["CONSOLE"].update(print.buffer)

    print.window = None
    window.close()
    save_options(options)


## W I N D O W S
def main_window(theme='DarkBlack1', size=16):
    opt1 = tools[:6]
    opt2 = tools[6:]

    theme = options.get('theme', theme)
    sg.set_options(font=options['font'])
    sg.theme(theme)
    layout = [[sg.Button(opt) for opt in opt1],
              [sg.Button(opt) for opt in opt2],
              [sg.Multiline(default_text=print.buffer, enable_events=False, size=(120, 20),
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
              [sg.Push(), sg.Button('Clear'), sg.Button('Copy'), sg.Button('Save')] ]
    return sg.Window('MP3 Gui', layout, font=options['font'], finalize=True)

def theme_menu(parent):
    font, size = options['font']
    layout = [[sg.Listbox(values=themes, size=(30,10), key='LIST')],
             [sg.Text('Size:'), sg.Slider(default_value=size, range=(6,24),
                    key='size', orientation='h')],
             [sg.Push(), sg.Button('Cancel'), sg.Button('Change')]]
 
    print('Changing theme')    
    window = sg.Window("Theme Chooser", layout, modal=True, font=options['font'])
    while True:
        event, values = window.read()
        if event == 'Change':
            theme = values.get('LIST')
            new_size = int(values.get('size', size))
            options['font'] = (font, new_size)
            if new_size != size:
                print(f'Size changed to {new_size}')
            if theme and theme[0] in themes:
                theme = theme[0]
                print(f'Theme changed to {theme}')
                options['theme'] = theme
            window.close()
            parent.close()
            return main_window(theme)
              
        elif event in (sg.WIN_CLOSED, 'Cancel'):
            print('Canceled theme change')
            window.close()
            break
    return parent

def sync_menu(source='', dest=''):
    source = options.get('source', source)
    dest = options.get('dest', dest)
    print('Opening sync menu')
    print.buffer, _buffer = getattr(sync_menu, 'buffer', ''), print.buffer # save a backup
    boxes = ('Missing', 'Different', 'Same', 'Extra', 'Clear', 'CRC')
    checked = dict(Missing=True)
    scanned = False
    tooltips = dict(
        Missing='Show/Copy files missing in dest folder',
        Different='Show/Copy files different in dest folder',
        Extra='Show/Copy non-MP3 files from source folder',
        Same='Show/Copy files that are the same in dest folder',
        Clear='Clear album title in dest folder',
        CRC='Use CRC value to compare source and dest folders(slow)')

    layout = [[sg.Text('Source', size=10),
                sg.In(source, size=(50,1), enable_events=True ,key='SOURCE'),
                sg.FolderBrowse(initial_folder=source)],
            [sg.Text('Dest', size=10),
                sg.In(dest, size=(50,1), enable_events=True ,key='DEST'),
                sg.FolderBrowse(initial_folder=dest)],
            [sg.Checkbox(box, key=box, tooltip=tooltips[box], enable_events=True,
                    default=checked.get(box, False)) for box in boxes],
            [sg.Multiline(enable_events=False, size=(100, 15),
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
            [sg.Push(), sg.Button('Cancel'), sg.Button('Scan'), sg.Button('Copy', disabled=True)] ]
    
    window = sg.Window('Sync Files', layout, modal=True, finalize=True)
    window['CONSOLE'].update(print.buffer)
    while True:
        print.window = window
        event, values = window.read()
        values = values or {}
        opts = {k:values.get(k, False) for k in boxes}
        source = values.get('SOURCE', source)
        dest = values.get('DEST', dest)

        if event in ('Cancel', sg.WIN_CLOSED):
            window.close()
            break
        elif event == 'Scan':
            scanned = False
            window['Copy'].update(disabled=True)
            results = load_data(source, dest)
            time.sleep(1)
            if results:
                files, artists, folders, extra = results
                print.window = None
                options['source'] = source
                options['dest'] = dest
                results = check_files(files, extra, source, dest, opts)
                window['Copy'].update(disabled=False)
                window['CONSOLE'].update(print.buffer)
                window.Refresh()
                scanned = True
        elif event == 'Copy':
            files = pick_files(results, opts)
            make_folders(dest, folders)
            sync_menu.buffer, print.buffer = print.buffer, _buffer
            window.close()
            copy_files(files, source, dest, opts)
            return

        elif event in boxes and scanned:
            print.window = None
            results = check_files(files, extra, source, dest, opts)
            window['Copy'].update(disabled=False)
            window['CONSOLE'].update(print.buffer)
            window.Refresh()


    sync_menu.buffer, print.buffer = print.buffer, _buffer 
    print.window = None

def old_copy_files(files):
    files, *_ = mp3.get_files(source, )
    total = len(files)
    max_length = 80
    trim = max_length - len('Copying ')

    # Display a progress meter. Allow user to break out of loop using cancel button
    for i, fn in enumerate(files):
        if not sg.one_line_progress_meter('Copying Files', i+1, total, 
                f'Syncing Files from {source} to {dest}', f'Copying {fn[-trim:]}',
                orientation='h', no_titlebar=True, size = (max_length, 3), grab_anywhere=False,
                bar_color=('white', 'red')):
            print(f'Canceled sync at file {fn}')
            break
        time.sleep(.02)


## U T I L I T Y  F U N C T I O N S
_print = print
def print(line):
    line = str(line)
    _print(line)
    print.buffer += line+'\n'
    if print.window:
        try:
            print.window['CONSOLE'].update(print.buffer)
            print.window.Refresh()
        except:
            pass
print.buffer = '' 
print.window = None

'''
class Printer():
    buffers = {}
    controls
    
    def __call__():
        
    def set(name, control):
        Printer.buffer = Printer.buffers.get(name, '')
        Printer.buffers[name] = Printer.buffer
        Printer.control = control
    def clear()
    def previous()
    def refresh()
'''

def load_options(path=None):
    global options
    if not path:
        path = os.getcwd()
    fn = os.path.join(path, 'options.cfg')
    try:
        with open(fn, 'rb') as file:
            options = pickle.load(file)
        print(f'options loaded from {fn}')
        load_options.options = options.copy()
    except:
        load_options.options = None
        options = dict(
            source = '/home/michael/Music',
            dest = '/tmp/music_out',
            font = ('Arial', 16))
        print('Failed to load options: setting default')
    print(f'  {options}')
    if options.get('theme', None) in themes:
        sg.theme(options['theme'])
    return options

def save_options(options, path=None):
    if not path:
        path = os.getcwd()
    if options != load_options.options:
        fn = os.path.join(path, 'options.cfg')
        print(f'Options changed: saving to {fn}')
        with open(fn, 'wb') as file:
            pickle.dump(options, file)
    else:
        print('Options unchanged: not saving')


## M P 3  F U N C T I O N S
def get_artists(files, path):
    artists = {}
    for f in files:
        tags = ID3(os.path.join(path, f))
        artist = tags.get('Artist', [None,])[0]
        album = tags.get('Album', [artist,])[0]
        l = artists.get(artist, [])
        l.append((f, album))
        artists[artist] = l
    return artists

def load_data(source, dest):
    if not os.path.isdir(source):
        print(f'{source} is not a folder')
        return
    if not os.path.isdir(dest):
        try:
            os.mkdir(dest)
        except:
            print(f'{dest} is not a folder')
            return

    ti = time.perf_counter()
    files, extra, folders = get_files(source)
    artists = get_artists(files, source)
    ti = (time.perf_counter() - ti) * 1000
    print(f'found {len(files)} MP3s, {len(extra)} other files in {ti:0.2f}ms')

    return files, artists, folders, extra

def get_files(path, extensions=('.mp3',), subfolders=True):
    'Create image list from given path and file extensions'
    depth = len(path[1:].split(os.sep))
    trim = len(path) if path.endswith(os.sep) else len(path) + 1
    files = []
    extra = []
    folders = []

    print(f'Scanning files in {path}')
    total = 0
    if subfolders:
        for (dirpath, dirnames, filenames) in os.walk(path):
            sp = dirpath[1:].split(os.sep)
            dots = '.'*(len(sp) - depth)
            in_folder = 0
            for filename in filenames:
                total += 1
                if os.path.splitext(filename)[-1].lower() in extensions:
                    files.append(os.path.join(dirpath, filename)[trim:])
                    in_folder += 1
                else:
                    extra.append(os.path.join(dirpath, filename)[trim:])
            for dirname in dirnames:
                folders.append(os.path.join(dirpath, dirname)[trim:])
            if in_folder:
                print(f'  {dots}{sp[-1]}: {in_folder} MP3s')
    else:
        for f in os.listdir(path):
            if os.path.splitext(f)[-1].lower() in extensions:
                files.append(os.path.join(path, f))
                total += 1

    return files, extra, folders

def check_files(files, extra, sdir, ddir, opts):
    missing = []
    older = []
    differ = []
    same = []
    nextra = []
    displayed = 0
    ti = time.perf_counter()

    if opts['Extra']:
        if not (opts['Missing'] or opts['Different'] or opts['Same']):
            files = extra
        else:
            files = files + extra

    files.sort(key=lambda s: s.lower())
    print(f'Comparing {len(files)} files')
    for file in files:
        _print(sdir, file)
        source = os.path.join(sdir, file)
        dest = os.path.join(ddir, file)

        if opts['Extra'] and files == extra:
            nextra.append((source, dest))
            print(f"{file} extra"); displayed += 1
        elif not os.path.isfile(dest):
            if opts['Missing']:
                print(f"{file} missing"); displayed += 1
            missing.append((source, dest))
        elif os.path.getsize(dest) != os.path.getsize(source):
            if opts['Different']:
                print(f"dest '{file}' differs"); displayed += 1
            differ.append((source, dest))
        elif opts['CRC'] and check_crc(source, dest):
            pass
        elif os.path.getmtime(dest) < os.path.getmtime(source):
            if opts['Older']:
                print(f"dest '{file}' older"); displayed += 1
            older.append((source, dest))
        else:
            if opts['Same']:
                print(f"dest '{dest}' skipped")
            same.append((source, dest))
    ti = (time.perf_counter() - ti) * 1000
    print(f'Compared {len(files)} files in {ti:.2f}ms, displayed {displayed}')
    return missing, older, differ, same, nextra

def make_folders(dest, folders):
    for folder in folders:
        f = os.path.join(dest, folder)
        if not os.path.exists(f):
            os.mkdir(f)

def pick_files(results, opts):
    missing, older, differ, same, extra = results
    which = []
    if opts['Missing']:
        which += missing
    if opts['Different']:
        which += older
        which += differ
    if opts['Same']:
        which += same
    if opts['Extra']:
        which += extra
    return which

def copy_files(files, source, dest, opts):
    total = len(files)
    clear = opts['Clear']
    max_length = 80
    trim = max_length - len('Copying ')
    src_trim = len(source) + 1

    print(f'Copying {len(files)} files')
    for i, file in enumerate(files):
        _source, _dest = file
        src = _source[src_trim:]
        if not sg.one_line_progress_meter('Copying Files', i+1, total, 
                f'Syncing Files from {source} to {dest}', f'Copying {src[-trim:]}',
                orientation='h', no_titlebar=True, size = (max_length, 3), grab_anywhere=False,
                bar_color=('white', 'red')):
            print(f'Canceled sync at file {source}')
            break

        if clear:
            tmp = os.path.join(temp_dir, os.path.split(_dest)[1])
            copy(_source, tmp)
            tags = ID3(tmp)
            artist = tags.get('Artist', [None,])[0]
            tags['Album'] = artist
            tags.save()
            _source = tmp
        copy(_source, _dest)
        print(_source)
        if clear:
            os.remove(tmp)
        time.sleep(.2)


if __name__ == '__main__':
    main()