import sys
sys.stdin = open('input.txt', 'r')


# 순서 대로 이동 --> 리스트 같은거 써서 순차적으로 처리

# 1. 루돌프 to 가장 가까운 산타 -> 행 큰 순 -> 열 큰 순 (인접한 8방향)
    # 산타와 충돌하면 산타 C점 + C칸 밀림 -> 해당 칸에 산타 있으면 연쇄 밀림
    # 충돌하면 기절 (k턴 -> k+2턴에 정상)
# 2. 산타 to 루돌프 가까워지는 방향 -> 상, 우, 하, 좌 순으로 이동 (산타 있으면 안됨)
    # 루돌프와 충돌하면 산타 D점 + 반대방향으로 D칸 밀림 -> 해당 칸에 산타 있으면 연쇄 밀림
# 3. 모두 탈락하면 종료 or 살아남은 산타는 +1



# 0. 입력
N, M, P, C, D = map(int, input().split())
v = [[0] * N for _ in range(N)]

# 루돌프 초기화
ri, rj = map(lambda x:int(x) - 1, input().split())
v[ri][rj] = -1

# 산타 초기화
score = [0] * (P + 1)
alive = [1] * (P + 1)
alive[0] = 0
wakeup_turn = [1] * (P + 1)
santa = [[N] * 2 for _ in range(P + 1)]
for _ in range(1, P + 1):
    n, i, j = map(int, input().split())
    santa[n] = [i-1, j-1]
    v[i-1][j-1] = n


# 충돌한 산타 + 연쇄 충돌
def move_santa(cur, si, sj, di, dj, val):
    q = [(cur, si, sj, val)]    # cur번 산타를 si, sj에서 di, dj 방향으로 mul칸 이동

    while q:
        cur, ci, cj, val = q.pop(0)
        # 진행방향으로 val 칸 만큼 이동해서 범위 내이고, 산타 있으면 q 삽입
        ni, nj = ci + di * val, cj + dj * val
        if 0<=ni<N and 0<=nj<N:
            if v[ni][nj] == 0:  # 산타가 없으면 빈땅
                v[ni][nj] = cur
                santa[cur] = [ni, nj]
                return
            else:               # 산타가 있으면 반복
                q.append((v[ni][nj], ni, nj, 1))
                v[ni][nj] = cur
                santa[cur] = [ni, nj]
        else:
            alive[cur] = 0 # 범위 밖이면 탈락
            return



# 게임 시작
for time in range(1, M + 1):
    if alive.count(1) == 0: break   # 살아남은 산타가 없으면 게임 종료

    # 1-1. 루돌프 이동 --> 가장 가까운 산타 찾기
    min_dist = N ** 2 + N ** 2 + 1      # 가장 큰값
    min_list = []
    for idx in range(1, P + 1):
        if alive[idx] == 0: continue    # 탈락한 산타는 할 필요 없음
        si, sj = santa[idx]
        dist = (ri - si) **2 + (rj - sj) ** 2
        if dist < min_dist:
            min_dist = dist
            min_list.append((si, sj, idx))
        elif dist == min_dist:
            min_list.append((si, sj, idx))
    min_list = sorted(min_list, reverse=True)
    si, sj, min_idx = min_list[0]   # --> 돌격 목표 산타

    # 1-2. 루돌프 이동 --> 산타 방향으로 이동
    # 항상 산타와 가까워지는 방향으로 움직이기 때문에 루돌프는 항상 범위내 에 있음
    # 루돌프는 항상 산타를 밀어내기 때문에 초기화가 쉬움 (산타의 좌표는 어차피 santa 변수에 저장되어 있음)
    rdi, rdj = 0, 0
    if   ri > si: rdi = -1
    elif ri < si: rdi = 1
    if   rj > sj: rdj = -1
    elif rj < sj: rdj = 1

    v[ri][rj] = 0
    ri, rj = ri + rdi, rj + rdj
    v[ri][rj] = -1

    # 1-3. 루돌프 이동 --> 산타에게 충돌 -> 연쇄 충돌
    # 항상 가장 가까운 산타와 충돌함
    if (ri, rj) == (si, sj):
        score[min_idx] += C
        wakeup_turn[min_idx] = time + 2
        move_santa(min_idx, si, sj, rdi, rdj, C)


    # 2-1. 기절하지 않고 살아남은 산타 --> 루돌프에게로 이동 --> 산타 이동 및 충돌 처리
    for idx in range(1, P + 1):
        if alive[idx] == 0:         continue
        if wakeup_turn[idx] > time: continue

        # 산타의 이동 방향 결정
        si, sj = santa[idx]
        min_dist = (ri - si) ** 2 + (rj - sj) ** 2
        temp_list = []
        for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            ni, nj = si + di, sj + dj
            dist = (ri - ni) ** 2 + (rj - nj) ** 2

            # 범위 내, 산타 없음 (<=0), 더 짧은 거리
            if 0<=ni<N and 0<=nj<N and v[ni][nj] <= 0 and dist < min_dist:
                min_dist = dist
                temp_list.append((ni, nj, di, dj))

        if len(temp_list) == 0: continue # 이동할 위치 없음
        ni, nj, di, dj = temp_list[-1]

        # 산타 이동 --> 루돌프와 충돌
        if (ni, nj) == (ri, rj):
            score[idx] += D
            wakeup_turn[idx] = time + 2
            v[si][sj] = 0
            move_santa(idx, ni, nj, -di, -dj, D)

        # 산타 이동 --> 빈칸으로 이동
        else:
            v[si][sj] = 0
            v[ni][nj] = idx
            santa[idx] = [ni, nj]



    # 3. 점수 획득 (alive +1)
    for i in range(1, P + 1):
        if alive[i] == 1:
            score[i] += 1

print(*score[1:])