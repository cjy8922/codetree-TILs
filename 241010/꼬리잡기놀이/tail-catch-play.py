import sys
sys.stdin = open('input.txt', 'r')

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

# 1. 팀 구성
from collections import deque
def bfs(si, sj, team_n):
    q = deque()
    team = []

    q.append((si, sj))
    v[si][sj] = 1
    team.append((si, sj))
    arr[si][sj] = team_n

    while q:
        ci, cj = q.popleft()
        # 4방향 범위 내, 미방문, 조건:2 or 출발지가 아닌 곳에서 온 3
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci + di, cj + dj
            if 0<=ni<N and 0<=nj<N and v[ni][nj] == 0:
                if arr[ni][nj] == 2 or (arr[ni][nj] == 3 and (ci, cj) != (si, sj)):
                    q.append((ni, nj))
                    v[ni][nj] = 1
                    team.append((ni, nj))
                    arr[ni][nj] = team_n
    teams[team_n] = team

v = [[0] * N for _ in range(N)]
team_n = 5
teams = {}

for i in range(N):
    for j in range(N):
        # 머리 위치인 경우 Team 생성
        if v[i][j] == 0 and arr[i][j] == 1:
            bfs(i, j, team_n)
            team_n += 1

# 2. 게임 시작
di = [0, -1, 0, 1]
dj = [1, 0, -1, 0]
ans = 0
for k in range(K): # 0부터 k-1까지 진행

    # 2-1. 머리 방향으로 이동
    for team in teams.values(): # 팀별로 순서대로 이동
        ei, ej = team.pop()     # 꼬리 좌표 삭제
        arr[ei][ej] = 4         # 이동 선으로 복원
        si, sj = team[0]        # 머리 좌표 가져오기

        # 범위 내 인접한 네 방향에서 4인 값으로 진행
        for ni, nj in ((si-1, sj), (si + 1, sj), (si, sj - 1), (si, sj + 1)):
            if 0<=ni<N and 0<=nj<N and arr[ni][nj] == 4:
                team.insert(0, (ni, nj))    # 새 머리 좌표를 제일 앞에 추가
                arr[ni][nj] = arr[si][sj]   # 새 머리 좌표에 팀 번호 적기
                break

    # 2-2. 라운드 번호에 맞게 방향과 시작 위치 계산
    # 라운드 수로 방향 계산
    dr = (k // N) % 4
    offset = k % N
    # 라운드 수로 시작 위치 계산
    if dr == 0:     ci, cj = offset, 0          # 우측 (시작 행, 첫번째 열)
    elif dr == 1:   ci, cj = N-1, offset        # 하측 (마지막 행, 시작 열)
    elif dr == 2:   ci, cj = N-1-offset, N-1    # 좌측 (시작 행, 마지막 열)
    else:           ci, cj = 0, N-1-offset      # 상측 (첫번째 행, 시작 열)

    # 2-3. 공을 던지고, 공을 받은 사람 점수 추가 및 방향 반전
    for _ in range(N):
        if 0<=ci<N and 0<=cj<N and arr[ci][cj] > 4:
            team_n = arr[ci][cj]
            ans += (teams[team_n].index((ci, cj)) + 1) ** 2 # (맞은 사람 좌표 인덱스 + 1) ** 2
            teams[team_n] = teams[team_n][::-1]             # 방향 뒤집기
            break
        ci, cj = ci + di[dr], cj + dj[dr]

print(ans)