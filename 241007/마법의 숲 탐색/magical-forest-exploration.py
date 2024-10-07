from collections import deque

MAX_L = 70
R, C, K = 0, 0, 0
A = [[0] * MAX_L for _ in range(MAX_L + 3)]
isExit = [[0] * MAX_L for _ in range(MAX_L + 3)]
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]
answer = 0

# 맵 초기화
def resetMap():
    for i in range(R + 3):
        for j in range(C):
            A[i][j] = 0
            isExit[i][j] = False

# 골렘이 마법의 숲 내부에 있는가
def inRange(y, x):
    flag = (3<=y) and (y<R+3) and (0<=x) and (x<C)
    return flag

# 골렘이 움직일 수 있는 위치인가
def canGo(y, x):
    flag = (0<=x-1) and (x+1<C) and (y+1<R+3)
    flag = flag and (A[y-1][x-1] == 0)
    flag = flag and (A[y-1][x] == 0)
    flag = flag and (A[y-1][x+1] == 0)
    flag = flag and (A[y][x-1] == 0)
    flag = flag and (A[y][x] == 0)
    flag = flag and (A[y][x+1] == 0)
    flag = flag and (A[y+1][x] == 0)
    return flag

def angelMove(y, x):
    result = y
    q = deque([(y, x)])
    isVisit = [[False] * C for _ in range(R + 3)]
    isVisit[y][x] = True

    while q:
        cur_y, cur_x = q.popleft()
        for i in range(4):
            ny, nx = cur_y + dy[i], cur_x + dx[i]
            canVisit = inRange(ny, nx) and not isVisit[ny][nx]
            canVisit = canVisit and (A[ny][nx] == A[cur_y][cur_x] or (A[ny][nx] != 0 and isExit[cur_y][cur_x] == True))
            if canVisit:
                q.append((ny, nx))
                isVisit[ny][nx] = True
                result = max(result, ny)
    return result - 2

# 골렘의 이동
def down(y, x, d, id):
    if canGo(y+1, x):       down(y+1, x, d, id)         # 남쪽
    elif canGo(y+1, x-1):   down(y+1, x-1, (d+3)%4, id) # 서쪽
    elif canGo(y+1, x+1):   down(y+1, x+1, (d+1)%4, id) # 북쪽
    
    # 골렘의 정착
    else:
        if not (inRange(y-1, x-1) and inRange(y+1, x+1)): resetMap()    # 골렘이 숲 안에 없으면 리셋
        else:                                                           # 골렘이 숲에 있으면 정령 움직임
            A[y][x] = id
            for i in range(4):
                A[y+dy[i]][x+dx[i]] = id

            isExit[y+dy[d]][x+dx[d]] = True
            global answer
            answer += angelMove(y, x)

def main():
    global R, C, K
    R, C, K = map(int, input().split())
    for id in range(1, K+1):
        x, d = map(int, input().split())
        down(0, x - 1, d, id)
    print(answer)


if __name__ == "__main__":
    main()