#!bin/python
'''
FIX:
Cannot edit tags found in from scan function
TODO:
keyboard scrolling: 
category menu update tags?
Fix Playlist - Remove Clicked

'''
import os, sys, pickle, time, pyperclip, zlib, subprocess, random
import PySimpleGUI as sg
from mutagen.easyid3 import EasyID3 as ID3
from shutil import copy
from io import StringIO

## G L O B A L  V A L U E S
icon = b'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'

main_tips = {
    'Sync to Dest': 'Copy missing MP3s from source folder to chosen destination',
    'Clean Dest': 'Remove any files from destination folder if missing in source folder',
    'Verify Filenames': 'Compare filenames to MP3 tags and detect mangled filenames',
    'Show non-MP3s': 'Show or delete non-MP3 files in source older',
    'Fix Playlist': 'Normalize playlist to use relative paths and remove extra lines',
    'Browser': 'Button for testing my custom file browsr',
    'Artists': 'Display all artists in source folder and edit mislabeled artist tags',
    'Albums': 'Display all albums in source folder and edit mislabeled albums tags',
    'Genres': 'Display all genres in source folder and edit mislabeled genres tags',
    'Editor': 'Show, filter, and edit the tags for all MP3s in source folder',
    'Change Theme': 'Change GUI colors and font size', }
themes = sg.theme_list()
temp_dir = '/tmp'
MAX_HISTORY = 9
MAX_FILES = 50000

def main():
    global tooltips
    options = load_options()    
    tooltips = load_tooltips('README.md')
    window = main_window()
    returned_at = time.perf_counter() - 1

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print.window = window

        if event == sg.WIN_X_EVENT or event == 'Cancel':
            if time.perf_counter() - returned_at > .5: 
                break
        else:
            if event == 'Clear':
                print.buffer = StringIO()
            elif event == "Change Theme":
                window = theme_menu(window)
            elif event == "Sync to Dest":
                sync_menu()
            elif event == 'Clean Dest':
                clean_menu(window)
            elif event == 'Verify Filenames':
                filename_menu(window)
            elif event == "Fix Playlist":
                fix_playlist_menu(window)
            elif event == 'Artists':
                category_menu(window, 'Artists')
            elif event == 'Albums':
                category_menu(window, 'Albums')
            elif event == 'Genres':
                category_menu(window, 'Genres')
            elif event == 'Browser':
                browser('/home/michael')
            elif event == 'Tag Editor':
                tag_editor(window)
            elif event == 'Show non-MP3s':
                extra_menu(window)
            elif event == 'Copy':
                pyperclip.copy(print.buffer.getvalue())
            elif event == '?':
                if os.path.exists('README.md'):
                    subprocess.call(('xdg-open', 'README.md'))
                #help_window(window)
            else:
                print(f'{event}: {values}')
            returned_at = time.perf_counter()
        window["CONSOLE"].update(print.buffer.getvalue())

    print.window = None
    window.close()
    save_options(options)


