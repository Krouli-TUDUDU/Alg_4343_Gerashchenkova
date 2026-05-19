from collections import deque
import sys

ALPHABET = "ACGTN"
CHAR_ID = {ch: i for i, ch in enumerate(ALPHABET)}

nexts = []
go = []
link = []
terminal_link = []
outputs = []
blocks = []


def new_node():
    nexts.append([-1] * 5)
    go.append([0] * 5)
    link.append(0)
    terminal_link.append(-1)
    outputs.append([])


def split_pattern(pattern, wildcard):
    i = 0
    m = len(pattern)

    while i < m:
        while i < m and pattern[i] == wildcard:
            i += 1

        if i >= m:
            break

        start = i
        block = []

        while i < m and pattern[i] != wildcard:
            block.append(pattern[i])
            i += 1

        blocks.append(("".join(block), start))


def add_block(block, block_id):
    vertex = 0

    for ch in block:
        c = CHAR_ID[ch]

        if nexts[vertex][c] == -1:
            nexts[vertex][c] = len(nexts)
            new_node()

        vertex = nexts[vertex][c]

    outputs[vertex].append(block_id)


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
    pattern = data[1].strip()
    wildcard = data[2].strip()[0]

    text_length = len(text)
    pattern_length = len(pattern)

    split_pattern(pattern, wildcard)

    new_node()

    for i, block in enumerate(blocks):
        add_block(block[0], i)

    build_automaton()

    possible_starts_count = max(0, text_length - pattern_length + 1)
    matches_count = [0] * possible_starts_count

    state = 0

    for i, ch in enumerate(text):
        c = CHAR_ID[ch]
        state = go[state][c]

        for block_id in outputs[state]:
            block_value, block_offset = blocks[block_id]
            block_length = len(block_value)

            block_start_in_text = i - block_length + 1
            possible_pattern_start = block_start_in_text - block_offset

            if 0 <= possible_pattern_start < possible_starts_count:
                matches_count[possible_pattern_start] += 1

        current = terminal_link[state]

        while current != -1:
            for block_id in outputs[current]:
                block_value, block_offset = blocks[block_id]
                block_length = len(block_value)

                block_start_in_text = i - block_length + 1
                possible_pattern_start = block_start_in_text - block_offset

                if 0 <= possible_pattern_start < possible_starts_count:
                    matches_count[possible_pattern_start] += 1

            current = terminal_link[current]

    need_blocks = len(blocks)
    answer = []

    for start in range(possible_starts_count):
        if matches_count[start] == need_blocks:
            answer.append(str(start + 1))

    print("\n".join(answer))


main()




