n = int(input("Enter the number of quadruples: "))
b = [list(map(str, input().split())) for _ in range(n)]
a = []
for i in range(n):
    opr = b[i][0]
    op1 = b[i][1]
    op2 = b[i][2]
    res = b[i][3]
    if opr == '^':
        k = int(op2)
        x = ['*', op1, op1, res]
        a.append(x)
        for j in range(0, k - 2):
            x = ['*', op1, res, res]
            a.append(x)
    elif opr == '*':
        k = int(op2)
        x = ['+', op1, op1, res]
        a.append(x)
        for j in range(0, k - 2):
            x = ['+', op1, res, res]
            a.append(x)
    else:
        a.append(b[i])
print("After strength reduction:")
for i in a:
    print(' '.join(i))