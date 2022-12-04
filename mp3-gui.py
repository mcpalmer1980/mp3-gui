#!bin/python
'''
TODO:
update initial folder in sync window when text changes

'''
import os, sys, pickle, time, pyperclip, zlib
import PySimpleGUI as sg
from mutagen.easyid3 import EasyID3 as ID3
from shutil import copy
from io import StringIO

## G L O B A L  V A L U E S
tools = ('Sync to Dest', 'Remove Extras', 'Verify Filenames', 'Artists',
        'Show Albums', 'Show non-MP3s', 'Tags', 'Make Album Playlists',
        'Fix Playlist', 'Change Theme')
tooltips = {
    'Sync to Dest': 'Sync MP3s from source to dest folder',
    'Clean Dest': 'Remove files from dest missing in source folder',
    'Verify Filenames': 'Check for and fix mangled filenames',
    'Artists': 'Show all artists in source folder (for fixing misspellings etc)',
    'Albums': 'Show all albums with song counts in source folder',
    'Genres': 'Show all genres',
    'Show non-MP3s': 'Show/Delete non-MP3 files in source folder',
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
            print.buffer = StringIO()
        elif event == "Change Theme":
            window = theme_menu(window)
        elif event == "Sync to Dest":
            sync_menu()
        elif event == 'Clean Dest':
            clean_menu(window)
        elif event == 'Verify Filenames':
            verify_menu(window)
        elif event == 'Artists':
            category_menu(window, 'Artists')
        elif event == 'Albums':
            category_menu(window, 'Albums')
        elif event == 'Genres':
            category_menu(window, 'Genres')
        elif event == 'Copy':
            pyperclip.copy(print.buffer.getvalue())
        else:
            print(f'{event}: {values}')

        window["CONSOLE"].update(print.buffer.getvalue())

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
              [sg.Multiline(default_text=print.buffer.getvalue(),
                    enable_events=False, size=(120, 20),
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
              [sg.Push(), sg.Button('Clear'), sg.Button('Copy'), sg.Button('Save')] ]
    return sg.Window('MP3 Gui', layout, font=options['font'], finalize=True)

def theme_menu(parent, theme=None):
    font, size = options['font']
    if theme:
        sg.theme(theme)
    else:
        print('Changing theme')    

    layout = [[sg.Listbox(values=themes, size=(30,10), key='LIST',
                    enable_events=True)],
             [sg.Text('Size:'), sg.Slider(default_value=size, range=(6,24),
                    key='size', orientation='h')],
             [sg.Push(), sg.Button('Cancel'), sg.Button('Change')]]
 
    window = sg.Window("Theme Chooser", layout, modal=True,
            font=options['font'], finalize=True)
    sg.theme(options['theme'])

    if theme in themes:
        i = themes.index(theme)
        window['LIST'].update(set_to_index=[i], scroll_to_index=max(i-3, 0))
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
        elif event == 'LIST':
            theme = values['LIST'][0]
            window.close()
            return theme_menu(parent, theme)
    return parent

def sync_menu(source='', dest=''):
    def update(results):
        files, folders, extra = results
        print.window = None
        options['source'] = source
        options['dest'] = dest
        results = check_files(files, extra, source, dest, opts)
        if results:
            window['Copy'].update(disabled=False)
            window['Clip Filenames'].update(disabled=False)
            scanned = True
        window['CONSOLE'].update(print.buffer.getvalue())
        window.Refresh()
        return results

    source = options.get('source', source)
    dest = options.get('dest', dest)
    print('Opening sync menu')
    print.buffer, _buffer = getattr(sync_menu, 'buffer', StringIO()), print.buffer # save a backup
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
    window['CONSOLE'].update(print.buffer.getvalue())
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
            print.buffer = StringIO()
            window['Copy'].update(disabled=True)
            window['Clip Filenames'].update(disabled=True)
            results = load_data(source, dest)
            time.sleep(1)
            if results:
                final_results = update(results)
        elif event == 'Copy':
            files, folders, extra = results
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
            print.buffer = StringIO()
            final_results = update(results)
            if not final_results:
                window['Copy'].update(disabled=True)
                window['Clip Filenames'].update(disabled=True)

    sync_menu.buffer, print.buffer = print.buffer, _buffer 
    print.window = None

def clean_menu(source='', dest=''):
    def update(source, dest, opts):
        extras = find_unexpected(source, dest, opts)
        window['LIST'].update(values=extras or ['Nothing found'])
        if extras:
            window['Clip Filenames'].update(disabled=False)
            window['Remove'].update(disabled=False)
        else:
            window['Clip Filenames'].update(disabled=True)
            window['Remove'].update(disabled=True)
        window['SBUT'].InitialFolder=source
        window['DBUT'].InitialFolder=dest
        options['source'] = source
        options['dest'] = dest
        return extras

    source = options.get('source', source)
    dest = options.get('dest', dest)
    print('Opening clean menu')
    boxes = ('MP3s', 'Other')
    checked = dict(MP3s=True, Other=False)
    tooltips = dict(
        MP3s='Remove extra MP3s from dest folder',
        Other='Remove other extra files from dest folder',
        Remove='Delete shown files from dest folder',
        Swap='Swap source and dest folders')

    layout = [[sg.Text('Source', size=10),
                sg.In(source, size=(50,1), enable_events=True ,key='SOURCE'),
                sg.FolderBrowse(initial_folder=source, key="SBUT"),
                sg.Push(), sg.Button('Swap', tooltip=tooltips['Swap'])],
            [sg.Text('Dest', size=10),
                sg.In(dest, size=(50,1), enable_events=True ,key='DEST'),
                sg.FolderBrowse(initial_folder=dest, key='DBUT')],
            [sg.Checkbox(box, key=box, tooltip=tooltips[box], enable_events=True,
                    default=checked.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning'], size=(100, 15),
                    key="LIST", enable_events=True)],
            [sg.Button('Clip Filenames', disabled=True), sg.Push(), sg.Button('Cancel'), 
                    sg.Button('Remove', tooltip=tooltips['Remove'], disabled=True)] ]
    
    window = sg.Window('Clean Dest Folder', layout, modal=True, finalize=True)

    extras =  update(source, dest, checked)
    while True:
        event, values = window.read()
        values = values or {}
        opts = {k:values.get(k, False) for k in boxes}

        if event in ('Cancel', sg.WIN_CLOSED):
            window.close()
            break
        elif event == 'Remove':
            r = sg.popup_ok_cancel(f'Delete {len(extras)} files from {dest}?', title='Delete')
            if r == 'OK':
                for f in extras:
                    os.remove(os.path.join(dest, f))
                print(f'Deleted {len(extras)} files from {dest}')
                window.close()
                break
        elif event == 'Clip Filenames' and extras:
            s = ''
            for f in extras:
                s += os.path.join(dest, f) + '\n'
            pyperclip.copy(s)
        elif event == 'Swap':
            source, dest = dest, source
            window['SOURCE'].update(source)
            window['DEST'].update(dest)
            extras = update(source, dest, opts)
        elif event in boxes:
            extras = update(source, dest, opts)
        elif event == 'SOURCE':
            nsource = values['SOURCE']
            if comp_dir(source, nsource, True):
                source = nsource
                extras = update(source, dest, opts)
        elif event == 'DEST':
            ndest = values['DEST']
            if comp_dir(dest, ndest, True):
                dest = ndest
                extras = update(source, dest, opts)
        elif event == 'LIST':
            item = values[event][0]
            if item in extras:
                i = extras.index(item)
                extras.remove(item)
                window['LIST'].update(values=extras or ['Nothing found'],
                        scroll_to_index=max(i-2, 0))
            print(f'{event}: {values[event]}')
        else:
            print(f'{event} {values}')

def verify_menu(window):
    source = options['source']
    print('Opening filename menu')
    boxes = ('MP3s', 'Other')


    files = get_files(source, quiet=True)[0]
    items = check_filenames(files)
    layout = [[sg.Text('Source', size=10),
                sg.In(source, size=(50,1), enable_events=True ,key='SOURCE'),
                sg.FolderBrowse(initial_folder=source, key="SBUT")],
            [sg.Listbox(items, size=(100, 15),
                    key="LIST")],
            [sg.Push(), sg.Button('Copy'), sg.Button('Close')] ]
    
    window = sg.Window('Verify Filenames', layout, modal=True, finalize=True)

    while True:
        event, values = window.read()

        if event in ('Close', sg.WIN_CLOSED):
            window.close()
            break
        elif event == 'Copy':
            pyperclip.copy('\n'.join(items))
        elif event == 'Clip Filenames' and extras:
            s = ''
            for f in extras:
                s += os.path.join(dest, f) + '\n'
            pyperclip.copy(s)
        elif event == 'Swap':
            source, dest = dest, source
            window['SOURCE'].update(source)
            window['DEST'].update(dest)
            extras = update(source, dest, opts)
        elif event in boxes:
            extras = update(source, dest, opts)
        elif event == 'SOURCE':
            nsource = values['SOURCE']
            if comp_dir(source, nsource, True):
                source = options['source'] = nsource
                files = get_files(source, quiet=True)[0]
                items = check_filenames(files)
                window['LIST'].update(values=items)

def category_menu(window, mode='Artists'):
    def set_mode(mode):
        if mode == 'Artists':
            print('Opening Artists window')
            return "Artist Lister", list_artists, 1
        elif mode == 'Albums':
            print('Opening Albums window')
            return "Album Lister", list_albums, 3
        elif mode == 'Genres':
            print('Opening Genres window')
            return "Genre Lister", list_genres, 1

    source = options['source']
    modes = ['Artists', 'Albums', 'Genres']
    boxes = ['Sort by Count', 'Extra Details', 'Unfold Details']
    checked = {'Sort by Count':False, 'Extra Details': True}
    opts = [checked.get(k, False) for k in boxes]
    title, list_items, min_count = set_mode(mode)

    layout = [[sg.Text('Source', size=10),
                sg.In(source, size=(50,1), enable_events=True ,key='SOURCE'),
                sg.FolderBrowse(initial_folder=source, key="SBUT"),
                sg.Push(), sg.Combo(modes, default_value=mode, readonly=True,
                    enable_events=True, key='MODE')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=checked.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning...'], size=(100, 15), enable_events=True,
                    key="LIST", horizontal_scroll=True)],
            [sg.Text('Minimum Count'), sg.Input(min_count, size=5,
                    enable_events=True, key='COUNT'),
                sg.Push(), sg.Button('Make Playlists'),
                sg.Button('Copy'), sg.Button('Close')] ]
    
    window = sg.Window(title, layout, modal=True, finalize=True)
    items, indexes, songs = list_items(source, min_count, *opts)
    window['LIST'].update(items)
    while True:
        event, values = window.read()

        if event in ('Close', sg.WIN_CLOSED):
            window.close()
            break
        elif event == 'Copy':
            pyperclip.copy('\n'.join(items))
        elif event == 'Clip Filenames' and extras:
            s = ''
            for f in extras:
                s += os.path.join(dest, f) + '\n'
            pyperclip.copy(s)
        elif event in boxes:
            if event=='Unfold Details' and values.get('Unfold Details', False):
                window['Extra Details'].update(True)
            elif event=='Extra Details' and not values.get('Extra Details', False):
                window['Unfold Details'].update(False)
            opts = [values.get(k, False) for k in boxes]
            items, indexes, songs = list_items(source, min_count, *opts)
            window['LIST'].update(values=items)
        elif event == 'COUNT':
            try:
                min_count = int(values['COUNT'])
            except:
                continue
            items, indexes, songs = list_items(source, min_count, *opts)
            window['LIST'].update(values=items)
        elif event == 'SOURCE':
            nsource = values['SOURCE']
            if comp_dir(source, nsource, True):
                source = options['source'] = nsource
                items, indexes, songs = list_items(source, min_count, *opts)
                window['LIST'].update(values=items)
        elif event == 'MODE':
            title, list_items, min_count = set_mode(values['MODE'])
            items, indexes, songs = list_items(source, min_count, *opts)
            window['LIST'].update(items)
            window['COUNT'].update(min_count)
            window.set_title(title)
        elif event == 'LIST':
            selected = window['LIST'].GetIndexes()[0]
            key = indexes[selected]
            if indexes[selected]:
                value = input_menu('Change Value', default=key)
                if value and value != key:
                    attr = mode.lower()[:-1] # exp: Artists -> artist
                    print(f'Changing {attr} from {key} to {value}')
                    for song in songs[key]:
                        fn = os.path.join(source, song.filename)
                        tag = ID3(fn)
                        tag[attr] = value
                        tag.save()
                    items[selected] = items[selected].replace(key, value, 1)
                    window['LIST'].update(items, set_to_index=[selected],
                            scroll_to_index=max(selected-3, 0))



def input_menu(title, default='None', text=''):
    size = max(50, len(title), len(text))
    layout = [[sg.Text(text)],
              [sg.Input(default, size=size, key='INPUT')],
              [sg.Push(), sg.Button('Cancel'), sg.Button('Okay')]]
    window = sg.Window(title, layout, modal=True)
    event, values = window.read()
    window.close()
    if event == 'Okay':
        return values['INPUT']


## U T I L I T Y  F U N C T I O N S
_print = print
def print(*args, **kargs):
    if print.quiet:
        return
    #line = str(line)
    _print(*args, **kargs)
    _print(*args, file=print.buffer, **kargs)
    #_print(line, file=print.buffer)
    #print.buffer += line+'\n'
    if print.window:
        try:
            print.window['CONSOLE'].update(print.buffer.getvalue())
            print.window.Refresh()
        except:
            pass
print.buffer = StringIO()
print.window = None
print.quiet = False

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

def comp_dir(d1, d2, check_exist=False):
    d1 = os.path.normpath(d1)
    d2 = os.path.normpath(d2)
    r = d1 == d2
    exists = os.path.isdir(d1) and os.path.isdir(d2)
    #print(f'1: {d1}, 2: {d2}, equal: {r}, exists: {exists}')
    return exists and not r

## M P 3  F U N C T I O N S
def check_filenames(files, dashes=False):
    items = []
    for file in files:
        f = os.path.split(file)[1]
        msg = ''
        if f.count('-') < 1:
            msg += 'no dash,'
        if f.count('-') > 1 and dashes:
            msg += 'over dashed,'
        if f.count('—') > 0:
            msg += 'em dash,'
        if f.count('  ') > 0:
            msg += 'misspaced'
        if msg:
            items.append(f'{file} ({msg})')
    print(f'Found {len(items)} malformed filenames')
    return items or ['Nothing Found']

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
        if clear:
            os.remove(tmp)
        time.sleep(.2)
    print(f'Finished copying {len(files)} files in {time_str(ti)}')

def find_unexpected(source, dest, opts):
    sfiles, sextra, *_ = get_files(source, quiet=True)
    dfiles, dextra, *_ = get_files(dest, quiet=True)
    extra = []

    if not opts.get('MP3s', False):
        sfiles = []
        dfiles = []

    if opts.get('Other', False):
        sfiles = sorted(sfiles + sextra, key=lambda x: x.lower())
        dfiles = sorted(dfiles + dextra, key=lambda x: x.lower())

    for file in dfiles:
        if file not in sfiles:
            extra.append(file)
    return extra

def get_tags(files, path, rescan=False):
    class SongTag:
        __slots__ = ('filename', 'title', 'artist', 'album', 'genre')
        def __init__(self, filename, title, artist, album, genre):
            self.filename = filename
            self.title = title
            self.artist = artist
            self.album = album
            self.genre = genre
        def __repr__(self):
            return f'SongTags ({self.title}, {self.artist}, {self.album}, {self.genre})'

    if not hasattr(get_tags, 'history'):
        get_tags.history = {}

    path = os.path.normpath(path)    
    loaded = get_tags.history.get(path, None)
    if loaded and not rescan:
        #print(f'Loaded tag information for {path}')
        return loaded

    ti = time.perf_counter()
    filenames = {}; artists = {}; albums = {}; genres = {}
    for f in files[0]:
        #print(f)
        id3 = ID3(os.path.join(path, f))
        artist = id3.get('Artist', [None,])[0]
        tags = SongTag(
            f,
            id3.get('Title', [None,])[0],
            artist,
            id3.get('Album', [artist,])[0],
            id3.get('Genre', [None,])[0])
        art = artists.get(tags.artist, [])
        alb = albums.get(tags.album, [])
        gen = genres.get(tags.genre, [])
        art.append(tags)
        alb.append(tags)
        gen.append(tags)
        artists[tags.artist] = art
        albums[tags.album] = alb
        genres[tags.genre] = gen
        filenames[f] = tags

    print(f'Scanned for tags in {path} ({time_str(ti)})')
    get_tags.history[path] = artists, albums, genres, filenames
    return get_tags.history[path]

def list_artists(path, min_count=1, by_count=False, details=False, unfold=False):
    ti = time.perf_counter()

    files = get_files(path, quiet=True)
    artists, albums, genres, filenames = get_tags(files, path)

    if by_count:
        keyer = lambda x: len(artists[x])
        albkeyer = lambda x: len(albums[x])
        reverse = True
    else:
        keyer = albkeyer = lambda x: x.lower()
        reverse = False

    acount = 0
    artl = []
    arti = []
    for a in sorted(artists.keys(), key=keyer, reverse=reverse):
        songs = artists[a]
        scount = len(songs)
        aalb = {}
        for song in songs:
            aalb[song.album] = aalb.get(song.album, 0) + 1

        sstr = f'{a} ({scount} songs in {len(aalb)} albums)'
        if scount < min_count:
            pass
        elif details:
            acount += 1
            if unfold:
                artl.append(sstr)
                arti.append(a)
                for s in sorted(aalb.keys(), key=albkeyer, reverse=reverse):
                    artl.append(f'    {s} ({len(albums[s])})')
                    arti.append(None)
            else:
                sstr += ' - ' 
                for s in sorted(aalb.keys(), key=albkeyer, reverse=reverse):
                    sstr += f'{s} ({len(albums[s])}), '
                artl.append(sstr[:-2])
                arti.append(a)
        else:
            acount += 1
            artl.append(sstr)
            arti.append(a)
    print(f'found {acount} artists in {path} ({time_str(ti)})')
    return artl, arti, artists

def list_albums(path, min_count=1, by_count=False, details=False, unfold=False):
    def keyer(i):
        return f'{1000-i[1]}{i[0]}'
    ti = time.perf_counter()

    files = get_files(path, quiet=True)
    artists, albums, genres, filenames = get_tags(files, path)

    if by_count:
        album_list = sorted([(a,len(c), c[0].artist) for a, c in albums.items()
                if len(c) >= min_count], key=keyer)
    else:
        album_list = sorted([(a,len(c), c[0].artist) for a, c in albums.items()
                if len(c) >= min_count], key=lambda x: x[0].lower())

    albl = []
    albi = []
    for a, c, art in album_list:
        s = (f'{a} ({c} songs by {art})')
        if details:
            if unfold:
                albl.append(s)
                albi.append(a)
                for a in sorted(albums[a], key=lambda x: x.title.lower()):
                    albl.append('    '+a.title)
                    albi.append(None)
            else:
                d = ', '.join(sorted([a.title for a in albums[a]], key=lambda x: x.lower()))
                s += f' - {d}'
                albl.append(s)
                albi.append(a)
        else:
            albl.append(s)
            albi.append(a)
    print(f'found {len(album_list)} albums in {path} ({time_str(ti)})')
    return albl, albi, albums

def list_genres(path, min_count=1, by_count=False, details=False, unfold=False):
    def keyer(i):
        return f'{1000-i[1]}{i[0]}'
    ti = time.perf_counter()

    files = get_files(path, quiet=True)
    artists, albums, genres, filenames = get_tags(files, path)

    if by_count:
        gkeyer = lambda x: len(genres[x])
        akeyer = lambda x: gart[x]
        reverse = True
    else:
        gkeyer = akeyer = lambda x: x.lower()
        reverse = False

    gcount = 0
    glist = []
    gindex = []
    for g in sorted(genres.keys(), key=gkeyer, reverse=reverse):
        songs = genres[g]
        scount = len(songs)
        gart = {}
        for song in songs:
            gart[song.artist] = gart.get(song.artist, 0) + 1


        gstr = f'{g} ({scount} songs by {len(gart)} artists)'
        if scount < min_count:
            pass
        elif details:
            gcount += 1
            items = sorted([k for k, v in gart.items() if v >= min_count],
                    key=akeyer, reverse=reverse)
            if unfold:
                glist.append(gstr)
                gindex.append(g)
                for i in items:
                    glist.append(f'    {i} ({gart[i]})')
                    gindex.append(None)
            else:
                gstr += ' - '  
                for i in items:
                    gstr += f'{i} ({gart[i]}), '
                glist.append(gstr[:-2])
                gindex.append(g)
        else:
            gcount += 1
            glist.append(gstr)
            gindex.append(g)
    print(f'found {gcount} genres in {path} ({time_str(ti)})')
    return glist, gindex, genres




def get_files(path, extensions=('.mp3',), subfolders=True, quiet=False):
    'Create image list from given path and file extensions'
    depth = len(path[1:].split(os.sep))
    trim = len(path) if path.endswith(os.sep) else len(path) + 1
    files = []
    extra = []
    folders = []
    print.quiet = quiet

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

    print.quiet = False
    return files, extra, folders

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
    print(f'found {len(files)} MP3s, {len(extra)} other files in {time_str(ti)}')

    return files, folders, extra

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


if __name__ == '__main__':
    main()