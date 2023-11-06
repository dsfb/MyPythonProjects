from pathlib import Path
import os
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')


def get_new_path(location):
    if os.path.isabs(location):
        return location

    return os.path.join(os.getcwd(), location)


def change_current_directory(location):
    new_path = get_new_path(location)

    try:
        os.chdir(new_path)
    except FileNotFoundError:
        pass
    finally:
        print(os.path.basename(os.getcwd()))


def get_human_format_size(size_bytes):
    if size_bytes < 1024:
        return f'{size_bytes}B'

    if size_bytes < 1024 ** 2:
        return f'{round(size_bytes / 1024)}KB'

    if size_bytes < 1024 ** 3:
        return f'{round(size_bytes / 1024 ** 2)}MB'

    return f'{round(size_bytes / 1024 ** 2)}GB'


def get_entries():
    old_entries = os.listdir(os.getcwd())
    dir_entries = sorted([ent for ent in old_entries if os.path.isdir(ent)])
    file_entries = sorted([ent for ent in old_entries if os.path.isfile(ent)])
    return dir_entries + file_entries


def show_long_listing_format_directory(entries):
    for ent in entries:
        if os.path.isdir(ent):
            print(ent)
        else:
            size = os.stat(ent).st_size
            print(f'{ent} {size}')


def show_long_human_readable_format_directory(entries):
    for ent in entries:
        if os.path.isdir(ent):
            print(ent)
        else:
            size = os.stat(ent).st_size
            print(f'{ent} {get_human_format_size(size)}')


def list_directory(cmd):
    tokens = cmd.split()
    len_t = len(tokens)
    entries = get_entries()

    if len_t == 1:
        for ent in entries:
            print(ent)
    elif len_t == 2:
        if tokens[1] == '-l':
            show_long_listing_format_directory(entries)
        elif tokens[1] == '-lh':
            show_long_human_readable_format_directory(entries)


def get_input_from_prompt_question(filename):
    question = f'{filename} already exists in this directory. Replace? (y/n)'
    choice = ''
    while choice.lower() not in ('y', 'n'):
        choice = input(question)
    return choice


def remove(arg):
    if not arg.startswith('.'):
        if not arg or not arg.strip():
            print('Specify the file or directory')
            return

        if not os.path.isfile(arg) and \
                not os.path.isdir(arg):
            print('No such file or directory')
            return

        abs_path = get_new_path(arg)
        if os.path.isdir(abs_path):
            if not os.listdir(abs_path):
                os.removedirs(abs_path)
            else:
                shutil.rmtree(abs_path)
        else:
            os.remove(abs_path)

        return

    entries = get_entries()

    found_files = [entry for entry in entries if
                   Path(entry).suffix == arg]

    if not found_files:
        print(f'File extension {arg} not found in this directory')
        return

    for entry in found_files:
        os.remove(entry)


def mv(src, dest):
    shutil.move(src, dest)


def check_for_invalid_movement(the_extension, dest_dir):
    if not the_extension:
        print('Specify the current name of the file or directory and the new location and/or name')
        return True

    if not dest_dir:
        print('Specify the current name of the file or directory and the new name')
        return True

    if os.path.isdir(the_extension) and \
            not Path(dest_dir).suffix:
        mv(the_extension, dest_dir)
        return True

    if os.path.isfile(the_extension):
        print('The file or directory already exists')
        return True

    if not the_extension.startswith('.'):
        print('No such file or directory')
        return True

    return False


def move(cmd):
    if not cmd.startswith('.'):
        filenames = cmd.split()

        if len(filenames) == 1:
            print('Specify the current name of the file or directory and the new name')
            return

        if len(filenames) != 2:
            print('Specify the current name of the file or directory and the new location and/or name')
            return

        if os.path.isfile(filenames[-1]):
            print('The file or directory already exists')
            return

        if not os.path.isfile(filenames[0]) and \
                not os.path.isdir(filenames[0]):
            print('No such file or directory')
            return

        shutil.move(filenames[0], filenames[1])

        return

    arg, destin_dir = cmd.split()

    if check_for_invalid_movement(arg, destin_dir):
        return

    if os.path.isfile(arg) and \
            not Path(destin_dir).suffix:
        mv(arg, destin_dir)
        return

    entries = get_entries()
    found_files = [entry for entry in entries if
                   Path(entry).suffix == arg]

    if not found_files:
        print(f'File extension {arg} not found in this directory')
        return

    for filename in found_files:
        target_filename = os.path.join(destin_dir, filename)
        if os.path.isfile(target_filename):
            choice = get_input_from_prompt_question(filename)
            if choice == 'n':
                continue
            elif choice == 'y':
                os.remove(target_filename)
                mv(filename, destin_dir)
        else:
            mv(filename, destin_dir)


def create_dir(arg):
    if not arg or not arg.strip():
        print('Specify the name of the directory to be made')
        return

    if os.path.exists(arg) and os.path.isdir(arg):
        print('The directory already exists')
        return

    os.mkdir(arg)


def copy(cmd):
    if not cmd.startswith('.'):
        if not cmd or not cmd.strip():
            print('Specify the file')
            return

        filenames = cmd.split()
        if not os.path.exists(filenames[0]):
            print(f'No such file or directory: {filenames[0]}')
            return

        if len(filenames) != 2:
            print('Specify the current name of the file or directory and the new name')
            return

        if os.path.exists(filenames[1]) and filenames[1] != '..':
            print(f'{filenames[0] if filenames[1] == "." else filenames[1]} already exists in this directory')
            return

        if os.path.isdir(filenames[1]):
            shutil.copy(filenames[0], filenames[1])
            return

        shutil.copyfile(filenames[0], filenames[1])

        return

    if not cmd:
        print('Specify the file')
        return

    arg, target_dir = cmd.split()

    entries = get_entries()
    found_files = [entry for entry in entries if
                   Path(entry).suffix == arg]

    if not found_files:
        print(f'File extension {arg} not found in this directory')
        return

    for filename in found_files:
        target_filename = os.path.join(target_dir, filename)
        if os.path.isfile(target_filename):
            choice = get_input_from_prompt_question(filename)
            if choice == 'n':
                continue
            elif choice == 'y':
                os.remove(target_filename)
                shutil.copy(filename, target_dir)
        else:
            shutil.copy(filename, target_dir)


if __name__ == '__main__':
    print('Input the command')
    while True:
        cmd = input()
        if cmd == 'pwd':
            print(os.getcwd())
        elif cmd.startswith('cd') and len(cmd) > 2:
            change_current_directory(cmd[3:])
        elif cmd.startswith('ls'):
            list_directory(cmd)
        elif cmd.startswith('rm'):
            tokens = cmd.split()
            if len(tokens) == 2:
                _, extension = tokens
            else:
                extension = ''

            remove(extension)
        elif any(word for word in ('mv', 'cp') if word in cmd):
            if cmd.startswith('cp'):
                copy(cmd[3:])
            elif cmd.startswith('mv'):
                move(cmd[3:])
        elif cmd.startswith('mkdir'):
            create_dir(cmd[6:])
        elif cmd == 'quit':
            break
        else:
            print('Invalid command')
