N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
for _ in range(M):
    i, j = map(lambda x: int(x) - 1, input().split())   # 좌표가 (1, 1)부터이기 때문에 -1씩 감소시켜서 (0, 0) 좌표 기준으로 입력
    arr[i][j] -= 1  # 사람은 -1 (같은 위치에 여러명 있을 수 있으므로 -1을 계속 빼줘야함)

ei, ej = map(lambda x: int(x) - 1, input().split())
arr[ei][ej] = -11


def find_square(arr):
    min_dist = N
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0:
                min_dist = min(min_dist, max(abs(ei - i), abs(ej - j)))

    for si in range(N-min_dist):
        for sj in range(N-min_dist):
            if si <= ei <= si + min_dist and sj <= ej <= sj + min_dist:  # 비상구가 포함된 위치
                for i in range(si, si + min_dist + 1):
                    for j in range(sj, sj + min_dist + 1):
                        if -11 < arr[i][j] < 0:
                            return si, sj, min_dist + 1

# 게임 시작
ans = 0
cnt = M

for _ in range(K):

    # 1. 모든 참가자가 동시에 이동 --> 복사 or 0으로 새로운 array 만들기
    new_arr = [x[:] for x in arr]
    for ci in range(N):
        for cj in range(N):
            if -11 < new_arr[ci][cj] < 0:     # 사람인 경우 --> 출구와 가깝게 최단거리로 이동
                dist = abs(ei - ci) + abs(ej - cj)
                # 네 방향, 범위 내, 벽이 아닌 경우, 최단 거리
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = ci + di, cj + dj
                    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] <= 0 and dist > (abs(ei - ni) + abs(ej - nj)):
                        ans += arr[ci][cj]                          # 현재 위치에 있는 모든 인원이 이동해야함
                        new_arr[ci][cj] -= arr[ci][cj]              # 이동
                        if arr[ni][nj] == -11: cnt += arr[ci][cj]               # 비상구이면 탈출
                        else:                  new_arr[ni][nj] += arr[ci][cj]   # 들어온 인원 추가
                        break                                       # 다 하고나면 다른 방향으로 이동할 필요가 없음
    arr = new_arr

    # 모든 참가자가 탈출하면 그대로 게임 끝
    if cnt == 0: break

    # 2. 미로 회전
    # 비상구와 사람을 포함한 가장 작은 정사각형 변 찾기
    si, sj, L = find_square(arr)

    # 시계 방향으로 90도 회전
    new_arr = [x[:] for x in arr]
    for i in range(L):
        for j in range(L):
            new_arr[si + i][sj + j] = arr[si +  L - 1 - j][sj + i]
            if new_arr[si + i][sj + j] > 0:   # 벽이면 회전 시 내구도 감소
                new_arr[si + i][sj + j] -= 1
    arr = new_arr

    # 새로운 비상구 위치 찾기
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -11:
                ei, ej = i, j

print(-ans)
print(ei + 1, ej + 1)