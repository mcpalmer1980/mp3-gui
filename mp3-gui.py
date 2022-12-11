#!bin/python
'''
TODO:
multi edit
keyboard skipping in sync_menu
category menu update tags?
tooltips

'''
import os, sys, pickle, time, pyperclip, zlib, textwrap
import PySimpleGUI as sg
from mutagen.easyid3 import EasyID3 as ID3
from shutil import copy
from io import StringIO
import operator

## G L O B A L  V A L U E S
icon = b'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bXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjI2NDMwZTc4LWQ2YjYtNDk3Mi1iMDMyLThlYWVmMTQ4ZGZmOSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDozYjBjNjJkYi00MWNhLTQyNTYtOWNiNi0xZjg4MzhlMWQyZGIiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpjNjZmNzNhMS00ZTQzLTRkNTktODVjNy1jZmY5NThiY2U2ZmEiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJMaW51eCIKICAgR0lNUDpUaW1lU3RhbXA9IjE2NzAxNTg4OTk1NDA2NTciCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zMiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjI6MTI6MDRUMDg6MDE6MzctMDU6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDIyOjEyOjA0VDA4OjAxOjM3LTA1OjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6YjE3OTIyMmMtYjJjOC00NDNjLWFlOGUtODY0NTgwMTJmNmJjIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKExpbnV4KSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyMi0xMi0wNFQwODowMTozOS0wNTowMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4Y6lR8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAB3RJTUUH5gwEDQEn8pI/EAAABg1JREFUeNrt3T1y4zoQhVFBpVjesQPv2N4AJpnAgafGkgAS6HtO1Qvf2CbZH5uSf9qFAXp3DI7SmmMw8Gg6BAZeDAQAQy8EAoDBFwIBwOALgQAYfERAAAw/QiAABh8READDjwgIgOFHBATA8CMCAmD4EQEBMPiIwFauDgG2QBuAE45NQAAMPyIgAIYfEfAaAHhEtAE4qdgEBMDwIwQeAcAjQRk3J2+8t/cv8/OAz4+7g+ARYO8AGPqqIaj9KNAMv8EXgdwI3FxyBp/f3lTqhaDVPFGG3xZgG7ABGHym3GTqRMDbgAhtsEIBmLv+uyg5+lFTANyREAEBMPysG4G9Q3CtcyLA9WcDcPdHBAQAEACwBQiA9R8REAA4LAJ7hEAAIHgbEAAIjoAAQDABgOAtQAAgOAICAIdGYK0QCAAEbwMCwJJ8I5YAgC1AAEAEBABEQABABAQAREAAQAQEYDBvQZESAQGA4AgIAARHQAAgOAICAMEREAAIjoAAQHAEBACCIyAAEBwBAYDgCAgABEdAACA4AgIAwQQAgrcAAYDgCAgAeAQAErcAAQAbAJC4BQgA2ACAxC1AAMAGAOvx25nnbwECADYAsAUIACAAYAsQAFgqAkIw3s0hYPdt4PPj7sAIAKKwntXjJAAQvLF4DQCCNxYBgOAICAAER0AAIDgCAgDBBAAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAO9uKfBuu94kHxxyZr8teFhwag5vBT17/CnhyGq+FHGO4CYPgRAQEw/CAAYAsQAHd/REAAAAEABAAQAGB7t3M+bBvwb/Tin1ubePy9nstpAWgD/52+6Oe2+sdvCwbhf1+7aBXaAFhLO3jI2oD/RxAEgI1C0Db6XHNca1ywFdb/ise1fftv5ufq3IUGgDUjcMZQioAALLeeOi7Hf75CEBYAJ9zxdU3YADBQCICLe4Xj1J1XAQBWV+T7AGZ8V+BO+i+PUeLW4vsEbACG4u8g9MWPl2G1AXDAkLWTP05/IAKe5W0A7uYF7rT9yS2kuy5sAGSHphvkGhvASiexGU5fpwA4BCAAXgcAAQAEoDybQsb58vwvAGweQbEWgFMvGHeR885jc94m2+D7AEa/B/zMT7VVex/a27FsEQAVrzdwzXXjEWD2CXVXmXNcesFrxQZgAKZcSKv8KGpKDA2+ALizGzAqPgIA4QF49XWA3X6nnfXao44AYPgfjIAQLBoAJ8bwu9ZsAJEXpOEXAQE48SLw/L/O8Du+Kwl4G9CdYL0BPerXmPu14ALApnflPigGIlDsEcB6Ou5r7Rff3msDwN19k6/j2U3AFiAAhjw8AhR5BDBEEB4Aw8ozjwHYAAABsFGAABCzxot8sQA4ofCqmwGf+XFS339uE46xF/HCAoAgGHwBWGojcTGe/yzvcdFrAMNOrAtj/+F2jjcIgDsn2ABwh3NsBMBJxnUhAC4Qz//OrQCA4RcAJx3XweFuLhTGH1fv8wsAQjA9BAa/aAC6i6HcptUMfm4AesEL2nF6/Wtrht0GgA2Bs3gbEAQAEABAAH7W/Egf5b29fwkAIAC2ANz9i3vibcDWLpfu/RsMfu4jQGu2AQx/5Abw0yOBjQADHxiAVV4bGBsgFwkeAQABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABAARgWZ8fdwcBAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABAAQAAAAQAEABCAc/m1YCRcZwIANgBsAQjAtlpzKnGDsQHYAkAARIDka+r3G7EAQPANpVAA5r4OYAug4nVkAxABSl0/j90IBUAECL5uCr591vtRH+nt/cuVzULD//hjsACIAGXu+gJwSgSEgPPX/edeBBcAkaDEc74AbBEBWGX4L5fS7wL4+QAIDgC4+wc/AngUwPDbADwKgEcAcGOLfATwKIDhFwARwPCnB0AEMPzhARABDH94AEQAwx8eABEge/gFQAQIHn4BEAKCh18ARIDQwRcAISB48AVABAgefAEQA8KHXwCEgMChFwAxIHjov/sDGBifz8Hi978AAAAASUVORK5CYII='
tools = ('Sync to Dest', 'Remove Extras', 'Verify Filenames', 'Artists',
        'Show Albums', 'Show non-MP3s', 'Tags', 'Make Album Playlists',
        'Fix Playlist', 'Change Theme')
