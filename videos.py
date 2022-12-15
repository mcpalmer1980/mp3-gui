import PySimpleGUI as sg
import os, sys, subprocess

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

buttons = ['Replay', 'Reset', 'Skip', 'Next']

def play_video(path, fn=None):
    if fn: path = os.path.join(path, fn)
    opts = '--no-fullscreen --repeat --hotkeys-y-wheel-mode=2'
    opts = opts.split(' ')
    params = ['vlc', path] + opts
    subprocess.run(params, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def main_window(path):
    def update(filename, play=True):
        nonlocal prefix, orig, shortname
        orig = shortname = os.path.splitext(filename)[0]
        window['Reset'].update('Clear')
        window['orig'].update(orig)
        window['new'].update(orig)
        if play: play_video(path, filename)
        prefix = ''
    def update_filename():
        orig = window['orig'].get()
        if orig == shortname:
            window['Reset'].update('Clear')
        else:
            window['Reset'].update('Reset')

        if prefix:
            window['new'].update(f'{prefix} - {orig}')
        else:
            window['new'].update(orig)

    prefix = orig = shortname = ''
    files = get_files(path)
    if not files:
        print('No Files found: exiting')
        return

    filename = files[0]
    font = ('arial', 16)
    sg.set_options(font=font, tooltip_font=font)

    layout = [
        [sg.Text('Orig:', size=8), sg.In(key='orig', size=30,
                expand_x=True, enable_events=True)],
        [sg.Text('New:', size=8), sg.Text(key='new', size=30, expand_x=True)]
    ]
    layout += [[sg.Button(but) for but in line] for line in keywords]
    layout += [[sg.VSeparator(pad=(10, 20))]]
    layout += [[sg.Push()] + [sg.Button(but) for but in buttons]]

    window = sg.Window('Video Namer', layout, finalize=True)
    update(filename)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,):
            finish = os.path.join(path, continue_file)
            if files:
                with open(finish, 'w') as file:
                    for f in files:
                        print(f, file=file)
            elif os.path.isfile(finish):
                os.remove(finish)
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
        elif event == 'Skip':
            files.pop(0)
            filename = files[0]
            update(filename)
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

            files.pop(0)
            filename = files[0]
            update(filename)
        elif event in keylist:
            prefix += f'{event} '
            update_filename()
    window.close()

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
print(path)
main_window(path)