%{
#include <stdio.h>
#include <stdlib.h>

int index1 = 0;
char temp = 'A' - 1;

struct expr {
    char op1[10];   // store operand1 (as string: variable or number)
    char op2[10];   // store operand2
    char oper;      // operator (+, -, *, /, =)
    char res[10];   // result (temp variable or assignment)
} arr[20];

char* addtotable(char *a, char *b, char o);
void threeAdd();
void yyerror(const char *s);
int yylex(void);
%}

%union {
    char symbol;    // for single character variables (LETTER)
    int num;        // for full integers (NUMBER)
    char* str;      // for expression results (strings)
}

%token <symbol> LETTER
%token <num> NUMBER
%left '+' '-'
%left '*' '/'
%type <str> exp stmt
%%

stmt:
      LETTER '=' exp ';'   { 
                              char lhs[2] = { $1, '\0' };
                              addtotable(lhs, $3, '=');
                           }
    ;

exp:
      exp '+' exp   { $$ = addtotable($1, $3, '+'); }
    | exp '-' exp   { $$ = addtotable($1, $3, '-'); }
    | exp '*' exp   { $$ = addtotable($1, $3, '*'); }
    | exp '/' exp   { $$ = addtotable($1, $3, '/'); }
    | '(' exp ')'   { $$ = $2; }
    | LETTER        { 
                        char *buf = malloc(2);
                        buf[0] = $1; buf[1] = '\0';
                        $$ = buf;
                     }
    | NUMBER        { 
                        char *buf = malloc(20);
                        sprintf(buf, "%d", $1);
                        $$ = buf;
                     }
    ;

%%

char* addtotable(char *a, char *b, char o) {
    temp++;
    snprintf(arr[index1].op1, 10, "%s", a);
    snprintf(arr[index1].op2, 10, "%s", b);
    arr[index1].oper = o;
    snprintf(arr[index1].res, 10, "%c", temp);
    index1++;

    char *buf = malloc(2);
    buf[0] = temp; buf[1] = '\0';
    return buf;
}

void threeAdd() {
    printf("\nThree Address Code:\n");
    for (int i = 0; i < index1; i++) {
        printf("%s := %s %c %s\n",
               arr[i].res,
               arr[i].op1,
               arr[i].oper,
               arr[i].op2);
    }
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter expression (e.g., a = b + 3 * 45;):\n");
    if (yyparse() == 0) {
        threeAdd();
    }
    return 0;
}
