import sys
input = sys.stdin.readline
from collections import deque as dq
# 방패 : 자신 기준 r, c직사각형 크기
# 체력 k
# 1. 명령 -> 기사 이동
# 다른 기사있으면 한칸씩 밀려남, 끝이 벽이면 이동 못함
# 2. 기사가 다른기사를 밀면
# 밀린 기사는 피해를 입음, 이동후 장소에서 w*h안의 함정 수만큼 피해 입음
# 체력 이상 피해입으면 사라짐,
# 명령 받은 기사 안입음, 모두 밀린 후에 패해 입음

direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
def minus_one(x):
    return int(x) - 1
l, n, q = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(l)]
shields = [[0 for _ in range(l)] for _ in range(l)]
soldiers, shields_dic = [0], {i:[] for i in range(1, n + 1)}
damaged = [0 for _ in range(n + 1)]

for i in range(1, n + 1):
    r, c, h, w, k = map(int, input().split())
    soldiers.append([r - 1, c - 1, h, w, k])
    for j in range(h):
        for e in range(w):
            shields[r - 1 + j][c - 1 + e] = i
            shields_dic[i].append([r - 1 + j, c - 1 + e])

def check_move_soldier(idx, d):
    if soldiers[idx] == 0:return (True, '')
    is_wall = False
    r, c, _, _, _ = soldiers[idx]
    q = dq([(r, c)])
    visit = [[0 for _ in range(l)] for _ in range(l)]
    visit[r][c] = 1
    is_move = [0 for _ in range(n + 1)]
    is_move[idx] = 1
    while q and not is_wall:
        x, y = q.popleft()
        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            if nx in range(l) and ny in range(l):
                if not visit[nx][ny]:
                    if shields[nx][ny] == shields[x][y]:
                        visit[nx][ny] = 1
                        q.append((nx, ny))
            if direction[d] == (dx, dy):
                if nx in range(l) and ny in range(l):
                    if not visit[nx][ny]:
                        if shields[nx][ny] and shields[nx][ny] != shields[x][y]:
                            visit[nx][ny] = 1
                            q.append((nx, ny))
                            is_move[shields[nx][ny]] = 1
                        if board[nx][ny] == 2:
                            is_wall = True
                            break
                else:
                    is_wall = True
                    break
        if is_wall:break
    return (is_wall, is_move)

def move_soldier(move, d):
    tmp_shields = [[0 for _ in range(l)] for _ in range(l)]
    for idx in range(1, n + 1):
        if move[idx] == 1:
            tmp = []
            for x, y in shields_dic[idx]:
                nx, ny = x + direction[d][0], y + direction[d][1]
                tmp_shields[nx][ny] = idx
                tmp.append((nx, ny))
            shields_dic[idx] = tmp
            soldiers[idx][:2] = shields_dic[idx][0]

    for x in range(l):
        for y in range(l):
            if shields[x][y] > 0 and tmp_shields[x][y] == 0:
                if move[shields[x][y]] == 1:
                    shields[x][y] = 0
            if tmp_shields[x][y] > 0:
                shields[x][y] = tmp_shields[x][y]

def check_pitfall(move, first_idx):
    for x in range(l):
        for y in range(l):
            if board[x][y] == 1 and shields[x][y] > 0:
                idx = shields[x][y]
                if move[idx] == 1 and first_idx != idx:
                    if soldiers[idx] != 0:
                        soldiers[idx][-1] -= 1
                        damaged[idx] += 1
                        if soldiers[idx][-1] == 0:
                            for r, c in shields_dic[idx]:
                                shields[r][c] = 0
                            soldiers[idx] = 0
                            damaged[idx] = 0
                            continue

for _ in range(q):
    i, d = map(int, input().split())
    is_wall, is_move = check_move_soldier(i, d)
    if not is_wall:
        move_soldier(is_move, d)
        check_pitfall(is_move, i)

print(sum(damaged))