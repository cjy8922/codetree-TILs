from collections import deque


N_LARGE = 5
N_SMALL = 3

def rotateBoard(board, sy, sx, rotateCount):
    resultBoard = [row[:] for row in board]
    for _ in range(rotateCount):
        # (sy, sx)는 좌상단
        temp = resultBoard[sy + 0][sx + 2]
        resultBoard[sy + 0][sx + 2] = resultBoard[sy + 0][sx + 0]
        resultBoard[sy + 0][sx + 0] = resultBoard[sy + 2][sx + 0]
        resultBoard[sy + 2][sx + 0] = resultBoard[sy + 2][sx + 2]
        resultBoard[sy + 2][sx + 2] = temp
        temp = resultBoard[sy + 1][sx + 2]
        resultBoard[sy + 1][sx + 2] = resultBoard[sy + 0][sx + 1]
        resultBoard[sy + 0][sx + 1] = resultBoard[sy + 1][sx + 0]
        resultBoard[sy + 1][sx + 0] = resultBoard[sy + 2][sx + 1]
        resultBoard[sy + 2][sx + 1] = temp
    return resultBoard


def inRange(y, x):
    return 0<=y and y<N_LARGE and 0<=x and x<N_LARGE


def calculateValue(board):
    score = 0
    isVisit = [[False] * N_LARGE for _ in range(N_LARGE)]
    dy = [-1, 0, 1, 0]
    dx = [0, 1, 0, -1]

    # 모든 위치에서 유적 탐색
    for i in range(N_LARGE):
        for j in range(N_LARGE):
            if not isVisit[i][j]:
                q, trace = deque([(i, j)]), deque([(i, j)])
                isVisit[i][j] = True
                while q:
                    cur_y, cur_x = q.popleft()
                    for dir in range(4):
                        ny, nx = cur_y + dy[dir], cur_x + dx[dir]
                        if inRange(ny, nx) and not isVisit[ny][nx] and board[cur_y][cur_x] == board[ny][nx]:
                            q.append((ny, nx))
                            trace.append((ny, nx))
                            isVisit[ny][nx] = True

                # 만약 맞다면 유적 점수 추가 + 유적 초기화
                if len(trace) >= 3:
                    score += len(trace)
                    while trace:
                        pos_y, pos_x = trace.popleft()
                        board[pos_y][pos_x] = 0
    return score, board


def fillBoard(board, queue):
    for x in range(N_LARGE):
        for y in reversed(range(N_LARGE)):
            if board[y][x] == 0:
                board[y][x] = queue.popleft()
    return board


def main():
    # 입력 받기
    K, M = map(int, input().split())
    board = []
    for i in range(N_LARGE):
        board.append(list(map(int, input().split())))
    queue = deque()
    m = list(map(int, input().split()))
    for i in m:
        queue.append(i)


    # 유적 탐사 반복
    for _ in range(K):
        results = 0

        # 유적 회전
        maxScore = 0
        maxScoreBoard = None

        # 각 위치에서 총 3번 회전 (90, 180, 270)
        # 해당 위치에서 얻을 수 있는 가치 계산
        # 1. 가치 최대, 2. 적은 회전 각도, 3. 열이 작음, 4. 행이 작음
        for rotateCount in range(1, 4):
            for sx in range(N_LARGE - N_SMALL + 1):
                for sy in range(N_LARGE - N_SMALL + 1):
                    rotatedBoard = rotateBoard(board, sy, sx, rotateCount)
                    score, scoredBoard = calculateValue(rotatedBoard)
                    if maxScore < score:
                        maxScore = score
                        maxScoreBoard = scoredBoard

        # 더이상 찾을 수 있는 유물이 없으면 나올 것
        if maxScoreBoard is None: break
        results += maxScore
        board = maxScoreBoard

        # 유물 채워 넣기
        while True:
            board = fillBoard(board, queue)
            score, board = calculateValue(board)
            if score == 0: break
            results += score

        print(results, end=' ')


if __name__ == "__main__":
    main()