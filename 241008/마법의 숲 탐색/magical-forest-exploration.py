from collections import deque

MAX_L = 70
R, C, K = 0, 0, 0
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]
A = [[0] * MAX_L for _ in range(MAX_L + 3)]
isExit = [[0] * MAX_L for _ in range(MAX_L + 3)]
answer = 0


def inRange(y, x):
    flag = (0 <= x) and (x < C) and (3 <= y) and (y < R + 3)
    return flag

def resetMap():
    for i in range(R + 3):
        for j in range(C):
            A[i][j] = 0
            isExit[i][j] = 0

def canGo(y, x):
    flag = (0 <= x - 1) and (x + 1 < C) and (y + 1 < R + 3)
    flag = flag and (A[y - 1][x - 1] == 0)
    flag = flag and (A[y - 1][x] == 0)
    flag = flag and (A[y - 1][x + 1] == 0)
    flag = flag and (A[y][x - 1] == 0)
    flag = flag and (A[y][x] == 0)
    flag = flag and (A[y][x + 1] == 0)
    flag = flag and (A[y + 1][x] == 0)
    return flag


# bfs 방법으로 풀이
def angelMove(y, x):
    result = y
    q = deque([(y, x)])
    isVisit = [[0] * C for _ in range(R + 3)]
    isVisit[y][x] = 1


    while q:
        cur_y, cur_x = q.popleft()
        for i in range(4):
            ny, nx = cur_y + dy[i], cur_x + dx[i]
            canVisit = (inRange(ny, nx)) and (isVisit[ny][nx] == 0)
            canVisit = canVisit and (A[ny][nx] == A[cur_y][cur_x] or (A[ny][nx] != 0 and isExit[cur_y][cur_x] == 1))
            if canVisit:
                q.append((ny, nx))
                isVisit[ny][nx] = 1
                result = max(result, ny)
    return result - 2


def down(y, x, d, id):
    if   canGo(y + 1, x):       down(y + 1, x, d, id)
    elif canGo(y + 1, x - 1):   down(y + 1, x - 1, (d + 3) % 4, id)
    elif canGo(y + 1, x + 1):   down(y + 1, x + 1, (d + 1) % 4, id)
    else:
        if not (inRange(y-1, x-1) and inRange(y+1, x+1)): resetMap()
        else:
            A[y][x] = id
            for i in range(4):
                A[y + dy[i]][x + dx[i]] = id
            isExit[y + dy[d]][x + dx[d]] = 1
            global answer
            answer += angelMove(y, x)

def main():
    global R, C, K
    R, C, K = map(int, input().split())
    for id in range(1, K + 1):
        x, d = map(int, input().split())
        down(0, x - 1, d, id)
    print(answer)


if __name__ == "__main__":
    main()