import re
def algebraic_optimize(expr):
# Step 1: Constant folding
    expr = re.sub(r'(\d+)\s*\+\s*(\d+)', lambda m: str(int(m[1]) + int(m[2])), expr)
    expr = re.sub(r'(\d+)\s*-\s*(\d+)', lambda m: str(int(m[1]) - int(m[2])), expr)
    expr = re.sub(r'(\d+)\s*\*\s*(\d+)', lambda m: str(int(m[1]) * int(m[2])), expr)
    expr = re.sub(r'(\d+)\s*/\s*(\d+)', lambda m: str(int(int(m[1]) / int(m[2]))), expr)
    # Step 2: Strength reduction and identity rules
    expr = re.sub(r'\b(\w+)\s*\*\s*1\b', r'\1', expr) # x * 1 → x
    expr = re.sub(r'\b1\s*\*\s*(\w+)\b', r'\1', expr)
    expr = re.sub(r'\b(\w+)\s*\+\s*0\b', r'\1', expr) # x + 0 → x
    expr = re.sub(r'\b0\s*\+\s*(\w+)\b', r'\1', expr)
    expr = re.sub(r'\b(\w+)\s*\-\s*0\b', r'\1', expr) # x - 0 → x
    expr = re.sub(r'\b(\w+)\s*\*\s*0\b', r'0', expr) # x * 0 → 0
    expr = re.sub(r'\b0\s*\*\s*(\w+)\b', r'0', expr)
    return expr
expr = input("Enter Expression:")
print("Original:", expr)
optimized = algebraic_optimize(expr)
print("Optimized:", optimized)