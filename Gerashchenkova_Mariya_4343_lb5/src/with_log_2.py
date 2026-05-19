import sys
from collections import deque

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
    print("\n================ РАЗБИЕНИЕ ШАБЛОНА НА БЛОКИ ================")

    i = 0
    m = len(pattern)

    while i < m:
        while i < m and pattern[i] == wildcard:
            print(f"Позиция {i}: джокер '{wildcard}', пропускаем")
            i += 1

        if i >= m:
            break

        start = i
        block = []

        while i < m and pattern[i] != wildcard:
            block.append(pattern[i])
            i += 1

        block_value = "".join(block)
        blocks.append((block_value, start))

        print(
            f"Найден обычный блок: '{block_value}', "
            f"смещение в шаблоне = {start}"
        )


def add_block(block, block_id):
    vertex = 0

    print(
        f"\nДобавляем блок #{block_id}: '{block}', "
        f"смещение = {blocks[block_id][1]}"
    )

    for ch in block:
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

    outputs[vertex].append(block_id)

    print(f"  Вершина {vertex} стала терминальной для блока #{block_id}")


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
                print(f"    Суффиксная ссылка link[{child}] = {link[child]}")
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
            print(f"  Терминальная вершина. Блоки: {outputs[vertex]}")
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
    pattern = data[1].strip()
    wildcard = data[2].strip()[0]

    text_length = len(text)
    pattern_length = len(pattern)

    print("================ ВХОДНЫЕ ДАННЫЕ ================")
    print(f"Текст: {text}")
    print(f"Шаблон: {pattern}")
    print(f"Символ джокера: {wildcard}")
    print(f"Длина текста: {text_length}")
    print(f"Длина шаблона: {pattern_length}")

    split_pattern(pattern, wildcard)

    print("\nПолученные блоки:")
    for i, block in enumerate(blocks):
        print(
            f"  Блок #{i}: '{block[0]}', "
            f"смещение в шаблоне = {block[1]}"
        )

    print("\n================ ПОСТРОЕНИЕ БОРА ================")

    new_node()

    for i, block in enumerate(blocks):
        add_block(block[0], i)

    build_automaton()
    print_automaton()

    print("\n================ ПОИСК В ТЕКСТЕ ================")

    possible_starts_count = max(0, text_length - pattern_length + 1)
    matches_count = [0] * possible_starts_count

    state = 0

    for i, ch in enumerate(text):
        c = CHAR_ID[ch]

        old_state = state
        state = go[state][c]

        print(f"\nПозиция в тексте: {i + 1}, символ: '{ch}'")
        print(f"  Переход автомата: вершина {old_state} -> вершина {state}")

        for block_id in outputs[state]:
            block_value, block_offset = blocks[block_id]
            block_length = len(block_value)

            block_start_in_text = i - block_length + 1
            possible_pattern_start = block_start_in_text - block_offset

            print(f"  Найден блок #{block_id}: '{block_value}'")
            print(f"    Блок начинается в тексте с позиции {block_start_in_text + 1}")
            print(
                f"    Возможное начало всего шаблона: "
                f"{possible_pattern_start + 1}"
            )

            if 0 <= possible_pattern_start < possible_starts_count:
                matches_count[possible_pattern_start] += 1

                print(
                    f"    Счётчик для позиции {possible_pattern_start + 1} "
                    f"увеличен до {matches_count[possible_pattern_start]}"
                )
            else:
                print("    Начало шаблона выходит за границы текста")

        current = terminal_link[state]

        while current != -1:
            print(f"  Переходим по конечной ссылке в вершину {current}")

            for block_id in outputs[current]:
                block_value, block_offset = blocks[block_id]
                block_length = len(block_value)

                block_start_in_text = i - block_length + 1
                possible_pattern_start = block_start_in_text - block_offset

                print(f"  Через конечную ссылку найден блок #{block_id}: '{block_value}'")
                print(f"    Блок начинается в тексте с позиции {block_start_in_text + 1}")
                print(
                    f"    Возможное начало всего шаблона: "
                    f"{possible_pattern_start + 1}"
                )

                if 0 <= possible_pattern_start < possible_starts_count:
                    matches_count[possible_pattern_start] += 1

                    print(
                        f"    Счётчик для позиции {possible_pattern_start + 1} "
                        f"увеличен до {matches_count[possible_pattern_start]}"
                    )
                else:
                    print("    Начало шаблона выходит за границы текста")

            current = terminal_link[current]

    need_blocks = len(blocks)

    print("\n================ ПРОВЕРКА ПОЗИЦИЙ ================")
    print(f"Для полного совпадения нужно найденных блоков: {need_blocks}")

    answer = []

    for start in range(possible_starts_count):
        print(
            f"Позиция {start + 1}: найдено блоков "
            f"{matches_count[start]} из {need_blocks}"
        )

        if matches_count[start] == need_blocks:
            answer.append(start + 1)
            print(f"  Полное совпадение шаблона с позиции {start + 1}")

    print("\n================ ИТОГОВЫЙ ОТВЕТ ================")

    for position in answer:
        print(position)


main()