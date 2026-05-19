import sys
from collections import deque

ALPHABET = "ACGTN"
CHAR_ID = {ch: i for i, ch in enumerate(ALPHABET)}

nexts = []
go = []
link = []
terminal_link = []
outputs = []
pattern_length = []


def new_node():
    nexts.append([-1] * 5)
    go.append([0] * 5)
    link.append(0)
    terminal_link.append(-1)
    outputs.append([])


def add_pattern(pattern, pattern_id):
    vertex = 0

    for ch in pattern:
        c = CHAR_ID[ch]

        if nexts[vertex][c] == -1:
            nexts[vertex][c] = len(nexts)
            new_node()

        vertex = nexts[vertex][c]

    outputs[vertex].append(pattern_id)


def build_automaton():
    q = deque()

    for c in range(5):
        child = nexts[0][c]

        if child != -1:
            go[0][c] = child
            link[child] = 0
            terminal_link[child] = -1
            q.append(child)
        else:
            go[0][c] = 0

    while q:
        vertex = q.popleft()

        for c in range(5):
            child = nexts[vertex][c]

            if child != -1:
                link[child] = go[link[vertex]][c]

                suffix_vertex = link[child]

                if outputs[suffix_vertex]:
                    terminal_link[child] = suffix_vertex
                else:
                    terminal_link[child] = terminal_link[suffix_vertex]

                go[vertex][c] = child
                q.append(child)

            else:
                go[vertex][c] = go[link[vertex]][c]


def main():
    data = sys.stdin.read().splitlines()

    text = data[0].strip()
    n = int(data[1].strip())

    new_node()

    global pattern_length
    pattern_length = [0] * (n + 1)

    for i in range(1, n + 1):
        pattern = data[i + 1].strip()
        pattern_length[i] = len(pattern)
        add_pattern(pattern, i)

    build_automaton()

    answer = []
    state = 0

    for i, ch in enumerate(text):
        c = CHAR_ID[ch]
        state = go[state][c]

        for pattern_id in outputs[state]:
            start_position = i - pattern_length[pattern_id] + 2
            answer.append((start_position, pattern_id))

        current = terminal_link[state]

        while current != -1:
            for pattern_id in outputs[current]:
                start_position = i - pattern_length[pattern_id] + 2
                answer.append((start_position, pattern_id))

            current = terminal_link[current]

    answer.sort()

    result = []
    for position, pattern_id in answer:
        result.append(f"{position} {pattern_id}")

    print("\n".join(result))


main()



