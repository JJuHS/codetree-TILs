import sys
from copy import deepcopy
input = sys.stdin.readline
# 1. 참가자 모두 이동
# 출구랑 가까운 쪽으로, 상하 먼저, 좌우로
# 못움직인다면 가만히, 두명이상 같은 곳 가능
# 2. 미로 회전
# 참가자랑 출구 포함한 가장 작은 정사각형 찾기
# 2개 이상이면, 위에것 먼저, 왼쪽거 먼저
# 시계방향 90도 회전, 회전한 벽은 내구도 -1

direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]
n, m, k = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(n)]
survivors = [tuple(map(int, input().split())) for _ in range(m)]
exit_r, exit_c = map(int, input().split())
exit_r -= 1
exit_c -= 1

res = 0

def move_survivors(dist):
    global survivors
    for idx, p in enumerate(survivors):
        dist_r, dist_c = exit_r - p[0], exit_c - p[1]
        if dist_r != 0:
            is_down = 1 if dist_r > 0 else -1
            nr, nc = p[0] + is_down, p[1]
            if nr in range(n) and nc in range(n):
                if maze[nr][nc] == 0:
                    survivors[idx] = (nr, nc)
                    dist += 1
                    continue
        if dist_c != 0:
            is_right = 1 if dist_c > 0 else -1
            nr, nc = p[0], p[1] + is_right
            if nr in range(n) and nc in range(n):
                if maze[nr][nc] == 0:
                    survivors[idx] = (nr, nc)
                    dist += 1
    return dist

def find_distance(p):
    global exit_r, exit_c
    row_dist, col_dist = abs(exit_r - p[0]), abs(exit_c - p[1])
    dist, start_r, start_c = max(row_dist, col_dist), min(exit_r, p[0]), min(exit_c, p[1])
    
    if row_dist > col_dist:
        start_c = max(exit_c, p[1]) - dist
        if start_c < 0:start_c = 0
    
    if row_dist < col_dist:
        start_r = max(exit_r, p[0]) - dist
        if start_r < 0:start_r = 0
    
    return (dist, start_r, start_c)

def find_square():
    square_tmp = []
    for p in survivors:
        square_tmp.append(find_distance(p))
    return sorted(square_tmp)[0]

def rotate_square(x):
    global survivors, exit_r, exit_c
    dist, start_r, start_c = x
    n_maze = deepcopy(maze)
    n_survivors = []
    n_exit = exit
    for i in range(dist + 1):
        for j in range(dist + 1):
            if n_maze[start_r + i][start_c + j] > 0:   # 채워
                n_maze[start_r + i][start_c + j] -= 1   # 채워
            maze[start_r + i][start_c + j] = n_maze[start_r + dist -j][start_c + i]   # 채워

            while (start_r + i, start_c + j) in survivors:   # 채워
                survivors.remove((start_r + i, start_c + j))   # 채워
                n_survivors.append((start_r + j, start_c + dist - i))   # 채워

            if (start_r + i, start_c + j) == (exit_r, exit_c):   # 채워
                n_exit = (start_r + j, start_c + dist - i)   # 채워
    survivors.extend(n_survivors)
    exit_r, exit_c = n_exit

for _ in range(k):
    res = move_survivors(res)

    while (exit_r, exit_c) in survivors:
        survivors.remove((exit_r, exit_c))
    if not survivors:break

    square = find_square()
    rotate_square(square)

print(res)
print(exit_r + 1, exit_c + 1)