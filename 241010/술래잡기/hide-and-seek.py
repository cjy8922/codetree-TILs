N, M, H, K = map(int, input().split())

# 도망자 초기화 (좌 우 하 상)
arr = [list(map(int, input().split())) for _ in range(M)]
di = [ 0, 0, 1, -1]
dj = [-1, 1, 0,  0]
opp = {0:1, 1:0, 2:3, 3:2}  # 반대 방향

# 나무 좌표 초기화
tree = set()
for _ in range(H):
    i,j=map(int, input().split())
    tree.add((i,j))

# 술래의 이동 초기화 (상 우 하 좌)
tdi = [-1, 0, 1,  0]
tdj = [ 0, 1, 0, -1]
max_cnt, cnt, flag, val = 1, 0, 0, 1
tm = (N + 1) // 2
ti, tj, td = tm, tm, 0

# 게임 시작
ans = 0
for k in range(1, K+1):
    # 1. 도망자의 이동 (arr)
    for i in range(len(arr)):
        if abs(arr[i][0] - ti) + abs(arr[i][1] - tj) <= 3: # 술래와 거리가 3 이하인 경우 이동
            ni, nj = arr[i][0] + di[arr[i][2]], arr[i][1] + dj[arr[i][2]]

            if 1<=ni<=N and 1<=nj<=N: # 이동 방향이 범위 안인 경우 --> 술래 체크 --> 없으면 이동
                if (ni, nj) != (ti, tj):
                    arr[i][0], arr[i][1] = ni, nj
            else:                     # 범위 밖인 경우 방향 반대 --> 술래 체크 --> 없으면 이동
                nd = opp[arr[i][2]]
                ni, nj = arr[i][0] + di[nd], arr[i][1] + dj[nd]
                if (ni, nj) != (ti, tj):
                    arr[i] = [ni, nj, nd]
                else:
                    arr[i][2] = nd

    # 2. 술래의 이동
    cnt += 1
    ti, tj = ti + tdi[td], tj + tdj[td]
    if (ti, tj) == (1, 1):      # 안쪽으로 동작하는 달팽이 형태로 변형
        max_cnt, cnt, flag, val = N, 1, 1, -1
        td = 2
    elif (ti, tj) == (M, M):    # 바깥쪽으로 동작하는 달팽이 형태로 변형
        max_cnt, cnt, flag, val = 1, 0, 0, 1
        td = 0
    else:
        if cnt == max_cnt:      # 방향을 바꿀 지점에 도달
            cnt = 0             # 초기화
            td = (td + val) % 4 # 방향을 바꿈 (상, 우, 하, 좌 순으로)
            if flag == 0:
                flag = 1
            else:
                flag = 0
                max_cnt += val

    # 3. 도망자 잡기 --> 술래자리포함 3칸 + 나무가 없는 도망자면 잡힘
    t_set = set(((ti, tj), (ti + tdi[td], tj + tdj[td]), (ti + tdi[td] * 2, tj + tdj[td] * 2)))
    for i in range(len(arr) -1, -1, -1):
        if (arr[i][0], arr[i][1]) in t_set and (arr[i][0], arr[i][1]) not in tree:
            arr.pop(i)
            ans += k

    # 4. 도망자가 없으면 점수도 없음
    if not arr: break

print(ans)