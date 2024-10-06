import sys
input = sys.stdin.readline
from collections import deque as dq

def distance(x, y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

n, m, p, powerC, powerD = map(int, input().split())
r, c = map(int, input().split())
santas = [list(map(int, input().split())) for _ in range(p)]
r -= 1
c -= 1
board = [[0] * n for _ in range(n)]
board[r][c] = -1

# [x, y], 점수, 기절?, 탈락?
santa_is = {i: [[0, 0], 0, 0, False] for i in range(1, p + 1)}
for idx, x, y in santas:
    x -= 1
    y -= 1
    board[x][y] = idx
    santa_is[idx][0] = [x, y]

retired_santa = []

# direction
dx, dy = [
    -1, 0, 1, 0, -1, 1, -1, 1
], [
    0, 1, 0, -1, 1, 1, -1, -1
]
direction_santa = [[0, 2], [3, 1]]
direction_up_down = [0, 2]
direction_left_and_right = [3, 1]

def rudolph_find_santa():
    tmp = []
    for idx in range(1, p + 1):
        if santa_is[idx][3]:
            tmp.append(1e10)
            continue
        x, y = santa_is[idx][0][0], santa_is[idx][0][1]
        tmp.append(distance([x, y], [r, c]))

    min_dist = min(tmp)
    tmp_santas = [idx + 1 for idx, d in enumerate(tmp) if d == min_dist]
    tmp_santas2 = [[santa_is[idx][0], idx] for idx in tmp_santas]
    tmp_santas2.sort(reverse=True)
    return tmp_santas2[0][-1]

def rudolph_find_direction(selected_santa_loc):
    x, y = selected_santa_loc[0], selected_santa_loc[1]
    if x < r:
        if y == c:return 0
        if y < c:return 6
        return 4
    if x > r:
        if y == c:return 2
        if y > c:return 5
        if y < c:return 7
    if y < c:return 3
    return 1

def fight(is_rudolph, toward, santa_idx, x, y):
    global board
    score = powerC if is_rudolph else powerD
    santa_is[santa_idx][1] += score
    santa_is[santa_idx][2] = 2
    if not is_rudolph:
        if toward % 2 == 0:
            toward = direction_up_down[abs(direction_up_down.index(toward) - 1)]
        else:
            toward = direction_left_and_right[abs(direction_left_and_right.index(toward) - 1)]
    
    q = dq()
    q.append([santa_idx, x, y, toward, score])
    while q:
        now_santa_id, x, y, toward, score = q.popleft()
        nx, ny = x + score*dx[toward], y + score*dy[toward]
        if (nx not in range(n)) or (ny not in range(n)):
            santa_is[now_santa_id][3] = True
            retired_santa.append(now_santa_id)
            break
        
        if board[nx][ny] > 0 and board[nx][ny] != now_santa_id:
            q.append([board[nx][ny], nx, ny, toward, 1])
            santa_is[now_santa_id][0] = [nx, ny]
        else:
            santa_is[now_santa_id][0] = [nx, ny]
            break

    board = [[0] * n for _ in range(n)]
    for key, value in santa_is.items():
        if not value[3]:
            board[value[0][0]][value[0][1]] = key
    board[r][c] -= 1
    return


def santa_move(x, y, key):
    dist = distance((x, y), (r, c))
    tmp = []
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if nx not in range(n) or ny not in range(n):continue
        if board[nx][ny] > 0:continue
        dist_tmp = distance((nx, ny), (r, c))
        if dist > dist_tmp:
            dist = dist_tmp
            tmp.append([nx, ny, dist])
    if not tmp:return
    nx, ny, toward = tmp.pop()
    if (r, c) == (nx, ny):
        fight(False, toward, key, nx, ny)
    else:
        santa_is[key][0] = [nx, ny]
        board[x][y] = 0
        board[nx][ny] = key

for _ in range(m):
    if len(retired_santa) == p:break
    for key, value in santa_is.items():
        if value[2] > 0 and not value[3]:
            santa_is[key][2] -= 1
    
    # 루돌프 이동 1. 산타 선택
    selected_santa = rudolph_find_santa()
    # 2. 방향 선택
    rudolph_toward = rudolph_find_direction(santa_is[selected_santa][0])
    # 3. 이동 및 충돌
    board[r][c] = 0
    r += dx[rudolph_toward]
    c += dy[rudolph_toward]
    
    if board[r][c] > 0:
        fight(True, rudolph_toward, board[r][c], r, c)
    board[r][c] = -1

    # 2. 산타 이동
    for key, value in santa_is.items():
        if value[3] or value[2] > 0:continue
        santa_move(value[0][0], value[0][1], key)

    # 3. 탈락하지 않은 산타 + 1점
    for idx in range(1, p + 1):
        if not santa_is[idx][3]:
            santa_is[idx][1] += 1

score = [value[1] for value in santa_is.values()]
print(*score)