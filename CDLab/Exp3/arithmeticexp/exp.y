%{
#include <stdio.h>
#include <stdlib.h>

int valid = 1;  // Flag to track validity of expression

/* Forward declarations */
int yylex(void);
int yyerror(const char *s);
%}

/* Tokens expected from lexer */
%token IDENTIFIER NUMBER
%token '=' ';' '+' '-' '*' '/' '(' ')'

%%

/* Start rule: assignment statement */
start:
      IDENTIFIER '=' expr ';'  { /* If we reach here, expression is valid */ }
    ;

expr:
      IDENTIFIER expr_tail
    | NUMBER expr_tail
    | '-' NUMBER expr_tail
    | '(' expr ')' expr_tail
    ;

expr_tail:
      '+' expr
    | '-' expr
    | '*' expr
    | '/' expr
    | /* empty */
    ;

%%

int yyerror(const char *s) {
    fprintf(stderr, "Invalid expression!\n");
    valid = 0;
    return 0;
}

int main() {
    printf("Enter an expression to validate:\n");
    yyparse();
    if (valid) {
        printf("Valid expression!\n");
    }
    return 0;
}
