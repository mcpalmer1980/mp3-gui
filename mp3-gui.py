#!bin/python
import os, sys, pickle, time, pyperclip, zlib
import PySimpleGUI as sg
from mutagen.easyid3 import EasyID3 as ID3
from shutil import copy

## G L O B A L  V A L U E S
tools = ('Sync to Dest', 'Remove Extras', 'Verify Filenames', 'Show Artists',
        'Show Albums', 'Show non-MP3s', 'Make Artist Playlist', 'Make Album Playlists',
        'Fix Playlist', 'Change Theme')
tooltips = {
    'Sync to Dest': 'Sync MP3s from source to dest folder',
    'Remove Extras': 'Remove non-MP3 files from source folder',
    'Verify Filenames': 'Check for and fix mangled filenames',
    'Show Artists': 'Show all artists in source folder (for fixing misspellings etc)',
    'Show Albums': 'Show all albums with song counts in source folder',
    'Show non-MP3s': 'Show/Delete non-MP3 files in source folder',
    'Artist Playlists': 'Make playlists for artists with x songs or more',
    'Album Playlists': 'Make playlists for albums with x songs or more',
    'Fix Playlist': 'Normalize playlist for root folder and remove extra lines',
    'Change Theme': 'Change GUI colors and font size' }
tools = list(tooltips.keys())
themes = sg.theme_list()
temp_dir = '/tmp'


def main():
    options = load_options()
    window = main_window()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print.window = window

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Clear':
            print.buffer = ''
        elif event == "Change Theme":
            window = theme_menu(window)
        elif event == "Sync to Dest":
            sync_menu()
        elif event == 'Copy':
            pyperclip.copy(print.buffer)
        else:
            print(f'{event}: {values}')

        window["CONSOLE"].update(print.buffer)

    print.window = None
    window.close()
    save_options(options)


