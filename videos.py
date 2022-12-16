import PySimpleGUI as sg
import os, sys, subprocess

icon = b'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'
extensions = ('.avi', '.mpg', '.mp4', '.mpv', '.mov', '.mpeg')
continue_file = 'finish.dat'

def get_files(path):
    finish = os.path.join(path, continue_file)
    try:            
        files = []
        with open(finish) as f:
            for line in f:
                files.append(line.strip('\n'))
        print(f'{len(files)} videos will be continued')
    except:
        print('Scanning for videos in', path)
        files = sorted(os.listdir(path), key=lambda x: x.lower())

    videos = []
    others = []
    for f in files:
        if os.path.splitext(f)[1] in extensions:
            videos.append(f)
        elif os.path.isfile(os.path.join(path, f)):
            others.append(f)
    print('Found: '+', '.join(set([os.path.splitext(f)[1] for f in videos])))
    print('Unmatched: '+', '.join(set([os.path.splitext(f)[1] for f in others])))
    print(f"Non video files: {', '.join(others)}")
    return videos

try:
    with open('keywords') as f:
        keywords = []
        for line in f:
            if line:
                keywords.append(line.strip(' \n').split(' '))
except:
    keywords = [['good', 'best',]]
keylist = sum(keywords, [])

buttons = ['Replay', 'Delete', 'Reset', 'Skip', 'Next']

def play_video(path, fn=None):
    if fn: path = os.path.join(path, fn)
    opts = '--no-fullscreen --repeat --hotkeys-y-wheel-mode=2'
    opts = opts.split(' ')
    params = ['vlc', path] + opts
    subprocess.run(params, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def rename_path(path, element):
    print(path)
    p = os.path.split(path)[-1]
    p = sg.popup_get_text(f'Rename {p} folder?', title='Rename',
            default_text=p)
    if p:
        base = os.path.split(path)[0]
        old = path
        new = os.path.join(base, p)
        element.update(p)
        os.rename(old, new)
        return new
    return path

    print(f"rename '{old}' -> '{new}")


def main_window(path):
    def update(fn, play=True):
        nonlocal prefix, orig, shortname, filename
        filename = fn
        orig = shortname = os.path.splitext(filename)[0]
        window['Reset'].update('Clear')
        window['orig'].update(orig)
        window['new'].update(orig)
        window['path'].update(os.path.split(path)[-1])
        if play: play_video(path, filename)
        prefix = ''
    def update_filename():
        orig = window['orig'].get()
        if orig == shortname:
            window['Reset'].update('Clear')
        else:
            window['Reset'].update('Reset')

        new = f'{prefix} - {orig}' if prefix else orig
        window['new'].update(new)
        sg.clipboard_set(new)

    def next_file():
        nonlocal files
        if len(files) > 1:
            files.pop(0)
            update(files[0])
            return True
        files = []

    prefix = orig = shortname = ''
    files = get_files(path)
    if not files:
        print('No Files found: exiting')
        return

    filename = files[0]
    font = ('arial', 16)
    sg.set_options(font=font, tooltip_font=font, icon=icon)

    layout = [
        [sg.Text('Path:', size=6), sg.Text(key='path', size=30,
                expand_x=True), sg.Push(), sg.Button('<-Add'), 
                    sg.Button('Rename'), sg.Button('Add->')],
        [sg.Text('Orig:', size=6), sg.In(key='orig', size=30,
                expand_x=True, enable_events=True)],
        [sg.Text('New:', size=6), sg.Text(key='new', size=30, expand_x=True)]
    ]
    layout += [[sg.Button(but) for but in line] for line in keywords]
    layout += [[sg.VSeparator(pad=(10, 20))]]
    layout += [[sg.Push()] + [sg.Button(but) for but in buttons]]

    window = sg.Window('Video Namer', layout, finalize=True)
    update(filename)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,):
            break
        elif event == 'orig':
            update_filename()
        elif event == 'Replay':
            play_video(path, filename)
        elif event == 'Reset':
            if values['orig'] == shortname:
                window['orig'].update('')
                update_filename()
            else:
                update(filename, False)
        elif event == '<-Add':
            s = os.path.split(path)[-1] + ' ' + window['orig'].get()
            window['orig'].update(s)
            update_filename()
        elif event == 'Add->':
            s =  window['orig'].get() + ' ' +os.path.split(path)[-1]
            window['orig'].update(s)
            update_filename()
        elif event == 'Rename':
            path = rename_path(path, window['path'])
        elif event == 'Delete':
            r = sg.popup_ok_cancel(filename, 'Okay to delete this file?',
                    title='Confirm')
            if r == 'OK':
                os.remove(os.path.join(path, filename))
                if not next_file():
                    break
        elif event == 'Skip':
            if not next_file():
                break
        elif event == 'Next':
            oldname = os.path.join(path, filename)
            newname = os.path.join(path, window['new'].get())
            newname += os.path.splitext(filename)[1]
            if oldname == newname:
                pass
            elif not window['orig'].get():
                update(filename, False)
                continue
            elif os.path.exists(newname):
                sg.popup_ok('Please choose another filename', title='File Exists')
                continue
            else:
                os.rename(oldname, newname)
            if not next_file():
                break
        elif event in keylist:
            prefix += f'{event} '
            update_filename()
    window.close()


    finish = os.path.join(path, continue_file)
    if files:
        with open(finish, 'w') as file:
            for f in files:
                print(f, file=file)
    elif os.path.isfile(finish):
        os.remove(finish)
        return True


path = None
if len(sys.argv) > 1:
    path = sys.argv[1]
    if os.path.isfile(path):
        path = os.path.split(path)[0]
    elif not os.path.isdir(path):
        path = None
if not path:
    path = os.path.split(__file__)[0]
    path = sg.popup_get_folder('Select a Folder', default_path=path)
    if not path:
        print('No path offered')
        exit()

while True:
    if main_window(path):
        if sg.popup_yes_no('All files have been named',
                'Rename another folder?', title='Another?') != 'Yes':
            break
        print(path)
        path = sg.popup_get_folder('Select a Folder', initial_folder=path, default_path=path)
        if not path: break
    else:
        break