## W I N D O W S
def main_window(theme='DarkBlack1', size=16):
    maintips = tooltips.get('main', main_tips)
    tools = list(maintips.keys())
    top_row = 6
    opt1 = tools[:top_row]
    opt2 = tools[top_row:]

    theme = options.get('theme', theme)
    font = options.get('font', ('Arial', size))
    sg.set_options(font=font, tooltip_font=font, icon=icon)
    sg.theme(theme)
    layout = [[sg.Button(opt) for opt in opt1] + [
                    sg.Push(), sg.Button('?')],
              [sg.Button(opt) for opt in opt2],
              [sg.Multiline(default_text=print.buffer.getvalue(),enable_events=False,
                    size=(120, 20), expand_x=True, expand_y=True,
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
              [sg.Push(), sg.Text('History:'), sg.Button('Clear'), sg.Button('Copy'),
                    sg.Button('Save')] ]
    window = sg.Window('MP3 Gui', layout, font=options['font'], icon=icon,
            enable_close_attempted_event=True, resizable=True, finalize=True)
    set_tooltips(window, 'main')
    return window

def help_window(parent, filename='README.md'):
    try:
        with open(filename) as f:
            lines = f.readlines()
            text = ''
            for line in lines:
                text += line
    except:
        text = 'README.md not found\n'

    print('Opening help window')
    layout = [[sg.Multiline(text, size=(80, 20))],
              [sg.Push(), sg.Button('Close')]]
    window = sg.Window('MP3 GUI Help', layout, modal=True, finalize=True)
    ev, v = window.read()
    window.close()

def theme_menu(parent, theme=None):
    font, size = options['font']
    if theme:
        sg.theme(theme)
    else:
        print('Changing theme')    

    layout = [[sg.Listbox(values=themes, size=(30,10), key='List',
                    enable_events=True)],
             [sg.Text('Size:'), sg.Slider(default_value=size, range=(6,24),
                    key='size', orientation='h')],
             [sg.Checkbox('Show Tooltips', default=options['tooltips'],
                    key='tooltips')],
             [sg.Push(), sg.Button('Cancel'), sg.Button('Change')]]
 
    window = sg.Window("Theme Chooser", layout, modal=True,
            font=options['font'], finalize=True)
    sg.theme(options.get('theme', ''))

    if theme in themes:
        i = themes.index(theme)
        window['List'].update(set_to_index=[i], scroll_to_index=max(i-3, 0))
    while True:
        event, values = window.read()
        if event == 'Change':
            theme = values.get('List')
            new_size = int(values.get('size', size))
            options['font'] = (font, new_size)
            options['tooltips'] = values['tooltips']
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
        elif event == 'List':
            theme = values['List'][0]
            window.close()
            return theme_menu(parent, theme)
    return parent

def sync_menu(source='', dest=''):
    def update(results):
        nonlocal text_rows
        files, folders, extra = results
        start = econsole.get().count('\n') + 2
        results = check_files(files, extra, source, dest, opts)
        if results:
            window['Copy'].update(disabled=False)
            window['Clip Filenames'].update(disabled=False)
            scanned = True
        t = print.buffer.getvalue()
        text_rows = ['']*start + t.split('\n')[start:]
        window['CONSOLE'].update(t)
        window.Refresh()
        return results

    source = options.get('source', source)
    dest = options.get('dest', dest)
    print('Opening sync menu')
    print.buffer, _buffer = getattr(sync_menu, 'buffer', StringIO()), print.buffer # save a backup
    boxes = ('Missing', 'Different', 'Same', 'Extra', 'Clear', 'CRC')
    checked = dict(Missing=True)
    scanned = False

    layout = [[sg.Text('Source', size=10),
                sg.Combo(options['history'], default_value=source,
                        size=(50,1), enable_events=True ,key='Source'),
                sg.FolderBrowse(initial_folder=source), sg.Push(), sg.Button('Swap')],
            [sg.Text('Dest', size=10),
                sg.Combo(options['history'], default_value=dest, size=(50,1),
                        enable_events=True ,key='Dest'),
                sg.FolderBrowse(initial_folder=dest)],
            [sg.Checkbox(box, key=box, enable_events=True,
                    default=checked.get(box, False)) for box in boxes],
            [sg.Multiline(enable_events=False, size=(100, 15), expand_x=True, expand_y=True,
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
            [sg.Button('Clip Filenames', disabled=True), sg.Push(), sg.Button('Cancel'), 
                    sg.Button('Scan'), sg.Button('Copy', disabled=True)] ]
    
    window = sg.Window('Sync Files', layout, modal=True, finalize=True,
            return_keyboard_events=True, resizable=True)
    set_tooltips(window, 'Sync to Dest')
    window['CONSOLE'].update(print.buffer.getvalue())
    econsole = window['CONSOLE']
    scroller = get_scroller(econsole)
    text_rows = []
    results = False
    while True:
        print.window = window
        event, values = window.read()
        values = values or {}
        opts = {k:values.get(k, False) for k in boxes}
        source = values.get('Source', source)
        dest = values.get('Dest', dest)

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
                update_history(window, source, dest)
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
        elif event == 'Swap':
            source, dest = dest, source
            window['Source'].update(source)
            window['Dest'].update(dest)
        elif event in boxes and results:
            print.buffer = StringIO()
            final_results = update(results)
            if not final_results:
                window['Copy'].update(disabled=True)
                window['Clip Filenames'].update(disabled=True)
        elif event[1] == ':' and window.find_element_with_focus() == econsole:
            scroller(event[0], text_rows)

    sync_menu.buffer, print.buffer = print.buffer, _buffer 
    print.window = None

def clean_menu(source='', dest=''):
    def update(source, dest, opts):
        extras = find_unexpected(source, dest, opts)
        window['List'].update(values=extras or ['Nothing found'])
        if extras:
            window['Clip Filenames'].update(disabled=False)
            window['Remove'].update(disabled=False)
        else:
            window['Clip Filenames'].update(disabled=True)
            window['Remove'].update(disabled=True)
        window['SBUT'].InitialFolder=source
        window['DBUT'].InitialFolder=dest
        return extras

    source = options.get('source', source)
    dest = options.get('dest', dest)
    print('Opening clean menu')
    boxes = ('MP3s', 'Other')
    checked = dict(MP3s=True, Other=False)

    layout = [[sg.Text('Source', size=10),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True ,key='Source', bind_return_key=True),
                sg.FolderBrowse(initial_folder=source, key="SBUT"),
                sg.Push(), sg.Button('Swap')],
            [sg.Text('Dest', size=10),
                sg.Combo(options['history'], default_value=dest, size=(50,1),
                        enable_events=True ,key='Dest', bind_return_key=True),
                sg.FolderBrowse(initial_folder=dest, key='DBUT')],
            [sg.Checkbox(box, key=box, enable_events=True,
                    default=checked.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning'], size=(100, 15), expand_x=True, expand_y=True,
                    key="List", enable_events=True)],
            [sg.Button('Clip Filenames', disabled=True), sg.Push(), sg.Button('Cancel'), 
                    sg.Button('Remove', disabled=True)] ]
    
    window = sg.Window('Clean Destination Folder', layout, modal=True,
            resizable=True, finalize=True)
    set_tooltips(window, 'Clean Dest')

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
            window['Source'].update(source)
            window['Dest'].update(dest)
            extras = update(source, dest, opts)
        elif event in boxes:
            extras = update(source, dest, opts)
        elif event == 'Source':
            nsource = values['Source']
            if comp_dir(source, nsource, True):
                source = nsource
                extras = update(source, dest, opts)
                update_history(window, source)
        elif event == 'Dest':
            ndest = values['Dest']
            if comp_dir(dest, ndest, True):
                dest = ndest
                extras = update(source, dest, opts)
                update_history(window, dest=dest)
        elif event == 'List':
            item = values[event][0]
            if item in extras:
                i = extras.index(item)
                extras.remove(item)
                window['List'].update(values=extras or ['Nothing found'],
                        scroll_to_index=max(i-2, 0))
        else:
            print(f'{event} {values}')

# NOT USED
def verify_menu(window):
    source = options['source']
    print('Opening filename menu')
    boxes = ('MP3s', 'Other')

    layout = [[sg.Text('Source', size=10),
                sg.Combo(options['history'], default_value=source,
                        size=(50,1), enable_events=True ,key='Source'),
                sg.FolderBrowse(initial_folder=source, key="SBUT")],
            [sg.Listbox(['Nothing Scanned'], size=(100, 15),
                    key="List")],
            [sg.Push(), sg.Button('Copy'), sg.Button('Scan'), sg.Button('Close')] ]
    
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
            window['Source'].update(source)
            window['Dest'].update(dest)
            extras = update(source, dest, opts)
        elif event in boxes:
            extras = update(source, dest, opts)
        elif event == 'Scan':
            source = values['Source']
            files = get_files(source, quiet=True)[0]
            items = check_filenames(files)
            window['List'].update(values=items)
            update_history(window, source)

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
    boxes = ['Sort by Count', 'Extra Details', 'Unfold Details', 'Play on Click']
    checked = {'Sort by Count':False, 'Extra Details': True}
    opts = [checked.get(k, False) for k in boxes]
    title, list_items, min_count = set_mode(mode)

    layout = [[sg.Text('Source', size=15),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True ,key='Source', bind_return_key=True),
                sg.FolderBrowse(initial_folder=source, key="SBUT"),
                sg.Push(), sg.Combo(modes, default_value=mode, readonly=True,
                    enable_events=True, key='MODE')],
            [sg.Text('Export Subfolder', size=15), sg.In(mode, size=(51,1),
                    key='Export Subfolder')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=checked.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning...'], size=(100, 15), enable_events=True,
                    key="List", horizontal_scroll=True, expand_x=True, expand_y=True)],
            [sg.Text('Minimum Count'), sg.Input(min_count, size=5,
                    enable_events=True, key='Minimum Count'),
                sg.Push(), sg.Button('Make Playlists'),
                sg.Button('Copy'), sg.Button('Close')] ]
    
    window = sg.Window(title, layout, modal=True, finalize=True, resizable=True)
    set_tooltips(window, mode)
    items, indexes, songs = list_items(source, min_count, rescan=False, *opts[:-1])
    window['List'].update(items)
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
        elif event == 'Make Playlists':
            make_playlists(songs, mode, source, min_count, values['Export Subfolder'])
        elif event in boxes:
            if event=='Unfold Details' and values.get('Unfold Details', False):
                window['Extra Details'].update(True)
            elif event=='Extra Details' and not values.get('Extra Details', False):
                window['Unfold Details'].update(False)
            opts = [values.get(k, False) for k in boxes]
            items, indexes, songs = list_items(source, min_count, *opts[:-1])
            window['List'].update(values=items)
        elif event == 'Minimum Count':
            try:
                min_count = int(values['Minimum Count'])
            except:
                continue
            items, indexes, songs = list_items(source, min_count, *opts[:-1])
            window['List'].update(values=items)
        elif event == 'Source':
            nsource = values['Source']
            if comp_dir(source, nsource, True):
                source = nsource
                update_history(window, source)
                items, indexes, songs = list_items(source, min_count, *opts[:-1])
                window['List'].update(values=items)
        elif event == 'MODE':
            new_mode = values['MODE']
            title, list_items, min_count = set_mode(new_mode)
            items, indexes, songs = list_items(source, min_count, *opts[:-1])
            window['List'].update(items)
            window['Minimum Count'].update(min_count)
            old = window['Export Subfolder'].get()
            window['Export Subfolder'].update(old.replace(mode, new_mode))
            mode = new_mode
            window.set_title(title)
            set_tooltips(window, mode)
        elif event == 'List':
            selected = window['List'].GetIndexes()[0]
            key = indexes[selected]

            # P L A Y  O N  C L I C K  I S  S E L E C T E D
            if opts[-1]: 
                l = [os.path.join(source, s.filename) for s in songs[key]]
                play_songs(l, True)
                continue

            if indexes[selected]:
                value = sg.popup_get_text('', title='Change Value', default_text=key)
                if value and value != key:
                    attr = mode.lower()[:-1] # exp: Artists -> artist
                    print(f'Changing {attr} from {key} to {value}')
                    for song in songs[key]:
                        fn = os.path.join(source, song.filename)
                        tag = ID3(fn)
                        tag[attr] = value
                        tag.save()
                    items[selected] = items[selected].replace(key, value, 1)
                    window['List'].update(items, set_to_index=[selected],
                            scroll_to_index=max(selected-3, 0))

def extra_menu(parent):
    def get_extras(path):
        files, extras, folders = get_files(path, quiet=True)
        return sorted(extras, key=lambda x:x.lower())

    source = options['source']
    boxes = ['Filter Same Folder', 'Filter Same Extensions']
    opts = {k :False for k in boxes}
    print('Showing non-MP3 files')

    layout = [[sg.Text('Source', size=15),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True, key='Source', bind_return_key=True),
                sg.FolderBrowse(initial_folder=source, key="SBUT")],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning...'], size=(100, 15), enable_events=True,
                    key="List", expand_x=True, expand_y=True)],
            [sg.Button('Clip Filenames'), sg.Push(), sg.Button('Reset'),
                    sg.Button('Remove'), sg.Button('Close')] ]
    window = sg.Window('Extra File Browser', layout, modal=True,
            resizable=True, finalize=True)
    set_tooltips(window, 'Show non-MP3s')
    files = get_extras(source)
    window['List'].update(files)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in boxes:
            if values[event]:
                for i in boxes:
                    window[i].update(False)
                    opts[i] = False
                window[event].update(True)
            opts = {k :window[k].get() for k in boxes}
        elif event == 'List':
            item = values[event][0]
            remove_extras(files, item, opts, window)
        elif event == 'Source':
            if os.path.isdir(values[event]):
                source = os.path.normpath(values[event])
                update_history(window, source)
                files = get_extras(source)
                window['List'].update(files)
        elif event == 'Clip Filenames':
            if files:
                pyperclip.copy('\n'.join(files))
        elif event == 'Reset':
            files = get_extras(source)
            window['List'].update(files)
        elif event == 'Remove':
            r = sg.popup_ok_cancel(f'Delete {len(files)} files from {source}?', title='Delete')
            if r == 'OK':
                for f in files:
                    os.remove(os.path.join(source, f))
                print(f'Deleted {len(files)} files from {source}')
                break
    window.close()