tooltips = {
    'Sync to Dest': 'Sync MP3s from source to dest folder',
    'Clean Dest': 'Remove files from dest missing in source folder',
    'Verify Filenames': 'Check for and fix mangled filenames',
    'Show non-MP3s': 'Show/Delete non-MP3 files in source folder',
    'Fix Playlist': 'Normalize playlist for root folder and remove extra lines',
    'Verify': 'Nothing here yet',
    'Browser': 'Make playlists for albums with x songs or more',
    'Artists': 'Show all artists in source folder (for fixing misspellings etc)',
    'Albums': 'Show all albums with song counts in source folder',
    'Genres': 'Show all genres',
    'Editor': 'Show and edit all Tags',
    'Change Theme': 'Change GUI colors and font size' }
tools = list(tooltips.keys())
themes = sg.theme_list()
temp_dir = '/tmp'
MAX_HISTORY = 9
MAX_FILES = 50000

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
        elif event == "Fix Playlist":
            fix_playlist_menu(window)
        elif event == 'Artists':
            category_menu(window, 'Artists')
        elif event == 'Albums':
            category_menu(window, 'Albums')
        elif event == 'Genres':
            category_menu(window, 'Genres')
        elif event == 'Verify':
            filename_menu(window)
        elif event == 'Browser':
            browser('/home/michael')
        elif event == 'Editor':
            tag_editor(window)
        elif event == 'Show non-MP3s':
            extra_menu(window)
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
    top_row = 7
    opt1 = tools[:top_row]
    opt2 = tools[top_row:]

    theme = options.get('theme', theme)
    font = options.get('font', ('Arial', size))
    sg.set_options(font=font, tooltip_font=font)
    sg.theme(theme)
    layout = [[sg.Button(opt, tooltip=tooltips[opt]) for opt in opt1],
              [sg.Button(opt, tooltip=tooltips[opt]) for opt in opt2],
              [sg.Multiline(default_text=print.buffer.getvalue(),
                    enable_events=False, size=(120, 20),
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
              [sg.Push(), sg.Text('History:'), sg.Button('Clear'), sg.Button('Copy'),
                    sg.Button('Save')] ]
    return sg.Window('MP3 Gui', layout, font=options['font'], icon=icon, finalize=True)

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
    sg.theme(options.get('theme', ''))

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
        nonlocal text_rows
        files, folders, extra = results
        print.window = None
        start = window['console'].get().count('\n') + 1
        results = check_files(files, extra, source, dest, opts)
        if results:
            window['Copy'].update(disabled=False)
            window['Clip Filenames'].update(disabled=False)
            scanned = True
        t = print.buffer.getvalue()
        text_rows = t.split('\n')[start:], 
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
    tooltips = dict(
        Missing='Show/Copy files missing in dest folder',
        Different='Show/Copy files different in dest folder',
        Extra='Show/Copy non-MP3 files from source folder',
        Same='Show/Copy files that are the same in dest folder',
        Clear='Clear album title in dest folder',
        CRC='Use CRC value to compare source and dest folders(slow)')

    layout = [[sg.Text('Source', size=10),
                sg.Combo(options['history'], default_value=source,
                        size=(50,1), enable_events=True ,key='SOURCE'),
                sg.FolderBrowse(initial_folder=source), sg.Push(), sg.Button('Swap')],
            [sg.Text('Dest', size=10),
                sg.Combo(options['history'], default_value=dest, size=(50,1),
                        enable_events=True ,key='DEST'),
                sg.FolderBrowse(initial_folder=dest)],
            [sg.Checkbox(box, key=box, tooltip=tooltips[box], enable_events=True,
                    default=checked.get(box, False)) for box in boxes],
            [sg.Multiline(enable_events=False, size=(100, 15),
                    key="CONSOLE", write_only=True, disabled=True, autoscroll=True)],
            [sg.Button('Clip Filenames', disabled=True), sg.Push(), sg.Button('Cancel'), 
                    sg.Button('Scan'), sg.Button('Copy', disabled=True)] ]
    
    window = sg.Window('Sync Files', layout, modal=True, finalize=True, return_keyboard_events=True)
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
            window['SOURCE'].update(source)
            window['DEST'].update(dest)
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
        window['LIST'].update(values=extras or ['Nothing found'])
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
    tooltips = dict(
        MP3s='Remove extra MP3s from dest folder',
        Other='Remove other extra files from dest folder',
        Remove='Delete shown files from dest folder',
        Swap='Swap source and dest folders')

    layout = [[sg.Text('Source', size=10),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True ,key='SOURCE', bind_return_key=True),
                sg.FolderBrowse(initial_folder=source, key="SBUT"),
                sg.Push(), sg.Button('Swap', tooltip=tooltips['Swap'])],
            [sg.Text('Dest', size=10),
                sg.Combo(options['history'], default_value=dest, size=(50,1),
                        enable_events=True ,key='DEST', bind_return_key=True),
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
            print('source event')
            nsource = values['SOURCE']
            if comp_dir(source, nsource, True):
                source = nsource
                extras = update(source, dest, opts)
                update_history(window, source)
        elif event == 'DEST':
            ndest = values['DEST']
            if comp_dir(dest, ndest, True):
                dest = ndest
                extras = update(source, dest, opts)
                update_history(window, dest=dest)
        elif event == 'LIST':
            item = values[event][0]
            if item in extras:
                i = extras.index(item)
                extras.remove(item)
                window['LIST'].update(values=extras or ['Nothing found'],
                        scroll_to_index=max(i-2, 0))
        else:
            print(f'{event} {values}')

def verify_menu(window):
    source = options['source']
    print('Opening filename menu')
    boxes = ('MP3s', 'Other')

    layout = [[sg.Text('Source', size=10),
                sg.Combo(options['history'], default_value=source,
                        size=(50,1), enable_events=True ,key='SOURCE'),
                sg.FolderBrowse(initial_folder=source, key="SBUT")],
            [sg.Listbox(['Nothing Scanned'], size=(100, 15),
                    key="LIST")],
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
            window['SOURCE'].update(source)
            window['DEST'].update(dest)
            extras = update(source, dest, opts)
        elif event in boxes:
            extras = update(source, dest, opts)
        elif event == 'Scan':
            source = values['SOURCE']
            files = get_files(source, quiet=True)[0]
            items = check_filenames(files)
            window['LIST'].update(values=items)
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
    boxes = ['Sort by Count', 'Extra Details', 'Unfold Details']
    checked = {'Sort by Count':False, 'Extra Details': True}
    opts = [checked.get(k, False) for k in boxes]
    title, list_items, min_count = set_mode(mode)

    layout = [[sg.Text('Source', size=15),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True ,key='SOURCE', bind_return_key=True),
                sg.FolderBrowse(initial_folder=source, key="SBUT"),
                sg.Push(), sg.Combo(modes, default_value=mode, readonly=True,
                    enable_events=True, key='MODE')],
            [sg.Text('Export Subfolder', size=15), sg.In(mode, size=(51,1), key='DEST')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=checked.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning...'], size=(100, 15), enable_events=True,
                    key="LIST", horizontal_scroll=True)],
            [sg.Text('Minimum Count'), sg.Input(min_count, size=5,
                    enable_events=True, key='COUNT'),
                sg.Push(), sg.Button('Make Playlists'),
                sg.Button('Copy'), sg.Button('Close')] ]
    
    window = sg.Window(title, layout, modal=True, finalize=True)
    items, indexes, songs = list_items(source, min_count, rescan=False, *opts)
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
        elif event == 'Make Playlists':
            make_playlists(songs, mode, source, min_count, values['DEST'])
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
                source = nsource
                update_history(window, source)
                items, indexes, songs = list_items(source, min_count, *opts)
                window['LIST'].update(values=items)
        elif event == 'MODE':
            new_mode = values['MODE']
            title, list_items, min_count = set_mode(new_mode)
            items, indexes, songs = list_items(source, min_count, *opts)
            window['LIST'].update(items)
            window['COUNT'].update(min_count)
            old = window['DEST'].get()
            window['DEST'].update(old.replace(mode, new_mode))
            mode = new_mode
            window.set_title(title)
        elif event == 'LIST':
            selected = window['LIST'].GetIndexes()[0]
            key = indexes[selected]
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
                    window['LIST'].update(items, set_to_index=[selected],
                            scroll_to_index=max(selected-3, 0))

def extra_menu(parent):
    def get_extras(path):
        files, extras, folders = get_files(path, quiet=True)
        return sorted(extras, key=lambda x:x.lower())

    source = options['source']
    boxes = ['Filter Same Folder', 'Filter Same Exts']
    opts = {k :False for k in boxes}
    tooltips = {
        'LIST': 'Click items to filter it or similar items from list'    }
    print('Showing non-MP3 files')

    layout = [[sg.Text('Source', size=15),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                        enable_events=True, key='SOURCE', bind_return_key=True),
                sg.FolderBrowse(initial_folder=source, key="SBUT")],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [sg.Listbox(['Scanning...'], size=(100, 15), enable_events=True,
                    key="LIST", tooltip=tooltips['LIST'])],
            [sg.Push(), sg.Button('Reset'), sg.Button('Remove'), sg.Button('Close')] ]
    window = sg.Window('Extra File Browser', layout, modal=True, finalize=True)
    files = get_extras(source)
    window['LIST'].update(files)
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
        elif event == 'LIST':
            item = values[event][0]
            remove_extras(files, item, opts, window)
        elif event == 'SOURCE':
            if os.path.isdir(values[event]):
                source = os.path.normpath(values[event])
                update_history(window, source)
                files = get_extras(source)
                window['LIST'].update(files)
        elif event == 'Reset':
            files = get_extras(source)
            window['LIST'].update(files)
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
                        enable_events=True ,key='SOURCE', bind_return_key=True),
                sg.FileBrowse(initial_folder=source, key="SBUT",
                    file_types=file_types)],
            [sg.Text('Strip', size=15), sg.In(size=(51,1), key='STRIP')],
            [sg.Text('Prefix', size=15), sg.In(size=(51,1), key='PREFIX')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [sg.Listbox(['Load a Playlist'], size=(100, 15), enable_events=True,
                    key="LIST")],
            [sg.Push(), sg.Button('Save', disabled=True),
                    sg.Button('Show', disabled=True), sg.Button('Close')] ]
    window = sg.Window('Playlist Fixer', layout, modal=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in boxes:
            opts = {box: values[box] for box in boxes}
            if playlist:
                files, strip, prefix = scan_playlist(playlist, opts, window)
        elif event == 'LIST':
            item = values[event][0]
        elif event == 'SOURCE':
            nsource = values[event]
            if os.path.isfile(nsource):
                playlist = values[event]
                source = os.path.split(nsource)[0]
                files, strip, prefix = scan_playlist(playlist, opts, window)
            elif os.path.isdir(nsource):
                source = nsource
                update_history(window, source)
                window['LIST'].update(['Load a Playlist'])
                window['Show'].update('Show', disabled=True)
                window['SBUT'].InitialFolder = source
        elif event == 'Show':
            if window[event].get_text() == 'Show':
                prefix = window['PREFIX'].get()
                window['Show'].update('Reset')
                l = len(values['STRIP'])
                outp = [prefix+f[l:] for f in files if f[0]!='#']
                window['LIST'].update(outp)
            else:
                window['Show'].update('Show')
                window['LIST'].update(files)
        elif event == 'Save':
            p = os.path.split(window['SOURCE'].get())[0]
            path = p if os.path.isdir(p) else options['dest']
            prefix = window['PREFIX'].get()
            l = len(values['STRIP'])
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
    wrong = None

    layout = [[sg.Text('Source', size=15),
                sg.Combo(options['history'], default_value=source,
                        size=(50,1), key='SOURCE'),
                sg.FileBrowse(initial_folder=source, key="SBUT",)],
            [sg.Text('Match', size=15), sg.In(match, size=(51,1), key='MATCH')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [sg.Listbox(['Nothing Found'], size=(100, 15), enable_events=True,
                    key="LIST")],
            [sg.Push(), sg.Button('Scan'), sg.Button('Close')] ]
    window = sg.Window('Verify Filenames', layout, modal=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in boxes:
            opts = {box: values[box] for box in boxes}
        elif event == 'LIST':
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
            window['LIST'].update(wrong, scroll_to_index=i-2)


        elif event == 'Scan':
            if os.path.isdir(values['SOURCE']):
                source = values['SOURCE']
                update_history(window, source)
            else:
                window['SOURCE'].update(source)
                continue
            match = options['pattern'] = values['MATCH']
            wrong, tags, indexes = get_unmatched_filenames(source, match, opts)
            window['LIST'].update(wrong or ['Nothing Found'])   

    window.close()

def edit_file(tags, dest, match=''):
    def get_match_str(tags, match):
        return match.format(
            title=tags.title,
            artist=tags.artist,
            album=tags.album,
            genre=tags.genre)

    size = 8, 60
    orig, tags = tags, tags.copy()
    if match:
        match = match if match and match.endswith('.mp3') else match + '.mp3'
    expected = get_match_str(tags, match)
    if match:
        layout = [[sg.Text('Expected', size=size[0], key='MTEXT'), sg.Text(expected, key='MATCH')]]
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
                window['MATCH'].update(m)
                if m == tags.filename:
                    window['MTEXT'].update('Match')
                else:
                    window['MTEXT'].update('Expected')
   
    window.close()
    return get_match_str(tags, match)

def tag_editor(parent):
    sort_column = 0
    source = options['source']
    boxes = ('Case Sensitive', 'Option 2')
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
            key='TABLE',
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True)

    layout = [[sg.Text('Source', size=12),
                sg.Combo(options['history'], default_value=source, size=(50,1),
                bind_return_key=True, key='SOURCE'),
                sg.FolderBrowse(initial_folder=source, key="SBUT",), sg.Button('Scan')],
            [sg.Text('Filter', size=12), sg.In(size=(51,1), key='FILTER'),
                sg.Combo(('Any',)+headings, default_value='Any', readonly=True,
                        enable_events=True, key='FKEY'),
                sg.Button('Includes'), sg.Button('Excludes'), sg.Button('Reset')],
            [sg.Checkbox(box, key=box, enable_events=True,
                default=opts.get(box, False)) for box in boxes],
            [table_layout],
            [sg.Push(), sg.Button('Multi Edit'), sg.Button('Close')] ]
    window = sg.Window('Verify Filenames', layout, modal=True,finalize=True, return_keyboard_events=True)
    window['SOURCE'].bind("<Return>", "_ENTER")
    window['FILTER'].bind("<Return>", "_ENTER")
    etable = window['TABLE']
    scroller = get_scroller(window['TABLE'])

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
        elif event in ('Scan', 'Reset', 'SOURCE_ENTER'):
            nsource = values['SOURCE']
            if os.path.isdir(nsource):
                source = nsource
                update_history(window, source)
                table, tags = make_tag_table(source, event=='Reset')
                sort_column = 0
                window['TABLE'].update(table)
            else:
                window['SOURCE'].update(source)
        elif event in ('Includes', 'FILTER_ENTER'):
            table = filter_tag_table(values['FILTER'], table,
                    window['FKEY'].get(), headings, opts)
            window['FILTER'].update('')
            window['TABLE'].update(table)
        elif event == 'Excludes':
            table = filter_tag_table(values['FILTER'], table,
                    window['FKEY'].get(), headings, opts, True)
            window['FILTER'].update('')
            window['TABLE'].update(table)
        elif event in boxes:
            opts[event] = values[event]

        # HANDLE TABLE CLICKS
        elif isinstance(event, tuple) and event[0] == 'TABLE':
            selected = values['TABLE']
            clicked = event[2]
            if len(selected) == 1 and selected[0] == clicked[0]:
                # DOUBLE CLICKED TO EDIT
                row = table[clicked[0]]
                fn = row[-1]
                seltags = tags[fn]
                edit_file(seltags, source)
                table[clicked[0]] = seltags.as_row()
                window['TABLE'].update(table)
            elif clicked[0] == -1:
                sort_column = clicked[1]
                table = sort_table(table, sort_column)
                window['TABLE'].update(table)
            else:
                print(f'Table clicked at {clicked}')

        elif event == 'TABLE':
            pass

        elif event == 'Multi Edit':
            print(f'rows seleced: {values["TABLE"]}')
        elif event[1] == ':' and window.find_element_with_focus() == etable:
            scroller(event[0], table, sort_column)
    window.close()


def get_scroller(element):
    def scroll_to_index(key, data, col=None):
        nonlocal last_press, keys_pressed
        c = key.lower()
        ti = time.perf_counter()
        if ti - last_press < KEY_DELAY:
            keys_pressed += c
        else:
            keys_pressed = c
        last_press = ti
        if col != None:
            for i, row in enumerate(data):
                if keys_pressed < row[col].lower():
                    break
        else:
            for i, item in enumerate(data):
                if keys_pressed < item.lower():
                    break
        perc = i / len(data)
        element.set_vscroll_position(perc)
        if isinstance(element, sg.Table):
            element.update(select_rows=[i])
    KEY_DELAY = 1
    keys_pressed = ''
    last_press = 0
    return scroll_to_index


def row_to_tags(row):
    pass


def make_tag_table(path, reset=False):
    if reset and hasattr(make_tag_table, 'files'):
        print('resetting')
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
            window['LIST'].update(items)
            window['PARENTS'].update(parents[0] or '/', values=parents[1:])
        return items, parents

    items, parents = get_listing(path)
    layout = [[sg.Combo(parents[1:], size=PATH_LENGTH,
                    default_value=parents[0], key='PARENTS',
                    enable_events=True, bind_return_key=True),
                sg.Push(), sg.Button('^', key='UP')],
            [sg.Listbox(items, size = (PATH_LENGTH+5, BOX_HEIGHT), key='LIST', enable_events=True)],
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
        elif event == 'LIST':
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
        print(f'options loaded from {fn}')
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
        e = window.Find('SOURCE', True)
        if e: window['SOURCE'].update(source, history)
    if dest:
        dest = os.path.normpath(dest)
        if dest in history:
            history.remove(dest)
        history.insert(0, dest)
        history = history[:MAX_HISTORY]
        options['dest'] = dest
        e = window.Find('DEST', True)
        if e: window['DEST'].update(dest, history)

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
        def update(self, other):
            self.filename = other.filename
            self.title = other.title
            self.artist = other.artist
            self.album = other.album
            self.genre = other.genre
        def as_row(self, folders=True):
            fn = self.filename if folders else os.path.split(self.filename)[1]
            return [self.title, self.artist, self.album,
                    self.genre, fn]
            
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
        def copy(self):
            return SongTag(self.filename, self.title, self.artist,
                    self.album, self.genre)

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

def remove_extras(files, clicked, opts, window):
    sel = files.index(clicked)
    if opts['Filter Same Folder']:
        folder = os.path.split(clicked)[0]
        for i, f in enumerate(reversed(files)):
            if os.path.split(f)[0] == folder:
                sel = i
                files.remove(f)
        sel = len(files) - sel
    elif opts['Filter Same Exts']:
        ext = os.path.splitext(clicked)[1]
        for i, f in enumerate(reversed(files)):
            if os.path.splitext(f)[1] == ext:
                sel = i
                files.remove(f)
        sel = len(files) - sel
    elif clicked in files:
        files.remove(clicked)
    window['LIST'].update(values=files or ['Nothing found'],
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
    window['LIST'].update(lines)
    window['STRIP'].update(strip)
    window['PREFIX'].update(prefix)
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

def print_dict(d, info='dictionary'):
    _print('\n', info)
    for i in d:
        _print(i, d[i])

if __name__ == '__main__':
    main()