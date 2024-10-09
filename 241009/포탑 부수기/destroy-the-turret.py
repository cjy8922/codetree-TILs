from collections import deque

dy = [0, 1, 0, -1]
dx = [1, 0, -1, 0]

def printBoard(board, N, M):
    for i in range(N):
        for j in range(M):
            print(board[i][j], end=' ')
        print()
    print()


# 공격자 & 수비자 결정
def decideWeakandStrong(board, latestAttackBoard, N, M):
    def _decideWeak(minAttack, minTankPos, i, j):
        if board[i][j] < minAttack:
            minAttack = board[i][j]
            minTankPos = (i, j)
        elif board[i][j] == minAttack:
            if latestAttackBoard[i][j] > latestAttackBoard[minTankPos[0]][minTankPos[1]]:
                minTankPos = (i, j)
            elif latestAttackBoard[i][j] == latestAttackBoard[minTankPos[0]][minTankPos[1]]:
                if i + j > minTankPos[0] + minTankPos[1]:
                    minTankPos = (i, j)
                elif i + j == minTankPos[0] + minTankPos[1]:
                    if j > minTankPos[1]:
                        minTankPos = (i, j)
        return minAttack, minTankPos

    def _decideStrong(maxAttack, maxTankPos, i, j):
        if board[i][j] > maxAttack:
            maxAttack = board[i][j]
            maxTankPos = (i, j)
        elif board[i][j] == maxAttack:
            if latestAttackBoard[i][j] < latestAttackBoard[maxTankPos[0]][maxTankPos[1]]:
                maxTankPos = (i, j)
            elif latestAttackBoard[i][j] == latestAttackBoard[maxTankPos[0]][maxTankPos[1]]:
                if i + j < maxTankPos[0] + maxTankPos[1]:
                    maxTankPos = (i, j)
                elif i + j == maxTankPos[0] + maxTankPos[1]:
                    if j < maxTankPos[1]:
                        maxTankPos = (i, j)
        return maxAttack, maxTankPos

    minAttack,  maxAttack  = 5001, -1
    minTankPos, maxTankPos = (-1, -1), (-1, -1)

    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0: continue
            minAttack, minTankPos = _decideWeak(minAttack, minTankPos, i, j)
            maxAttack, maxTankPos = _decideStrong(maxAttack, maxTankPos, i, j)
    return minTankPos, maxTankPos



# 레이저 공격 or # 포탑 공격
def laserAttack(board, isAttack, minTankPos, maxTankPos, N, M):
    attackPoint = board[minTankPos[0]][minTankPos[1]]

    q = deque([[minTankPos, []]])
    isVisit = [[False] * M for _ in range(N)]
    isVisit[minTankPos[0]][minTankPos[1]] = True

    while q:
        (cur_y, cur_x), route = q.popleft()
        for i in range(4):
            ny, nx = (cur_y + dy[i]) % N, (cur_x + dx[i]) % M
            if isVisit[ny][nx] or board[ny][nx] == 0: continue

            # 목표 도달
            if ny == maxTankPos[0] and nx == maxTankPos[1]:
                board[ny][nx] -= attackPoint
                for ry, rx in route:
                    board[ry][rx] -= (attackPoint // 2)
                    isAttack[ry][rx] = True
                return True, board, isAttack

            currRoute = route[:]
            currRoute.append((ny, nx))
            q.append([(ny, nx), currRoute])
            isVisit[ny][nx] = True
    return False, None, None


def shellAttack(board, isAttack, minTankPos, maxTankPos, N, M):
    attackPoint = board[minTankPos[0]][minTankPos[1]]
    board[maxTankPos[0]][maxTankPos[1]] -= attackPoint

    ddy = dy + [-1, -1, 1, 1]
    ddx = dx + [-1, 1, 1, -1]
    for i in range(8):
        ny, nx = (maxTankPos[0] + ddy[i]) % N, (maxTankPos[1] + ddx[i]) % M
        if ny == minTankPos[0] and nx == minTankPos[1]: continue
        board[ny][nx] -= (attackPoint // 2)
        isAttack[ny][nx] = True
    return board, isAttack

# 포탑 재정비
def check(board, isAttack, N, M):
    alive = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] <= 0: board[i][j] = 0
            if board[i][j] > 0 and not isAttack[i][j]: board[i][j] += 1
            if board[i][j] > 0: alive += 1
            isAttack[i][j] = False
    return alive, board, isAttack


def main():
    N, M, K = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    latestAttackBoard = [[0] * M for _ in range(N)]
    isAttack = [[0] * M for _ in range(N)]

    for turn in range(1, K + 1):

        # 1. 공격자 & 수비자 선정
        minTankPos, maxTankPos = decideWeakandStrong(board, latestAttackBoard, N, M)

        board[minTankPos[0]][minTankPos[1]] += (N+M)
        latestAttackBoard[minTankPos[0]][minTankPos[1]] = turn
        isAttack[minTankPos[0]][minTankPos[1]] = True
        isAttack[maxTankPos[0]][maxTankPos[1]] = True

        # 2. 공격
        canLaserAttack, laserAttackBoard, isLaserAttack = laserAttack(board, isAttack, minTankPos, maxTankPos, N, M)
        if canLaserAttack:
            board = laserAttackBoard
            isAttack = isLaserAttack
        else: board, isAttack = shellAttack(board, isAttack, minTankPos, maxTankPos, N, M)


        # 3. 포탑 재정비
        alive, board, isAttack = check(board, isAttack, N, M)
        if alive <= 1: break

    # 최후 공격자 선언
    print(max([max(line) for line in board]))


if __name__ == "__main__":
    main()