def fix_playlist_menu(parent):
    source = options['source']
    boxes = ['Remove Metadata', 'Remove Missing']
    playlist = None
    opts = {k :False for k in boxes}
    file_types=(('Playlists', '.m3u'),)
    print('Fixing playlists')

    layout = [[sg.Text('Playlist', size=15),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True ,key='Playlist', bind_return_key=True),
                sg.FileBrowse(initial_folder=source, key="SBUT",
                    file_types=file_types)],
            [sg.Text('Strip', size=15), sg.In(size=(51,1), key='Strip')],
            [sg.Text('Prefix', size=15), sg.In(size=(51,1), key='Prefix')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [sg.Listbox(['Load a Playlist'], size=(100, 15), enable_events=True,
                    expand_x=True, expand_y=True, key="List")],
            [sg.Push(), sg.Button('Save', disabled=True),
                    sg.Button('Show', disabled=True), sg.Button('Close')] ]
    window = sg.Window('Playlist Fixer', layout, modal=True,
            resizable=True, finalize=True)
    set_tooltips(window, 'Fix Playlist')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in boxes:
            opts = {box: values[box] for box in boxes}
            if playlist:
                files, strip, prefix = scan_playlist(playlist, opts, window)
        elif event == 'List':
            item = values[event][0]
        elif event == 'Playlist':
            nsource = values[event]
            if os.path.isfile(nsource):
                playlist = values[event]
                source = os.path.split(nsource)[0]
                files, strip, prefix = scan_playlist(playlist, opts, window)
            elif os.path.isdir(nsource):
                source = nsource
                update_history(window, source)
                window['List'].update(['Load a Playlist'])
                window['Show'].update('Show', disabled=True)
                window['SBUT'].InitialFolder = source
        elif event == 'Show':
            if window[event].get_text() == 'Show':
                prefix = window['Prefix'].get()
                window['Show'].update('Reset')
                l = len(values['Strip'])
                outp = [prefix+f[l:] for f in files if f[0]!='#']
                window['List'].update(outp)
            else:
                window['Show'].update('Show')
                window['List'].update(files)
        elif event == 'Save':
            p = os.path.split(window['Playlist'].get())[0]
            path = p if os.path.isdir(p) else options['Export Subfolder']
            prefix = window['Prefix'].get()
            l = len(values['Strip'])
            fn = sg.popup_get_file('Save Playlist', save_as=True,
                    default_path=path, default_extension='.m3u',
                    file_types=file_types)
            if os.path.isdir(fn) or not os.path.isdir(os.path.split(fn)[0]):
                print('invalid path to save playlist')
                continue
            with open(fn, 'w') as outp:
                for f in files:
                    if f[0] != '#':
                        f = prefix+f[l:]
                    _print(f, file=outp)
    window.close()
