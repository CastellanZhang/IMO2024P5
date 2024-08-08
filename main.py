import numpy as np


# 随机生成一个二维表格, 用于测试，0为安全，1为陷阱。除了第一行和最后一行外，每行一个陷阱；每列最多一个陷阱
def generate_table_random(row):
    column = row - 1
    trap_num = column - 1
    table = np.zeros((row, column), dtype=np.int8)
    trap_index = np.random.choice(column, trap_num, replace=False)
    k = 0
    for i in range(row):
        if i == 0 or i == row - 1:
            continue
        j = trap_index[k]
        k += 1
        table[i][j] = 1
    return table


# 给定表格，给定路径，判断是不是一个能获胜的路径
def is_win(table, path):
    row = table.shape[0]
    column = table.shape[1]
    if len(path) == 0:
        return False
    if path[0][0] != 0: # 起始位置必须为第一行
        return False
    if path[-1][0] != row - 1: # 结束位置必须为最后一行
        return False
    for i in range(len(path)):
        cur_p = path[i]
        x, y = cur_p
        if x < 0 or x >= row:
            return False
        if y < 0 or y >= column:
            return False
        if table[x][y] == 1: # 当前位置是陷阱
            return False
        if i == 0:
            continue
        pre_p = path[i - 1]
        # 前后两个格子的关系只能是上下左右
        if abs(cur_p[0] - pre_p[0]) + abs(cur_p[1] - pre_p[1]) != 1:
            return False
    return True


# 给定表格，按照策略生成最后获胜的路径
def generate_path(table):
    row = table.shape[0]
    column = table.shape[1]
    # 第一轮尝试，找到第二行的陷阱位置
    trap_y = -1
    for j in range(column):
        if table[1][j] == 1:
            trap_y = j
    # 分情况讨论
    if trap_y == 0: # 第二行陷阱靠最左边
        return generate_path_far_left(table)
    elif trap_y == column - 1: # 第二行陷阱靠最右边
        return generate_path_far_right(table)
    else:
        return generate_path_middle(table, trap_y)


# 一般情况
def generate_path_middle(table, trap_y):
    row = table.shape[0]
    column = table.shape[1]
    path = []
    if table[2][trap_y - 1] == 0: # 第二轮尝试，如果第二行陷阱的左下方安全
        path += [(0, trap_y - 1), (1, trap_y - 1), (2, trap_y - 1)]
    else: # 第三轮尝试，如果第二行陷阱的右下方安全
        path += [(0, trap_y + 1), (1, trap_y + 1), (2, trap_y + 1)]
    for i in range(2, row):
        path.append((i, trap_y))
    return path


# 靠最左边情况
def generate_path_far_left(table):
    row = table.shape[0]
    column = table.shape[1]
    path = [(0, 1), (1, 1), (1, 2)]
    pre_direction = 'R'
    while True:
        if pre_direction == 'R': # 上一步是右移，这一步则下移
            pre_direction = 'D'
            p = (path[-1][0] + 1, path[-1][1])
            if table[p[0]][p[1]] == 0: # 当前位置安全
                path.append(p)
                if p[1] == column - 1: # 已经走到图中深绿色位置
                    path.append((p[0] + 1, p[1]))
                    return path
            else: # 当前位置是陷阱
                path[-1] = (path[-1][0] + 1, path[-1][1] - 1) # 修正路线
                x, y = path[-1]
                for j in range(y - 1, -1, -1): # 左移到头
                    path.append((x, j))
                for i in range(x + 1, row): # 下移到头
                    path.append((i, 0))
                return path
        else: # 上一步是下移，这一步则右移
            pre_direction = 'R'
            p = (path[-1][0], path[-1][1] + 1)
            if table[p[0]][p[1]] == 0:  # 当前位置安全
                path.append(p)
            else:  # 当前位置是陷阱
                path.pop() # 修正路线
                path[-1] = (path[-1][0] + 1, path[-1][1] - 1) # 修正路线
                x, y = path[-1]
                for j in range(y - 1, -1, -1): # 左移到头
                    path.append((x, j))
                for i in range(x + 1, row): # 下移到头
                    path.append((i, 0))
                return path


# 将表格左右镜像翻转
def mirror_table(table):
    row = table.shape[0]
    column = table.shape[1]
    new_table = np.zeros(table.shape, dtype=np.int8)
    for i in range(row):
        for j in range(column):
            new_table[i][j] = table[i][column - j - 1]
    return new_table


# 将路径左右镜像翻转
def mirror_path(table, path):
    row = table.shape[0]
    column = table.shape[1]
    new_path = []
    for p in path:
        new_path.append((p[0], column - p[1] - 1))
    return new_path


# 靠最右边情况，利用镜像翻转实现
def generate_path_far_right(table):
    path = generate_path_far_left(mirror_table(table))
    return mirror_path(table, path)


# 用三种特殊符号将表格和路径打印出来
def print_talbe_and_path(table, path):
    row = table.shape[0]
    column = table.shape[1]
    img = [['🈳' for _ in range(column)] for _ in range(row)]
    for i in range(row):
        for j in range(column):
            if table[i][j] == 1:
                img[i][j] = '🈶'
    for p in path:
        x, y = p
        img[x][y] = '⭐️'
    for i in range(row):
        for j in range(column):
            print(img[i][j], end = '')
        print()


def test_is_win():
    table = np.array([[0,0,0,0],
                      [1,0,0,0],
                      [0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,0]])
    path = [(0,1),
            (1,1),
            (1,2),
            (2,2),
            (2,3),
            (3,3),
            (4,3)]
    print(is_win(table, path))


def test_generate_path_random():
    # table = np.array([[0,0,0,0],
    #                   [0,0,0,1],
    #                   [1,0,0,0],
    #                   [0,1,0,0],
    #                   [0,0,0,0]])
    table = generate_table_random(8)
    path = generate_path(table)
    print(path)
    print(is_win(table, path))
    print_talbe_and_path(table, path)


# 穷举生成所有陷阱分布，然后统计获胜策略是否都能成功
def generate_tables(row, column, current_row=1, table=None):
    global count, win_count
    if table is None:
        table = np.zeros((row, column), dtype=np.int8)
    if current_row == row - 1:
        # 当所有行都填充完毕时
        count += 1
        path = generate_path(table)
        if is_win(table, path):
            win_count += 1
            print_talbe_and_path(table, path)
            print()
        return
    # 从第一列开始尝试放置1
    for y in range(column):
        if all(table[x][y] == 0 for x in range(current_row)):
            # 如果当前列在之前的行中都是0，则尝试放置1
            table[current_row][y] = 1
            generate_tables(row, column, current_row + 1, table)
            table[current_row][y] = 0  # 回溯，撤销放置


if __name__ == '__main__':
    # test_generate_path_random()
    count = 0
    win_count = 0
    generate_tables(8, 7)
    # count为分布数，win_count为获胜数
    print("count = ", count)
    print("win_count = ", win_count)