## W I N D O W S
def main_window(theme='DarkBlack1', size=16):
    opt1 = tools[:6]
    opt2 = tools[6:]

    theme = options.get('theme', theme)
    font = options.get('font', ('Arial', size))
    sg.set_options(font=font, tooltip_font=font)
    sg.theme(theme)
    layout = [[sg.Button(opt, tooltip=tooltips[opt]) for opt in opt1],
              [sg.Button(opt, tooltip=tooltips[opt]) for opt in opt2],
              [sg.Multiline(default_text=print.buffer, enable_events=False, size=(120, 20),
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
              [sg.Push(), sg.Button('Clear'), sg.Button('Copy'), sg.Button('Save')] ]
    return sg.Window('MP3 Gui', layout, font=options['font'], finalize=True)

def theme_menu(parent):
    font, size = options['font']
    theme = options['theme']
    layout = [[sg.Listbox(values=themes, size=(30,10), key='LIST')],
             [sg.Text('Size:'), sg.Slider(default_value=size, range=(6,24),
                    key='size', orientation='h')],
             [sg.Push(), sg.Button('Cancel'), sg.Button('Change')]]
 
    print('Changing theme')    
    window = sg.Window("Theme Chooser", layout, modal=True,
            font=options['font'], finalize=True)

    if theme in themes:
        i = themes.index(theme)
        window['LIST'].update(set_to_index=[i], scroll_to_index=i)
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
            return main_window()
              
        elif event in (sg.WIN_CLOSED, 'Cancel'):
            print('Canceled theme change')
            window.close()
            break
    return parent

def sync_menu(source='', dest=''):
    def update(results):
        files, artists, folders, extra = results
        print.window = None
        options['source'] = source
        options['dest'] = dest
        results = check_files(files, extra, source, dest, opts)
        if results:
            window['Copy'].update(disabled=False)
            window['Clip Filenames'].update(disabled=False)
            scanned = True
        window['CONSOLE'].update(print.buffer)
        window.Refresh()
        return results

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
            [sg.Button('Clip Filenames', disabled=True), sg.Push(), sg.Button('Cancel'), 
                    sg.Button('Scan'), sg.Button('Copy', disabled=True)] ]
    
    window = sg.Window('Sync Files', layout, modal=True, finalize=True)
    window['CONSOLE'].update(print.buffer)
    results = False
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
            print.buffer = ''
            window['Copy'].update(disabled=True)
            window['Clip Filenames'].update(disabled=True)
            results = load_data(source, dest)
            time.sleep(1)
            if results:
                final_results = update(results)
        elif event == 'Copy':
            files, artists, folders, extra = results
            files = pick_files(final_results, opts)
            r = sg.popup_ok_cancel(f'Copy {len(files)} files to {dest}?', title='Copy')
            if r == 'Cancel':
                continue
            make_folders(dest, folders)
            sync_menu.buffer, print.buffer = print.buffer, _buffer
            window.close()
            copy_files(files, source, dest, opts)
            return
        elif event == 'Clip Filenames':
            clip_files(final_results, opts)
        elif event in boxes and results:
            print.buffer = ''
            final_results = update(results)
            if not final_results:
                window['Copy'].update(disabled=True)
                window['Clip Filenames'].update(disabled=True)



    sync_menu.buffer, print.buffer = print.buffer, _buffer 
    print.window = None


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

def time_str(ti):
    ti = (time.perf_counter() - ti) * 1000
    if ti < 1000:
        return f'{ti:.0f} ms'
    elif ti < 1000 * 60 * 2:
        return f'{ti/1000:.2f} s'
    else:
        return f'{ti/(1000*60):.1f} min'

def check_CRC(f1, f2):
    if get_CRC(f1) == get_CRC(f2):
        return True

def get_CRC(fpath):
    """With for loop and buffer."""
    crc = 0
    with open(fpath, 'rb', 65536) as ins:
        for x in range(int((os.stat(fpath).st_size / 65536)) + 1):
            crc = zlib.crc32(ins.read(65536), crc)
    return '%08X' % (crc & 0xFFFFFFFF)


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
    print(f'found {len(files)} MP3s, {len(extra)} other files in {time_str(ti)}')

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
        source = os.path.join(sdir, file)
        dest = os.path.join(ddir, file)

        if opts['Extra'] and files == extra:
            nextra.append((source, dest))
            print(f'{file} (extra)'); displayed += 1
        elif not os.path.isfile(dest):
            if opts['Missing']:
                print(f'{file} (missing)'); displayed += 1
            missing.append((source, dest))
        elif os.path.getsize(dest) != os.path.getsize(source):
            if opts['Different']:
                print(f'{file} (differs)'); displayed += 1
            differ.append((source, dest))
        elif opts['CRC'] and not check_CRC(source, dest):
            if opts['Different']:
                print(f'{file} (CRC differs)'); displayed += 1
            differ.append((source, dest))
        elif os.path.getmtime(dest) < os.path.getmtime(source):
            if opts['Different']:
                print(f'{file} (older)'); displayed += 1
            older.append((source, dest))
        else:
            if opts['Same']: 
                print(f'{file} (same)'); displayed += 1
            same.append((source, dest))
    print(f'Compared {len(files)} files in {time_str(ti)}, displayed {displayed}')

    if not displayed:
        return False
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

def clip_files(results, opts):
    missing, older, differ, same, extra = results
    outp = ''
    if opts['Missing']:
        outp += 'Missing Files\n'
        for l in missing:
            outp += l[0] + '\n'
    if opts['Different']:
        more = sorted(older+differ, key=lambda x: x.lower())
        outp += '\nDifferent Files\n'
        for l in differ:
            outp += l[0] + '\n'
    if opts['Same']:
        outp += '\nSame Files\n'
        for l in same:
            outp += l[0] + '\n'
    if opts['Extra']:
        outp += '\nnon-MP3 Files\n'
        for l in extra:
            outp += l[0] + '\n'
    pyperclip.copy(outp)

def copy_files(files, source, dest, opts):
    total = len(files)
    clear = opts['Clear']
    max_length = 80
    trim = max_length - len('Copying   ')
    src_trim = len(source) + 1
    ti = time.perf_counter()

    print(f'Copying {len(files)} files')
    for i, file in enumerate(files):
        _source, _dest = file
        src = _source[src_trim:]
        if not sg.one_line_progress_meter('Copying Files', i+1, total, 
                f'Syncing Files from {source} to {dest}', f'Copying {src[-trim:]}',
                orientation='h', no_titlebar=False, size = (max_length, 3), grab_anywhere=False,
                bar_color=('white', 'red'), keep_on_top=False):
            print(f'Canceled sync after {time_str(ti)} at file {_source}')
            return

        if clear:
            tmp = os.path.join(temp_dir, os.path.split(_dest)[1])
            copy(_source, tmp)
            tags = ID3(tmp)
            artist = tags.get('Artist', [None,])[0]
            tags['Album'] = artist
            tags.save()
            _source = tmp
        copy(_source, _dest)
        #print(_source)
        if clear:
            os.remove(tmp)
        time.sleep(.2)
    print(f'Finished copying {len(files)} files in {time_str(ti)}')


if __name__ == '__main__':
    main()