def filename_menu(parent):
    source = options['source']
    boxes = ['Ignore Folders']
    opts = {k :False for k in boxes}
    print('Checking Filenames')
    match = options['pattern']
    wrong = compared = None


    layout = [[sg.Text('Source', size=15),
                sg.Combo(options['history'], default_value=source,
                        size=(50,1), key='Source'),
                sg.FileBrowse(initial_folder=source, key="SBUT",)],
            [sg.Text('Match', size=15), sg.In(match, size=(51,1), key='Match')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [sg.Listbox(['Nothing Scanned'], size=(100, 15), enable_events=True,
                    key="List", expand_x=True, expand_y=True)],
            [sg.Button('Clip Filenames', disabled=True), sg.Push(),
                    sg.Button('Scan'), sg.Button('Compare'), sg.Button('Close')] ]
    window = sg.Window('Verify Filenames', layout, modal=True,
            resizable=True, finalize=True)
    set_tooltips(window, 'Verify Filenames')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in boxes:
            opts = {box: values[box] for box in boxes}
        elif event == 'List':
            if not compared: continue
            item = values[event][0]
            expected = item.split(' || ')[1]
            i = window[event].get_indexes()[0]
            seltags = tags[indexes[i]]
            m = edit_file(seltags, source, match)
            if m == seltags.filename:
                wrong.pop(i); indexes.pop(i)
            else:
                wrong[i] = f'{seltags.filename} || {m}'
                indexes[i] = seltags.filename
            window['List'].update(wrong, scroll_to_index=i-2)
        elif event == 'Clip Filenames':
            pyperclip.copy('\n'.join(wrong))
        elif event == 'Scan':
            source = values['Source']
            files = get_files(source, quiet=True)[0]
            wrong = check_filenames(files)
            window['List'].update(values=wrong)
            update_history(window, source)
            compared = False
            window['Clip Filenames'].update(disabled=False)
        elif event == 'Compare':
            if os.path.isdir(values['Source']):
                source = values['Source']
                update_history(window, source)
            else:
                window['Source'].update(source)
                continue
            match = options['pattern'] = values['Match']
            wrong, tags, indexes = get_unmatched_filenames(source, match, opts)
            window['List'].update(wrong or ['Nothing Found'])
            window['Clip Filenames'].update(disabled=False)
            compared = True  

    window.close()

def edit_file(tags, dest, match='', multi=False):
    def get_match_str(tags, match):
        return match.format(
            title=tags.title,
            artist=tags.artist,
            album=tags.album,
            genre=tags.genre)

    size = 8, 60
    orig, tags = tags, tags.copy()
    if multi:
        tags.clear()
    if match:
        match = match if match and match.endswith('.mp3') else match + '.mp3'
    expected = get_match_str(tags, match)
    if match:
        layout = [[sg.Text('Expected', size=size[0], key='MTEXT'), sg.Text(expected, key='Match')]]
    else:
        layout = [[]]

    items = ('Filename', 'Title', 'Artist', 'Album', 'Genre')
    layout += [ [sg.Text(i, size=size[0]), sg.In(getattr(tags, i.lower()), size=size[1],
                key=i, enable_events=True)] for i in items]
    if match:
        layout += [[sg.Button('Rename'), sg.Button('Re-tag')],
                   [sg.Push(), sg.Button('Cancel'), sg.Button('Save')]]
    else:
        layout += [[sg.Push(), sg.Button('Cancel'), sg.Button('Save')]]

    window = sg.Window('Edit Song Details', layout, modal=True)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            return
        elif event == 'Save':
            if multi:
                window.close()
                return tags
            update_tags(orig, tags, dest)
            break
        elif event == 'Rename':
            tags.filename = get_match_str(tags, match)
            window['Filename'].update(tags.filename)
        elif event == 'Re-tag':
            tags_from_fn(match, tags.filename, tags, window)
            
        elif event in items:
            tags.__setattr__(event.lower(), values[event])
            if match:
                m = get_match_str(tags, match)
                window['Match'].update(m)
                if m == tags.filename:
                    window['MTEXT'].update('Match')
                else:
                    window['MTEXT'].update('Expected')
   
    window.close()
    return get_match_str(tags, match)

def tag_editor(parent):
    sort_column = 0; clicked=None
    source = options['source']
    boxes = ('Case Sensitive', 'Play Songs')
    opts = {k: False for k in boxes}
    headings = ('Title', 'Artist', 'Album', 'Genre', 'Filename')
    hsizes = [20, 20, 20, 10, 30]
    hsized = dict(zip(headings, hsizes))
    table = [ ['' for _ in headings]] * 2
    table_layout = sg.Table(values=table, headings=headings,
            col_widths=hsizes,
            auto_size_columns=False,
            display_row_numbers=False,
            justification='left',
            key='Table',
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True)

    layout = [[sg.Text('Source', size=12),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                bind_return_key=True, key='Source'),
                sg.FolderBrowse(initial_folder=source, key="SBUT",), sg.Button('Scan')],
            [sg.Text('Filter', size=12), sg.In(size=(51,1), key='Filter'),
                sg.Combo(('Any',)+headings, default_value='Any', readonly=True,
                        enable_events=True, key='Key'),
                sg.Button('Include'), sg.Button('Exclude'), sg.Button('Reset')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [table_layout],
            [sg.Button('Play Song'), sg.Push(), sg.Button('Multi Edit'),
                sg.Button('Close')] ]

    window = sg.Window('Tag Editor', layout, modal=True,finalize=True,
            resizable=True, return_keyboard_events=True)
    set_tooltips(window, 'Tag Editor')
    window['Source'].bind("<Return>", "_ENTER")
    window['Filter'].bind("<Return>", "_ENTER")
    etable = window['Table']
    scroller = get_scroller(window['Table'])

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in ('Scan', 'Reset', 'Source_ENTER'):
            nsource = values['Source']
            if os.path.isdir(nsource):
                source = nsource
                update_history(window, source)
                table, tags = make_tag_table(source, event=='Reset')
                sort_column = 0
                window['Table'].update(table)
            else:
                window['Source'].update(source)
        elif event in ('Include', 'Filter_ENTER'):
            table = filter_tag_table(values['Filter'], table,
                    window['Key'].get(), headings, opts)
            window['Filter'].update('')
            window['Table'].update(table)
        elif event == 'Exclude':
            table = filter_tag_table(values['Filter'], table,
                    window['Key'].get(), headings, opts, True)
            window['Filter'].update('')
            window['Table'].update(table)
        elif event == 'Multi Edit':
            selected = values['Table']
            if selected:
                t = table[selected[0]][-1]
                t = edit_file(tags[t], source, multi=True)
                t.filename = ''
                update_multi_tags(table, selected, tags, t, source)
                window['Table'].update(table)

        elif event == 'Play Song':
            selected = values['Table']
            if len(selected) > 1:
                play_songs([os.path.join(source,table[row][-1]) for row in selected])
            elif clicked != None:
                fn = os.path.join(source, table[clicked[0]][-1])
                subprocess.call(('xdg-open', fn))
            
        elif event in boxes:
            opts[event] = values[event]

        # HANDLE Table CLICKS
        elif isinstance(event, tuple) and event[0] == 'Table':
            selected = values['Table']
            clicked = event[2]
            if len(selected) == 1 and selected[0] == clicked[0]:
                # DOUBLE CLICKED TO EDIT
                if opts['Play Songs']:
                    fn = os.path.join(source, table[clicked[0]][-1])
                    subprocess.call(('xdg-open', fn))
                else:
                    row = table[clicked[0]]
                    fn = row[-1]
                    seltags = tags[fn]
                    edit_file(seltags, source)
                    table[clicked[0]] = seltags.as_row()
                    window['Table'].update(table)
            elif clicked[0] == -1:
                sort_column = clicked[1]
                table = sort_table(table, sort_column)
                window['Table'].update(table)
            else:
                pass
                #print(f'Table clicked at {clicked}')
        elif event == 'Table':
            pass
        elif event[1] == ':' and window.find_element_with_focus() == etable:
            scroller(event[0], table, sort_column)
    window.close()

def update_multi_tags(table, rows, tag_list, settags, source):
    for row in rows:
        otags = tag_list[table[row][-1]]
        copy = otags.copy()
        copy.update(settags)
        update_tags(otags, copy, source)
        table[row] = copy.as_row()

def get_scroller(element):
    def scroll_to_index(key, data, col=None):
        nonlocal last_press, keys_pressed
        if not data:
            return
        c = key.lower()
        ti = time.perf_counter()
        if ti - last_press < Key_DELAY:
            keys_pressed += c
        else:
            keys_pressed = c
        last_press = ti
        if col == None:
            for i, item in enumerate(data):
                if keys_pressed < item.lower():
                    break
        else:
            for i, row in enumerate(data):
                if keys_pressed < row[col].lower():
                    break
        perc = i / len(data)
        element.set_vscroll_position(perc)
        if isinstance(element, sg.Table):
            element.update(select_rows=[i])
    Key_DELAY = 1
    keys_pressed = ''
    last_press = 0
    return scroll_to_index


def row_to_tags(row):
    pass


def make_tag_table(path, reset=False):
    if reset and hasattr(make_tag_table, 'files'):
        files = make_tag_table.files
    else:
        files = make_tag_table.files = get_files(path, quiet=True)[0]
    tags = get_tags(files, path)[-1]
    table = []
    for song in tags.values():
        row = song.as_row()
        table.append(row)
    return sort_table(table), tags

def filter_tag_table(text, table, key, headings, opts, exclude=False):
    case = lambda x: x
    if not opts.get('Case Sensitive'):
        text = text.lower()
        case = lambda x: x.lower()        
    if key in headings:
        i = headings.index(key)
        if exlude:
            table = [ r for r in table if text not in case(r[i])]
        else:
            table = [ r for r in table if text in case(r[i])]
    else:
        if exclude:
            table = [ r for r in table if text not in case(''.join(r))]
        else:
            table = [ r for r in table if text in case(''.join(r))]
    return table



def sort_table(table, col=0):
    return sorted(table, key=lambda x: x[col])



def browser(path, types=None):
    PATH_LENGTH = 60
    BOX_HEIGHT = 15
    def get_listing(path, window=None):
        folders = []; files = []
        path = os.path.normpath(path)
        for f in sorted(os.listdir(path), key=lambda x:x.lower()):
            p = os.path.join(path, f)
            if os.path.isdir(p):
                folders.append('/'+f)
            else:
                files.append(f)

        p = path
        parents = [path[-PATH_LENGTH:]]
        while True:
            p = os.path.normpath(os.path.join(p, '..'))
            parents.append(p[-PATH_LENGTH:])
            if p == os.path.sep:
                break
        items = folders+files
        if window != None:
            window['List'].update(items)
            window['PARENTS'].update(parents[0] or '/', values=parents[1:])
        return items, parents

    items, parents = get_listing(path)
    layout = [[sg.Combo(parents[1:], size=PATH_LENGTH,
                    default_value=parents[0], key='PARENTS',
                    enable_events=True, bind_return_key=True),
                sg.Push(), sg.Button('^', key='UP')],
            [sg.Listbox(items, size = (PATH_LENGTH+5, BOX_HEIGHT), key='List', enable_events=True)],
            [sg.Push(), sg.Button('Cancel'), sg.Button('Okay')]]
    window = sg.Window('File Chooser', layout, modal=True)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'UP':
            path = os.path.normpath(os.path.join(path, '..'))
            items, parents = get_listing(path, window)
        elif event == 'PARENTS':
            v = values[event]
            if v in parents:
                index = parents.index(v)
                for _ in range(index):
                    path = os.path.normpath(os.path.join(path, '..'))
            elif os.path.isdir(v):
                path = v
            else:
                path = path
            items, parents = get_listing(path, window)
        elif event == 'List':
            clicked = values[event][0]
            if clicked.startswith('/'):
                p = os.path.join(path, values[event][0][1:])
                if os.path.isdir(p):
                    path = p
                    items, parents = get_listing(path, window)

    window.close()


## U T I L I T Y  F U N C T I O N S
def check_CRC(f1, f2):
    if get_CRC(f1) == get_CRC(f2):
        return True

def comp_dir(d1, d2, check_exist=False):
    d1 = os.path.normpath(d1)
    d2 = os.path.normpath(d2)
    r = d1 == d2 or (d1 == '/' or d2 == '/')
    exists = os.path.isdir(d1) and os.path.isdir(d2)
    #print(f'1: {d1}, 2: {d2}, equal: {r}, exists: {exists}')
    return exists and not r

def get_CRC(fpath):
    """With for loop and buffer."""
    crc = 0
    with open(fpath, 'rb', 65536) as ins:
        for x in range(int((os.stat(fpath).st_size / 65536)) + 1):
            crc = zlib.crc32(ins.read(65536), crc)
    return '%08X' % (crc & 0xFFFFFFFF)

def load_options(path=None):
    global options
    if not path:
        path = os.getcwd()
    fn = os.path.join(path, 'options.cfg')
    try:
        with open(fn, 'rb') as file:
            options = pickle.load(file)
        print(f'Options loaded from {fn}')
        load_options.options = options.copy()
    except:
        load_options.options = None
        user = os.path.expanduser('~')
        music = os.path.join(user, 'Music')
        source = music if os.path.exists(music) else user 
        options = dict(
            theme = 'default1',
            source = source,
            dest = os.path.join(user, 'output'),
            font = ('Arial', 14),
            pattern = '{genre}/{artist} - {title}',
            tooltips = True,
            history = [source])
        print('Failed to load options: setting default')
    print(f'  {options}')
    if options.get('theme', None) in themes:
        sg.theme(options['theme'])
    return options

_print = print
def print(*args, **kargs):
    if print.quiet:
        return
    _print(*args, **kargs)
    _print(*args, file=print.buffer, **kargs)
    if print.window:
        try:
            print.window['CONSOLE'].update(print.buffer.getvalue())
            print.window.Refresh()
        except:
            pass
print.buffer = StringIO()
print.window = None
print.quiet = False

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

def update_history(window, source=None, dest=None):
    history = options['history']
    if source:
        source = os.path.normpath(source)
        if source in history:
            history.remove(source)
        history.insert(0, source)
        history = history[:MAX_HISTORY]
        options['source'] = source
        e = window.Find('Source', True)
        if e: window['Source'].update(source, history)
    if dest:
        dest = os.path.normpath(dest)
        if dest in history:
            history.remove(dest)
        history.insert(0, dest)
        history = history[:MAX_HISTORY]
        options['dest'] = dest
        e = window.Find('Dest', True)
        if e: window['Dest'].update(dest, history)

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
            msg += 'misspaced,'
        if msg:
            items.append(f"{file} ({msg.strip(',')})")
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
    print.window = None
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
            if total > MAX_FILES:
                raise Exception(f'Exceeded file limit of {MAX_FILES}: {total}')
    else:
        for f in os.listdir(path):
            if os.path.splitext(f)[-1].lower() in extensions:
                files.append(os.path.join(path, f))
                total += 1

    print.quiet = False
    return files, extra, folders

def get_tags(files, path, rescan=False):
    class SongTag:
        __slots__ = ('filename', 'title', 'artist', 'album', 'genre')
        def __init__(self, filename, title, artist, album, genre):
            self.filename = filename
            self.title = title
            self.artist = artist
            self.album = album
            self.genre = genre
        def as_row(self, folders=True):
            fn = self.filename if folders else os.path.split(self.filename)[1]
            return [self.title, self.artist, self.album,
                    self.genre, fn]
        def clear(self):
            self.__init__('','','','','')
        def copy(self):
            return SongTag(self.filename, self.title, self.artist,
                    self.album, self.genre)
        def update(self, other):
            self.filename = other.filename or self.filename
            self.title = other.title or self.title
            self.artist = other.artist or self.artist
            self.album = other.album or self.album
            self.genre = other.genre or self.genre
            
        def __repr__(self):
            return f'SongTags ({self.title}, {self.artist}, ' \
                    f'{self.album}, {self.genre})'
        def __hash__(self):
                return hash(self.filename)
        def __getitem__(self, key):
            if key in self.__slots__:
                return getattr(self, key)
        def __setitem__(self, key, value):
            if key in self.__slots__:
                setattr(self, key, value)
        def __eq__(self, other):
            if isinstance(other, SongTag):
                if (self.filename==other.filename and
                    self.title==other.title and self.artist==other.artist
                    and self.album==other.album and self.genre==other.genre):
                        return True
            return False

    if not hasattr(get_tags, 'history'):
        get_tags.last_path = path
        get_tags.history = {}

    path = os.path.normpath(path)    
    loaded = get_tags.history.get(path, None)
    if loaded and not rescan:
        #print(f'Loaded tag information for {path}')
        return loaded

    ti = time.perf_counter()
    filenames = {}; artists = {}; albums = {}; genres = {}
    for f in files:
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
    get_tags.last_path = path
    return get_tags.history[path]

def get_unmatched_filenames(source, match, opts):
    files = get_files(source, quiet=True)[0]
    artists, albums, genres, filenames = get_tags(files, source, True)
    if not match.endswith('.mp3'):
        match += '.mp3'

    ti = time.perf_counter()
    total = len(files)
    wrong = []
    indexes = []
    for i, fn in enumerate(files):
        f = os.path.split(fn)[1] if opts['Ignore Folders'] else fn
        m = match.format(
            title=filenames[fn].title,
            artist=filenames[fn].artist,
            album=filenames[fn].album,
            genre=filenames[fn].genre)
        if f != m:
            wrong.append(f'{f} || {m}')
            indexes.append(fn)
    print(f'Compared {total} files in {source} ({time_str(ti)})')
    return wrong, filenames, indexes

def update_tags(otags, ntags, dest):
    try:
        dicts = dict(zip( ('artist', 'album', 'genre'), 
                get_tags.history[get_tags.last_path]))
        filenames = get_tags.history[get_tags.last_path][3]
    except:
        print('Failed loading tag history')
        return

    for t in dicts.keys():
        # get old artists/albums/genres dict
        d = dicts.get(t, {})
        l = d.get(otags[t], [])
        # and remove the old tag reference
        if otags in l:
            _print(f'{otags} removed from {t}')
            l.remove(otags)
        # get the list to match new tags to artist/album/genre dict
        l = d.get(ntags[t], [])
        l.append(otags)
        d[ntags[t]] = l
    # remove old and add new reference to tags in filename dict
    filenames.pop(otags.filename)
    filenames[ntags.filename] = otags

    outtag = ID3(os.path.join(dest, otags.filename))
    for t in ('title', 'artist', 'album', 'genre'):
        outtag[t] = ntags[t]
    outtag.save()
    if otags.filename != ntags.filename:
        os.rename(os.path.join(dest, otags.filename),
                  os.path.join(dest,ntags.filename) )

    otags.update(ntags)


def list_artists(path, min_count=1, by_count=False, details=False, unfold=False, rescan=False):
    ti = time.perf_counter()

    files = get_files(path, quiet=True)[0]
    artists, albums, genres, filenames = get_tags(files, path, rescan)

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

def list_albums(path, min_count=1, by_count=False, details=False, unfold=False, rescan=False):
    def keyer(i):
        return f'{1000-i[1]}{i[0]}'
    ti = time.perf_counter()

    files = get_files(path, quiet=True)[0]
    artists, albums, genres, filenames = get_tags(files, path, rescan)

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

def list_genres(path, min_count=1, by_count=False, details=False, unfold=False, rescan=False):
    def keyer(i):
        return f'{1000-i[1]}{i[0]}'
    ti = time.perf_counter()

    files = get_files(path, quiet=True)[0]
    artists, albums, genres, filenames = get_tags(files, path, rescan)

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

def make_playlists(data, mode, dest, min_count, subfolder):
    mode = mode[0].upper() + mode[1:]
    where = os.path.join(dest, subfolder or mode)
    if os.path.isfile(where):
        sg.popup_error(f'Dest {where} is a file. Aborting.', title='Error')
        return
    elif os.path.isdir(where):
        if sg.popup_ok_cancel(f"Dest '{dest}' already exists. New playlists " 
                'will overide existing files.', title='Confirm') != 'OK':
            return
    else:
        os.makedirs(where)

    prefix = '../' * max(subfolder.count(os.sep)+1, 1)
    print(f'Making playlists for {mode} with {min_count} or more songs')
    print(f'Outputting to {where}')
    count = 0

    for item, songs in data.items():
        if len(songs) >= min_count:
            #print(f'  {item}')
            count += 1
            outf = os.path.join(where, item+'.m3u')
            with open(outf, 'w') as file:
                for s in songs:
                    _print(prefix+s.filename,file=file)
    if count:
        print(f'{count} playlists created')
    else:
        print('None found')

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

def play_songs(songs, shuffle=False):
    if not hasattr(play_songs, 'player'):
        try:
            r = subprocess.run(('xdg-mime', 'query', 'default', 'audio/mpeg'),
                    capture_output=True).stdout.decode()
            play_songs.player = r.split('.')[0]
        except:
            play_songs.player = None
    try:
        [s for s in songs]
    except:
        songs = [songs]
    if shuffle:
        random.shuffle(songs)
    if play_songs.player:
        subprocess.Popen([play_songs.player] + songs,
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    

def remove_extras(files, clicked, opts, window):
    sel = files.index(clicked)
    if opts['Filter Same Folder']:
        folder = os.path.split(clicked)[0]
        for i, f in enumerate(reversed(files)):
            if os.path.split(f)[0] == folder:
                sel = i
                files.remove(f)
        sel = len(files) - sel
    elif opts['Filter Same Extensions']:
        ext = os.path.splitext(clicked)[1]
        for i, f in enumerate(reversed(files)):
            if os.path.splitext(f)[1] == ext:
                sel = i
                files.remove(f)
        sel = len(files) - sel
    elif clicked in files:
        files.remove(clicked)
    window['List'].update(values=files or ['Nothing found'],
            scroll_to_index=max(sel-2, 0))


def scan_playlist(source, opts, window):
    try:
        file = open(source)
        lines = file.readlines()
        file.close()
    except:
        files = []
        print(f'Failed to open playlist: {source}')
    print(f'Scanning playlist: {source}')
    print(opts)

    files = [f.strip('\n') for f in lines if f[0] != '#']
    if opts['Remove Metadata']:
        lines = files
    else:
        lines = [f.strip('\n') for f in lines]
    if opts['Remove Missing']:
        lines = [f for f in lines if f[0]=='#' or os.path.isfile(f)]

    strip = os.path.commonpath(files) + os.sep
    prefix = '../'
    window['List'].update(lines)
    window['Strip'].update(strip)
    window['Prefix'].update(prefix)
    window['Save'].update(disabled=False)
    window['Show'].update(disabled=False)
    return lines, strip, prefix

def tags_from_fn(match, text, tags, window):
    parts = []; d = {}
    items = match.split('{')
    if not items: return
    for s in items:
        r = s.split('}')
        if len(r) > 1:
            key, token, *_ = r
            parts.append((key, token))
    for key, token in parts:
        if token:
            r = text.split(token, 1)
            if not r or len(r) != 2: return
            item, text = r
        else:
            item = text
        d[key] = item
    if len(parts) == len(d):
        for k, v in d.items():
            tags.__setattr__(k, v)
            window[k[0].upper()+k[1:]].update(v)

def load_tooltips(filename):
    try:
        with open(filename) as f:
            data = f.readlines()
    except:
        return {}
    tools = {'main': {}}
    tool = ''

    for l in data:
        l=l.strip()

        if l.startswith('## '):
            tool = l[3:].strip()
            tools[tool] = {}
        elif l.startswith('- '):
            try:
                item, value = l[2:].split(' - ')
                tools[tool][item] = value
            except:
                continue
        elif l.startswith('**') and not tool:
            try:
                k, v = l.split(' - ')
                tools['main'][k.strip('*')] = v
            except:
                continue
    return tools
    
def set_tooltips(window, name):
    found=[]; missed=[]
    if options['tooltips']:
        tips = tooltips[name]
        for e in window.key_dict:
            if e in tooltips[name]:
                window[e].set_tooltip(tips[e])
                found.append(e)
            else:
                missed.append(e)

def print_dict(d, info='dictionary'):
    _print(f'\n{info}')
    for i in d:
        _print(f'{i}: {d[i]}')

if __name__ == '__main__':
    main()