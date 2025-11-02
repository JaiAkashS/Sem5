#include <stdio.h>
#include <string.h>

int	main(void)
{
	char threecode[10][30], str[20], op[10];
	int i = 0;
	printf("Enter the three address code:\n");
	printf("Enter 'exit' at end\n\n");
	// Read the input until 'exit' is entered
	do
	{
		scanf("%s", threecode[i]);
	} while (strcmp(threecode[i++], "exit") != 0);
	printf("\nCorresponding Assembly Language Code\n\n");
	// Reset i to 0 for processing
	i = 0;
	do
	{
		strcpy(str, threecode[i]);
		// Determine the operation based on the character at index 3
		switch (str[3])
		{
		case '+':
			strcpy(op, "ADD");
			break ;
		case '-':
			strcpy(op, "SUB");
			break ;
		case '*':
			strcpy(op, "MUL");
			break ;
		case '/':
			strcpy(op, "DIV");
			break ;
		default:
			strcpy(op, "UNKNOWN"); // Handle unexpected cases
			break ;
		}
		// Generate the assembly code
		printf("Mov %c, R%d\n", str[2], i);
		printf("%s %c, R%d\n", op, str[4], i);
		printf("Mov R%d, %c\n", i, str[0]);
	} while (strcmp(threecode[++i], "exit") != 0);
	return (0);
}