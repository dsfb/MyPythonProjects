
def get_christmas_tree(tree_height, step):
    tree_lines = []
    i = 0
    # Tree
    for j in range(2 * tree_height - 1, 1, -2):
        line = []
        for _ in range(i):
            line.append(' ')
        line.append('/')
        for k in range(j - 2):
            line.append('*')
        line.append('\\')
        for _ in range(i):
            line.append(' ')
        i += 1
        tree_lines.insert(0, line)

    # Decorate the tree
    counter = 1
    for line in tree_lines:
        star_counter = 0
        for ind, c in enumerate(line):
            if c == '*':
                star_counter += 1
                if star_counter % 2 == 0:
                    if counter % step == 1 or step == 1:
                        line[ind] = 'O'
                    counter += 1

    # Tree topper
    for c in ('^', 'X'):
        line = []
        for _ in range(i):
            line.append(' ')
        line.append(c)
        for _ in range(i):
            line.append(' ')
        tree_lines.insert(0, line)

    # Tree stand
    line = []
    empty_space_len = tree_height - 2
    for _ in range(empty_space_len):
        line.append(' ')
    for c in ('|', ' ', '|'):
        line.append(c)
    for _ in range(empty_space_len):
        line.append(' ')
    tree_lines.append(line)

    return tree_lines



def get_empty_postcard(width, height, msg='Merry Xmas', line_msg=27):
    postcard_lines = []
    first_line = ['-',] * width
    postcard_lines.append(first_line)
    for _ in range(height - 2):
        second_line = ['|',] + [' ',] * (width - 2) + ['|',]
        postcard_lines.append(second_line)
    postcard_lines.append(first_line)
    msg_ind = int(width / 2)
    msg_ind -= int(len(msg) / 2)
    for c in msg:
        postcard_lines[line_msg][msg_ind] = c
        msg_ind += 1
    return postcard_lines


def get_tree_data_for_postcard(line):
    it = 0
    len_data = len(line)
    tree_data = []
    while it < len_data:
        tree_data.append(tuple(int(line[i]) for i in range(it, it + 4)))
        it += 4
    return tree_data


def fill_postcard(postcard, tree_data, postcard_width, postcard_height):
    for data in tree_data:
        height, step = data[:2]
        tree = get_christmas_tree(height, step)
        column, line = data[2:]
        for i in range(column, min(column + len(tree), postcard_height)):
            for j in range(line - height, min(line - height + len(tree[0]), postcard_width)):
                if tree[i - column][j - line + height] != ' ':
                    postcard[i][j + 1] = tree[i - column][j - line + height]

    return postcard


if __name__ == '__main__':
    while True:
        line = input().split()
        if len(line) == 2:
            height, step = tuple(int(elem) for elem in line)
            tree_lines = get_christmas_tree(height, step)

            # Tree printing
            for line in tree_lines:
                print(''.join(line))
        else:
            width = 50
            height = 30
            tree_data = get_tree_data_for_postcard(line)
            postcard = get_empty_postcard(width, height)
            postcard = fill_postcard(postcard, tree_data, width, height)

            # Postcard printing
            for line in postcard:
                print(''.join(line))
