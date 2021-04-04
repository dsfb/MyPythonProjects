# write your code here

import os

output = ''
while True:
    choice = input('- Choose a formatter:')
    if choice == '!done':
        file_name = 'output.md'
        dir_path = os.path.dirname(os. path. realpath(__file__))
        full_path = os.path.join(dir_path, file_name)
        print('full path:', full_path)
        with open(full_path, 'w') as output_file:
            output_file.write(output)
        break
    elif choice == '!help':
        print('''Available formatters: plain bold italic link inline-code header ordered-list unordered-list line-break
Special commands: !help !done''')
    elif choice in ('plain', 'bold', 'italic', 'inline-code', 'link', 'header', 'unordered-list',
                    'ordered-list', 'line-break', 'new-line'):
        if choice == 'header':
            level = input('- Level:')
            if int(level) not in (1, 2, 3, 4, 5, 6):
                print('The level should be within the range of 1 to 6')
            else:
                text = input('- Text:')
                if output == '':
                    output = '#' * int(level) + ' ' +  text + '\n'
                elif not output.endswith('\n'):
                    output += '#' * int(level) + ' ' + text + '\n'
        elif choice == 'plain':
            text = input('- Text:')
            output += text
        elif choice == 'bold':
            text = input('- Text:')
            output += f'**{text}**'
        elif choice == 'italic':
            text = input('- Text:')
            output += f'*{text}*'
        elif choice == 'inline-code':
            text = input('- Text:')
            output += f'`{text}`'
        elif choice == 'link':
            label = input('- Label:')
            url = input('- URL:')
            if output == '':
                output = f'[{label}]({url})'
            elif not output.endswith('\n'):
                output += f'[{label}]({url})'
        elif choice == 'new-line':
            output += '\n'
        elif choice == 'ordered-list':
            while True:
                number = int(input('- Number of rows: '))
                if number <= 0:
                    print('The number of rows should be greater than zero')
                else:
                    break
            rows = list()
            for i in range(1, number + 1):
                line = input(f'- Row #{i}: ')
                output += f'{i}. {line}\n'
        elif choice == 'unordered-list':
            while True:
                number = int(input('- Number of rows: '))
                if number <= 0:
                    print('The number of rows should be greater than zero')
                else:
                    break
            rows = list()
            for i in range(1, number + 1):
                line = input(f'- Row #{i}: ')
                output += f'* {line}\n'
        else:
            continue

        print(output)
    else:
        print('Unknown formatting type or command')