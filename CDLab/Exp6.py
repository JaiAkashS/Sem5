def constant_folding(expression):
    tokens = expression.split()
    for i in range(len(tokens)):
        if tokens[i].isdigit() and (i > 0 and tokens[i - 1] in ['+', '-', '*', '/']):
            # Look back at the previous operator and the left operand
            if i > 1 and tokens[i - 2].isdigit():
                left_operand = int(tokens[i - 2])
                operator = tokens[i - 1]
                right_operand = int(tokens[i])

                if operator == '+':
                    result = left_operand + right_operand
                elif operator == '-':
                    result = left_operand - right_operand
                elif operator == '*':
                    result = left_operand * right_operand
                elif operator == '/':
                    # Use float division to preserve non-integer results; change to // for integer division
                    result = left_operand / right_operand

                # Replace the operation with the result and recurse
                tokens[i - 2:i + 1] = [str(result)]
                return constant_folding(' '.join(tokens))  # Recurse until no more changes

    return ' '.join(tokens)

expr = input("Enter Expression:")
optimized_expr = constant_folding(expr)
print(f"Original: {expr} | Optimized: {optimized_expr}")