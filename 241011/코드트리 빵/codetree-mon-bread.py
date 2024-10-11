import sys
sys.stdin = open('input.txt', 'r')

# 입력 받기
N, M = map(int, input().split())
arr = [[1] * (N + 2)] + [[1] + list(map(int, input().split())) + [1] for _ in range(N)] + [[1] * (N + 2)]

basecamp = set()
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if arr[i][j] == 1:
            basecamp.add((i, j))
            arr[i][j] = 0           # 다시 0으로 만들어서 갈 수 있는 공간으로 만들기

store = {}
for m in range(1, M + 1):
    i, j = map(int, input().split())
    store[m] = (i, j)


from collections import deque

# 시작 좌표에서 목적지 좌표들(set) 중 최단 거리 동일 반경 리스트를 모두 찾음
def find(si, sj, destination):
    q = deque()
    isVisit = [[0] * (N + 2) for _ in range(N + 2)]
    temp_list = []

    q.append((si, sj))
    isVisit[si][sj] = 1
    while q:
        # 동일 반경까지 처리
        new_q = deque()
        for ci, cj in q:
            if (ci, cj) in destination: # 목적지를 찾음 --> 더 뻗어나갈 필요가 없음
                temp_list.append((ci, cj))

            # 그렇지 않으면~ 네 방향, 미방문, 조건 (arr[][] == 0, 벽이 아니면~)
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni, nj = ci + di, cj + dj
                if isVisit[ni][nj] == 0 and arr[ni][nj] == 0:
                    new_q.append((ni, nj))
                    isVisit[ni][nj] = isVisit[ci][cj] + 1

        # 목적지를 찾으면 리턴
        if len(temp_list) > 0:
            temp_list.sort()
            return temp_list[0]
        q = new_q

    # 올 일은 없겠지만..
    return -1


def solve():
    q = deque()
    time = 1
    arrived = [0] * (M + 1) # 0이면 아직 도착하지 않음

    while q or time == 1:    # 처음 or q에 데이터가 있는 동안 (이동할 사람이 있는 동안) 실행
        # 1. 모두 편의점 방향으로 최단 거리 이동 (이번 time에만 같은 반경)
        new_q = deque()
        arrived_list = []
        for ci, cj, m in q:
            if arrived[m] == 0:
                # 편의점 방향으로 가장 가까운 + 우선순위 높은 destination 선택
                ni, nj = find(
                    store[m][0], store[m][1],
                    set(( (ci - 1, cj), (ci, cj -1), (ci, cj + 1), (ci + 1, cj)) )
                )
                if (ni, nj) == store[m]:
                    arrived[m] = time
                    arrived_list.append((ni, nj))   # 통행 금지는 모두 이동 후 처리해야 하기 때문
                else:
                    new_q.append((ni, nj, m))   # 계속 이동
        q = new_q

        # 2. 편의점 도착 처리 --> arr[][] = 1 (이동 불가 처리)
        if len(arrived_list) > 0:
            for ai, aj in arrived_list:
                arr[ai][aj] = 1

        # 3. 시간 번호의 멤버가 베이스캠프로 순간이동
        if time <= M:
            si, sj = store[time]
            ei, ej = find(si, sj, basecamp) # 가장 가까운 + 우선순위 높은 basecamp 선택
            basecamp.remove((ei, ej))
            arr[ei][ej] = 1            # 이동 불가
            q.append((ei, ej, time))    # 베이스 캠프에서 시작

        time += 1
    return max(arrived)

print(solve())