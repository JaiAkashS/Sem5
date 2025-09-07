%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);

%}

%token NUMBER

%left '+' '-'
%left '*' '/'
%right UMINUS   /* Unary minus */

%%

input:
      /* empty */
    | input line
    ;

line:
      '\n'            /* empty line, ignore */
    | expr '\n'       { printf("Result = %d\n", $1); }
    ;

expr:
      NUMBER          { $$ = $1; }
    | expr '+' expr   { $$ = $1 + $3; }
    | expr '-' expr   { $$ = $1 - $3; }
    | expr '*' expr   { $$ = $1 * $3; }
    | expr '/' expr   { 
                         if ($3 == 0) {
                             yyerror("Division by zero");
                             $$ = 0;
                         } else {
                             $$ = $1 / $3;
                         }
                      }
    | '-' expr %prec UMINUS { $$ = -$2; }
    | '(' expr ')'    { $$ = $2; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter expressions to calculate (Ctrl+D to exit):\n");
    yyparse();
    return 0;
}
