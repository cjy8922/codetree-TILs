N, M, Q = map(int, input().split())
arr = [[2] * (N + 2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(N)] + [[2] * (N + 2)]

units = {}
v = [[0] * (N + 2) for _ in range(N + 2)]   # --> 디버거로 동작 확인 용
init_k = [0] * (M + 1)
for m in range(1, M + 1):
    si, sj, h, w, k = map(int, input().split())
    units[m] = [si, sj, h, w, k]
    init_k[m] = k
    for i in range(si, si + h):     # --> 기사 좌표 찍기
        v[i][sj: sj + w] = [m] * w  # --> 기사 좌표 찍기


di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def push_unit(start, dr):
    # s를 dr방향으로 밀고 연쇄 처리...
    q = []              # push 후보들 저장
    push_set = set()    # 이동 기사 번호 저장
    damage = [0] * (M + 1)

    q.append(start)
    push_set.add(start)
    while q:
        cur_idx = q.pop(0)
        ci, cj, h, w, k = units[cur_idx]

        # 초기 기사를 명령 받은 방향으로 이동
        ni, nj = ci + di[dr], cj + dj[dr]
        for i in range(ni, ni + h):
            for j in range(nj, nj + w):
                if arr[i][j] == 2: return # 벽이면 움직일 수 없음
                if arr[i][j] == 1:        # 함정이라면 데미지 누적
                    damage[cur_idx] += 1

        # 겹치는 다른 기사가 있으면 큐에 추가
        for idx in units:
            if idx in push_set: continue    # 기존에 움직일 대상에 있으면 체크하지 않음
            ti, tj, th, tw, tk = units[idx]

            # ★ 겹치는 지 확인
            if (ni <= ti + th - 1) and (ni + h - 1 >= ti) and \
                    (nj <= tj + tw - 1) and (nj + w - 1 >= tj):
                q.append(idx)
                push_set.add(idx)

    # 명령받은 기사는 데미지를 받지 않음
    damage[start] = 0

    # 나머지 기사는 이동 및 데미지가 체력 이상 입으면 삭제
    for idx in push_set:
        si, sj, h, w, k = units[idx]
        if k <= damage[idx]: units.pop(idx)
        else:
            ni, nj = si + di[dr], sj + dj[dr]
            units[idx] = [ni, nj, h, w, k - damage[idx]]



# 명령을 받아 있는 유닛들만 처리
for _ in range(Q):
    idx, dr = map(int, input().split())
    if idx in units:       # 존재하는 유닛만 명령 처리
        push_unit(idx, dr) # 명령 받은 기사를 연쇄적으로 미는 작업 (벽이 없으면)


ans = 0
for idx in units:
    ans += init_k[idx] - units[idx][4] # (초기 체력 - 현재 체력 == 데미지 누적 값)
print(ans)