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

    print(f"\nДобавляем образец #{pattern_id}: {pattern}")

    for ch in pattern:
        c = CHAR_ID[ch]

        if nexts[vertex][c] == -1:
            nexts[vertex][c] = len(nexts)
            new_node()

            print(
                f"  Создали вершину {nexts[vertex][c]} "
                f"по символу '{ch}' из вершины {vertex}"
            )
        else:
            print(
                f"  Переход по символу '{ch}' уже есть: "
                f"{vertex} -> {nexts[vertex][c]}"
            )

        vertex = nexts[vertex][c]

    outputs[vertex].append(pattern_id)

    print(f"  Вершина {vertex} стала терминальной для образца #{pattern_id}")


def build_automaton():
    print("\n================ ПОСТРОЕНИЕ АВТОМАТА ================")

    q = deque()

    print("\nОбрабатываем корень:")

    for c in range(5):
        child = nexts[0][c]

        if child != -1:
            go[0][c] = child
            link[child] = 0
            terminal_link[child] = -1
            q.append(child)

            print(
                f"  Из корня по '{ALPHABET[c]}' есть ребро в вершину {child}. "
                f"go[0][{ALPHABET[c]}] = {child}, link[{child}] = 0"
            )
        else:
            go[0][c] = 0

            print(
                f"  Из корня по '{ALPHABET[c]}' ребра нет. "
                f"go[0][{ALPHABET[c]}] = 0"
            )

    while q:
        vertex = q.popleft()

        print(f"\nОбрабатываем вершину {vertex}:")

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

                print(
                    f"  Есть ребро по '{ALPHABET[c]}': {vertex} -> {child}"
                )
                print(
                    f"    Суффиксная ссылка link[{child}] = {link[child]}"
                )
                print(
                    f"    Конечная ссылка terminal_link[{child}] = "
                    f"{terminal_link[child]}"
                )
                print(
                    f"    Автоматный переход go[{vertex}][{ALPHABET[c]}] = {child}"
                )

            else:
                go[vertex][c] = go[link[vertex]][c]

                print(
                    f"  Нет ребра по '{ALPHABET[c]}'. "
                    f"Берём переход по суффиксной ссылке: "
                    f"go[{vertex}][{ALPHABET[c]}] = {go[vertex][c]}"
                )


def suffix_chain_length(vertex):
    length = 0
    current = vertex

    while current != 0:
        current = link[current]
        length += 1

    return length


def final_chain_length(vertex):
    length = 0
    current = terminal_link[vertex]

    while current != -1:
        length += 1
        current = terminal_link[current]

    return length


def print_automaton():
    print("\n================ ПОСТРОЕННЫЙ АВТОМАТ ================")

    max_suffix_chain = 0
    max_final_chain = 0

    for vertex in range(len(nexts)):
        print(f"\nВершина {vertex}:")
        print(f"  Суффиксная ссылка: {link[vertex]}")
        print(f"  Конечная ссылка: {terminal_link[vertex]}")

        print("  Переходы бора:")
        has_trie_edges = False

        for c in range(5):
            if nexts[vertex][c] != -1:
                print(f"    {ALPHABET[c]} -> {nexts[vertex][c]}")
                has_trie_edges = True

        if not has_trie_edges:
            print("    Нет переходов бора")

        print("  Переходы автомата:")
        for c in range(5):
            print(f"    go[{ALPHABET[c]}] = {go[vertex][c]}")

        if outputs[vertex]:
            print(f"  Терминальная вершина. Образцы: {outputs[vertex]}")
        else:
            print("  Не терминальная вершина")

        current_suffix = suffix_chain_length(vertex)
        current_final = final_chain_length(vertex)

        print(f"  Длина цепочки суффиксных ссылок: {current_suffix}")
        print(f"  Длина цепочки конечных ссылок: {current_final}")

        max_suffix_chain = max(max_suffix_chain, current_suffix)
        max_final_chain = max(max_final_chain, current_final)

    print("\n================ ВАРИАНТ 3 ================")
    print(f"Самая длинная цепочка суффиксных ссылок: {max_suffix_chain}")
    print(f"Самая длинная цепочка конечных ссылок: {max_final_chain}")


def main():
    data = sys.stdin.read().splitlines()

    text = data[0].strip()
    n = int(data[1].strip())

    print("================ ВХОДНЫЕ ДАННЫЕ ================")
    print(f"Текст: {text}")
    print(f"Количество образцов: {n}")

    new_node()

    global pattern_length
    pattern_length = [0] * (n + 1)

    print("\n================ ПОСТРОЕНИЕ БОРА ================")

    for i in range(1, n + 1):
        pattern = data[i + 1].strip()
        pattern_length[i] = len(pattern)

        print(f"\nОбразец #{i}: {pattern}, длина = {pattern_length[i]}")
        add_pattern(pattern, i)

    build_automaton()
    print_automaton()

    print("\n================ ПОИСК В ТЕКСТЕ ================")

    answer = []
    state = 0

    for i, ch in enumerate(text):
        c = CHAR_ID[ch]

        old_state = state
        state = go[state][c]

        print(
            f"\nПозиция в тексте: {i + 1}, символ: '{ch}'"
        )
        print(
            f"  Переход автомата: вершина {old_state} -> вершина {state}"
        )

        if outputs[state]:
            print(f"  Вершина {state} терминальная")

        for pattern_id in outputs[state]:
            start_position = i - pattern_length[pattern_id] + 2
            answer.append((start_position, pattern_id))

            print(
                f"  Найден образец #{pattern_id}, "
                f"начальная позиция = {start_position}"
            )

        current = terminal_link[state]

        while current != -1:
            print(f"  Переходим по конечной ссылке в вершину {current}")

            for pattern_id in outputs[current]:
                start_position = i - pattern_length[pattern_id] + 2
                answer.append((start_position, pattern_id))

                print(
                    f"  Через конечную ссылку найден образец #{pattern_id}, "
                    f"начальная позиция = {start_position}"
                )

            current = terminal_link[current]

    answer.sort()

    print("\n================ ИТОГОВЫЙ ОТВЕТ ================")

    for position, pattern_id in answer:
        print(position, pattern_id)


main()