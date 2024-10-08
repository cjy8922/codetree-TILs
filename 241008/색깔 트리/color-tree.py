MAX_ID = 100000 + 1
MAX_DEPTH = 100 + 1
MAX_COLOR = 5   + 1


class Node:
    def __init__(self):
        self.id         = 0
        self.color      = 0
        self.maxDepth   = 0
        self.parentID   = 0
        self.childIDs   = []
        self.lastUpdate = 0

nodes = [Node() for _ in range(MAX_ID)]
isRoot = [0] * MAX_ID

# LAZY UPDATE
def addNode(query, time):
    mid, pid, color, maxDepth = query[1:]
    if pid == -1: isRoot[mid] = 1
    if canMakeNode(mid, pid):
        nodes[mid].id       = mid
        nodes[mid].color    = color
        nodes[mid].maxDepth = maxDepth
        nodes[mid].parentID = 0 if isRoot[mid] == 1 else pid
        if isRoot[mid] == 0: nodes[pid].childIDs.append(mid)
        nodes[mid].lastUpdate = time

def canMakeNode(mid, pid):
    def _checkMaxDepth(Node, curDepth):
        if Node.id == 0:              return True   # 제일 최상위 노드
        if Node.maxDepth <= curDepth: return False  # 부모 노드의 maxDepth 보다 크면 안됨
        return _checkMaxDepth(nodes[Node.parentID], curDepth + 1)
    
    # 새로운 루트 노드 or 부모 노드의 MaxDepth보다 넘지 않기
    flag = isRoot[mid] or _checkMaxDepth(nodes[pid], 1)
    return flag

# LAZY UPDATE
def changeColor(query, time):
    mid, color = query[1:]
    nodes[mid].color = color
    nodes[mid].lastUpdate = time


def getColor(query):
    def _getColor(Node):
        if Node.id == 0: return 0, 0            # 최상위 노드 (재귀 빠져 나오는 포인트)

        # 부모 노드의 색이 바뀐 시간이 현재 노드가 추가된 시간보다 빠르다면, 현재 노드의 정보 return
        # 그렇지 않다면 부모 노드의 정보 return
        info = _getColor(nodes[Node.parentID])
        if info[1] < Node.lastUpdate: return Node.color, Node.lastUpdate
        else:                         return info

    mid = query[1]
    color, _ = _getColor(nodes[mid])
    print(color)


def getScore(query):
    def _getScore(Node, color, lastUpdate):
        result = [0, [0] * MAX_COLOR]

        # 가장 최신 정보로 업데이트
        if lastUpdate < Node.lastUpdate:    
            lastUpdate = Node.lastUpdate
            color      = Node.color
        result[1][color] = 1

        for childID in Node.childIDs:
            subResult = _getScore(nodes[childID], color, lastUpdate)
            result[1] = [result[1][k] + subResult[1][k] for k in range(MAX_COLOR)]
            result[0] += subResult[0]

        temp_score = 0
        for i in range(1, MAX_COLOR):
            temp_score += 1 if result[1][i] != 0 else 0
        temp_score = temp_score * temp_score
        result[0] += temp_score
        return result

    score = 0
    for i in range(1, MAX_ID):
        if isRoot[i] == 1:
            score += _getScore(nodes[i], nodes[i].color, nodes[i].lastUpdate)[0]
    print(score)



def main():
    commandNum = int(input())
    for i in range(1, commandNum + 1):
        query = list(map(int, input().split()))
        if query[0] == 100:     addNode(query, i)
        elif query[0] == 200:   changeColor(query, i)
        elif query[0] == 300:   getColor(query)
        elif query[0] == 400:   getScore(query)


if __name__ == "__main__":
    main()