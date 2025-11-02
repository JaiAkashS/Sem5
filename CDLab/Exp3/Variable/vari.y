%{
#include <stdio.h>
int valid = 1;

/* Forward declarations to avoid warnings */
int yylex(void);
int yyerror(const char *s);
%}

%token DIGIT LETTER   /* Declare tokens for digits and letters */

%%

start : LETTER s      /* Starting rule: must begin with a letter */
     ;

s : LETTER s          /* s can be a letter followed by more s */
  | DIGIT s           /* or a digit followed by more s */
  |                   /* or empty (epsilon) */
  ;

%%

int yyerror(const char *s) {
    printf("\nIt's not a valid identifier!\n");
    valid = 0;
    return 0;
}

int main() {
    printf("Enter a name to be tested for identifier: ");
    yyparse();   /* Start parsing input */
    if (valid) {
        printf("\nIt is a valid identifier!\n");
    }
    return 0;
}
