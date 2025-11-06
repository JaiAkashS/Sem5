from collections import defaultdict
import copy

# ---------- Input Section ----------
def read_grammar():
    print("Enter augmented grammar (one rule per line, blank line to end):")
    grammar = defaultdict(list)
    start_symbol = None

    while True:
        line = input().strip()
        if not line:
            break
        lhs, rhs = line.split("->")
        lhs, rhs = lhs.strip(), rhs.strip()
        if start_symbol is None:
            start_symbol = lhs  # first rule's LHS is assumed start symbol
        for production in rhs.split("|"):
            grammar[lhs].append(list(production.strip()))
    return grammar, start_symbol


# ---------- Utility ----------
def is_nonterminal(symbol):
    return symbol.isupper() or (symbol.endswith("'") and symbol[:-1].isupper())


# ---------- Closure ----------
def closure(items, grammar):
    closure_set = set(items)
    added = True
    while added:
        added = False
        new_items = set()
        for (lhs, rhs, dot_pos) in closure_set:
            if dot_pos < len(rhs):
                symbol = rhs[dot_pos]
                if is_nonterminal(symbol):
                    for prod in grammar[symbol]:
                        new_item = (symbol, tuple(prod), 0)
                        if new_item not in closure_set:
                            new_items.add(new_item)
        if new_items:
            closure_set |= new_items
            added = True
    return frozenset(closure_set)


# ---------- Goto ----------
def goto(items, symbol, grammar):
    moved = []
    for (lhs, rhs, dot_pos) in items:
        if dot_pos < len(rhs) and rhs[dot_pos] == symbol:
            moved.append((lhs, rhs, dot_pos + 1))
    return closure(moved, grammar) if moved else frozenset()


# ---------- FIRST & FOLLOW ----------
def first_of_symbol(symbol, grammar):
    first = set()
    if not is_nonterminal(symbol):
        first.add(symbol)
        return first
    for prod in grammar[symbol]:
        first.add(prod[0])
    return first


def compute_follow(grammar, start_symbol):
    follow = defaultdict(set)
    follow[start_symbol].add('$')
    changed = True

    while changed:
        changed = False
        for A in grammar:
            for production in grammar[A]:
                for i, B in enumerate(production):
                    if is_nonterminal(B):
                        if i + 1 < len(production):
                            beta = production[i + 1]
                            if is_nonterminal(beta):
                                before = len(follow[B])
                                follow[B] |= first_of_symbol(beta, grammar) - {''}
                                if len(follow[B]) > before:
                                    changed = True
                            else:
                                if beta not in follow[B]:
                                    follow[B].add(beta)
                                    changed = True
                        else:
                            before = len(follow[B])
                            follow[B] |= follow[A]
                            if len(follow[B]) > before:
                                changed = True
    return follow


# ---------- Canonical Collection ----------
def canonical_collection(grammar, start_symbol):
    start_item = (start_symbol, tuple(grammar[start_symbol][0]), 0)
    C = [closure([start_item], grammar)]
    transitions = []

    symbols = set(sum([sum(v, []) for v in grammar.values()], []))

    while True:
        added = False
        for I in C.copy():
            for X in symbols:
                goto_set = goto(I, X, grammar)
                if goto_set and goto_set not in C:
                    C.append(goto_set)
                    added = True
                if goto_set:
                    transitions.append((C.index(I), X, C.index(goto_set)))
        if not added:
            break

    return C, transitions


# ---------- Parse Table Construction ----------
def construct_table(C, transitions, grammar, follow, start_symbol):
    ACTION = defaultdict(dict)
    GOTO = defaultdict(dict)

    trans_dict = defaultdict(list)
    for (i, X, j) in transitions:
        trans_dict[i].append((X, j))

    for i, I in enumerate(C):
        for (lhs, rhs, dot_pos) in I:
            if dot_pos < len(rhs):
                a = rhs[dot_pos]
                if not is_nonterminal(a):
                    for (X, j) in trans_dict[i]:
                        if X == a:
                            ACTION[i][a] = f"shift {j}"
            else:
                if lhs != start_symbol:
                    for a in follow[lhs]:
                        ACTION[i][a] = f"reduce {lhs} -> {''.join(rhs)}"
                else:
                    ACTION[i]['$'] = "accept"

        for (X, j) in trans_dict[i]:
            if is_nonterminal(X):
                GOTO[i][X] = j

    return ACTION, GOTO


# ---------- Main ----------
if __name__ == "__main__":
    grammar, start_symbol = read_grammar()
    follow = compute_follow(grammar, start_symbol)
    C, transitions = canonical_collection(grammar, start_symbol)
    ACTION, GOTO = construct_table(C, transitions, grammar, follow, start_symbol)

    print("\n--- Canonical LR(0) Item Sets ---")
    for i, I in enumerate(C):
        print(f"\nState {i}:")
        for (lhs, rhs, dot_pos) in I:
            before = ''.join(rhs[:dot_pos])
            after = ''.join(rhs[dot_pos:])
            print(f"  {lhs} → {before}•{after}")

    print("\n--- ACTION Table ---")
    for i in sorted(ACTION):
        print(f"{i}: {ACTION[i]}")

    print("\n--- GOTO Table ---")
    for i in sorted(GOTO):
        print(f"{i}: {GOTO[i]}")
