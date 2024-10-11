N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
turn = [[0] * M for _ in range(N)]


from collections import deque
def bfs(si, sj, ei, ej):
    q = deque()
    isVisited = [[[] for _ in range(M)] for _ in range(N)]   # 경로 표시를 위한 리스트

    q.append((si, sj))
    isVisited[si][sj] = (si, sj)
    d = arr[si][sj]
    while q:
        ci, cj = q.popleft()

        if (ci, cj) == (ei, ej):                    # 목적지를 찾았으면
            arr[ei][ej] = max(0, arr[ei][ej] - d)   # 공격 받은 후 음수가 되면 0
            while True:
                ci, cj = isVisited[ci][cj]              # 직전 좌표
                if (ci, cj) == (si, sj): return True    # 시작 좌표이면 공격 끝
                arr[ci][cj] = max(0, arr[ci][cj] - d // 2)
                fight_set.add((ci, cj))

        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):   # 우, 하, 좌, 상
            ni, nj = (ci + di) % N, (cj + dj) % M           # 범위 밖으로 넘어가면 반대편으로 이동1
            if len(isVisited[ni][nj]) == 0 and arr[ni][nj] > 0: # 미방문, 포탑 존재
                q.append((ni, nj))
                isVisited[ni][nj] = (ci, cj)

    # 목적지를 찾지 못했으면
    return False


def bomb(si, sj, ei, ej):
    d = arr[si][sj]
    arr[ei][ej] = max(0, arr[ei][ej] - d)

    # 나를 제외한 목표 좌표 주변 8개에 피해
    for di, dj in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        ni, nj = (ei + di) % N, (ej + dj) % M
        if (ni, nj) != (si, sj):
            arr[ni][nj] = max(0, arr[ni][nj] - d // 2)
            fight_set.add((ni, nj))



for T in range(1, K + 1):
    # 1-1. 공격력 낮은 --> 가장 최근 공격 --> 행 + 열이 클수록 --> 열이 클수록
    mn, mn_turn, si, sj = 5001, 0, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j] <= 0: continue # 포탑이 아니면 스킵
            if arr[i][j] < mn or (arr[i][j] == mn and turn[i][j] > mn_turn) or \
                    (arr[i][j] == mn and turn[i][j] == mn_turn and i + j > si + sj) or \
                    (arr[i][j] == mn and turn[i][j] == mn_turn and i + j == si + sj and j > sj):
                mn, mn_turn, si, sj = arr[i][j], turn[i][j], i, j

    # 선정된 공격자 공격력 증가 + 이번 턴에 공격한다고 알림
    arr[si][sj] += (N + M)
    turn[si][sj] = T

    # 1-2. 공격력 높은 --> 가장 나중에 공격 --> 행 + 열이 작은 --> 열이 작을수록
    mx, mx_turn, ei, ej = 0, 1001, N, M
    for i in range(N):
        for j in range(M):
            if arr[i][j] <= 0: continue # 포탑이 아니면 스킵
            if arr[i][j] > mx or (arr[i][j] == mx and turn[i][j] < mx_turn) or \
                    (arr[i][j] == mx and turn[i][j] == mx_turn and i + j < ei + ej) or \
                    (arr[i][j] == mx and turn[i][j] == mx_turn and i + j == ei + ej and j < ej):
                mx, mx_turn, ei, ej = arr[i][j], turn[i][j], i, j


    # 2. 레이저 공격 (우, 하, 좌, 상) --> 수비자 -> 공격까지 최단 경로 확인
    fight_set = set()
    fight_set.add((si, sj))
    fight_set.add((ei, ej))
    if not bfs(si, sj, ei, ej):

    # 3. 포탑 공격 --> 레이저 공격이 불가하면 공격자 주변 8칸 (이때, 공격자는 제외)
        bomb(si, sj, ei, ej)

    # 4. 재정비 (공격과 상관 없는 포탑은 + 1)
    for i in range(N):
        for j in range(M):
            if (i, j) not in fight_set:
                arr[i][j] += 1

    # 5. 살아남은 포탑이 하나이면 가장 강한 공격력 출력

print(max(map(max, arr)))