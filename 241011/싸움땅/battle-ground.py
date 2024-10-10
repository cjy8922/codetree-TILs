N, M, K = map(int, input().split())

# 총의 공격력에 대한 정보
arr = [list(map(int, input().split())) for _ in range(N)]
gun = [[ [] for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j] > 0:
            gun[i][j].append(arr[i][j])
arr = [[0] * N for _ in range(N)]

# 플레이어 정보 (위치, 방향, 능력치, 가지고 있는 총 공격력, 점수)
players = {}
for m in range(1, M + 1):
    x, y, d, s = map(int, input().split())
    players[m] = [x-1, y-1, d, s, 0, 0]
    arr[x-1][y-1] = m

# 방향 정보 (상, 우, 하, 좌)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]
opp = {0:2, 1:3, 2:0, 3:1}


def leave(n, ci, cj, cd, cp, cg, cs):
    # 현재 방향부터 시계방향으로 이동 (최소 내가 온 칸은 비어 있음)
    for k in range(4):
        ni, nj = ci + di[(cd + k) % 4], cj + dj[(cd + k) % 4]
        if 0<=ni<N and 0<=nj<N and arr[ni][nj] == 0:
            # 총이 있으면 가장 강한 총 획득
            if len(gun[ni][nj]) > 0:
                cg = max(gun[ni][nj])
                gun[ni][nj].remove(cg)
            arr[ni][nj] = n
            players[n] = [ni, nj, (cd + k) % 4, cp, cg, cs]
            return


# 게임 시작
for _ in range(K):

    # 1번부터 순서대로 이동
    for player in players:

        # 1. 플레이어 한 칸 이동 (격자에 벗어나면 반대방향으로 이동)
        ci, cj, cd, cp, cg, cs = players[player]
        ni, nj = ci + di[cd], cj + dj[cd]
        if not (0<=ni<N and 0<=nj<N):   # 방향을 벗어남
            cd = opp[cd]
            ni, nj = ci + di[cd], cj + dj[cd]
        arr[ci][cj] = 0 # 이전 위치에서 제거

        # 2-1. 이동한 위치가 빈칸 --> 가장 강한 총 가져오기
        if arr[ni][nj] == 0:
            if len(gun[ni][nj]) > 0:
                mx = max(gun[ni][nj])
                if cg < mx:
                    if cg > 0:
                        gun[ni][nj].append(cg)          # 총이 있는 경우 반납
                    gun[ni][nj].remove(mx)              # 총 가져오기
                    cg = mx
            arr[ni][nj] = player                        # 위치 이동
            players[player] = [ni, nj, cd, cp, cg, cs]  # 정보 갱신

        # 2-2. 빈칸이 아닌 경우 --> 상대방과 싸움
        else:
            enemy = arr[ni][nj]
            ei, ej, ed, ep, eg, es = players[enemy]

            # 내가 이기는 경우 (적보다 공격력이 높음 + 같을 경우, 선천적인 공격력이 좋음)
            if (cp + cg) > (ep + eg) or (cp + cg == ep + eg and cp > ep):
                cs += (cp + cg) - (ep + eg) # 공격력 차이만큼 점수 획득
                leave(enemy, ni, nj, ed, ep, 0, es) # 진 플레이어(상대방)는 총을 놓고 떠남

                # 이긴 플레이어는 가장 강한 총을 얻음 --> 상대방의 총과 내 총만 비교하면 됨
                if cg < eg:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                    cg = eg
                else:
                    if eg> 0:
                        gun[ni][nj].append(eg)

                # 내 정보 업데이트
                arr[ni][nj] = player
                players[player] = [ni, nj, cd, cp, cg, cs]

            # 내가 지는 경우
            else:
                es += (ep + eg) - (cp + cg)
                leave(player, ni, nj, cd, cp, 0, cs)
                if eg < cg:
                    if eg > 0:
                        gun[ni][nj].append(eg)
                    eg = cg
                else:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                arr[ni][nj] = enemy
                players[enemy] = [ni, nj, ed, ep, eg, es]

# 결과 출력
for idx in range(1, M + 1):
    print(players[idx][5], end=' ')