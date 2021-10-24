# write your code here
import hashlib
import os
import sys

from collections import defaultdict

if len(sys. argv) > 1:
    folder_path = sys.argv[1]
else:
    print('Directory is not specified')
    sys.exit(0)

file_format = input('Enter file format:')

print()
print('Size sorting options:')
print('1. Descending')
print('2. Ascending')

sorting_option = input('Enter a sorting option:')
print()
while sorting_option not in ('1', '2'):
    print('Wrong option')
    sorting_option = input('Enter a sorting option:')
sorting_option = int(sorting_option) == 1

files_by_size = defaultdict(list)
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if not file_format or file_name.endswith(file_format):
            full_path = os.path.join(root, file_name)
            file_size = os.path.getsize(full_path)
            files_by_size[file_size].append(full_path)

for file_size in sorted(files_by_size, reverse=sorting_option):
    if len(files_by_size[file_size]) > 1:
        print(f'\n{file_size} bytes')
        for file_path in files_by_size[file_size]:
            print(f'{file_path}')
print()

duplicates_option = input('Check for duplicates?')
while duplicates_option not in ('yes', 'no'):
    print('Wrong option')
    print()
    duplicates_option = input('Check for duplicates?')

if duplicates_option == 'yes':
    counter = 1
    duplicates_dict = {}
    for file_size in sorted(files_by_size, reverse=sorting_option):
        print(f'\n{file_size} bytes')
        hash_dict = defaultdict(list)
        for file_path in files_by_size[file_size]:
            md5_hash = hashlib.md5()
            a_file = open(file_path, "rb")
            content = a_file.read()
            md5_hash.update(content)
            digest = md5_hash.hexdigest()
            hash_dict[digest].append(file_path)

        for digest, file_paths in hash_dict.items():
            if len(file_paths) > 1:
                print(f'Hash: {digest}')
                sorted_file_paths = sorted(file_paths)
                for file_path in sorted_file_paths:
                    print(f'{counter}. {file_path}')
                    duplicates_dict[counter] = file_path, file_size
                    counter += 1

print()
deleting_option = input('Delete files?')
while deleting_option not in ('yes', 'no'):
    print('Wrong option')
    print()
    deleting_option = input('Delete files?')

if deleting_option == 'yes':
    file_list = input('Enter file numbers to delete:')
    while True:
        file_num_list = []
        continued_condition = False
        if not file_list or not file_list.replace(' ', '').isdigit():
            continued_condition = True

        if continued_condition:
            print('Wrong format')
            file_list = input('Enter file numbers to delete:')
            continue

        file_number_str_list = file_list.split(' ')
        for num_str in file_number_str_list:
            if num_str.isdigit():
                number = int(num_str)
                file_num_list.append(number)
                if number >= counter:
                    continued_condition = True
                    break

        if continued_condition:
            print('Wrong format')
            file_list = input('Enter file numbers to delete:')
        else:
            break

    freed_total = 0
    for file_number in file_num_list:
        os.remove(duplicates_dict[file_number][0])
        freed_total += duplicates_dict[file_number][1]

    print(f'Total freed up space: {freed_total} bytes')