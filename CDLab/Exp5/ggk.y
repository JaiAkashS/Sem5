%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void yyerror(const char* s) {
    fprintf(stderr, "Parse error: %s\n", s);
}
int yylex();  // Declare the lexer function
%}
%union {
   int ival;     // For INTEGER
    float fval;    // For FLOAT
    char* sval;    // For CHAR/STRING
}
%token <ival> INTEGER
%token <fval> FLOAT
%token <sval> CHAR
%token EOL
%type <ival> statement
%type <ival> expression
%type <sval> line%%
program:
   /* empty */
   | program line
    ;line:
    statement EOL {
        if ($1 == INTEGER) {
            printf("Type: INTEGER\n");
        } else if ($1 == FLOAT) {
            printf("Type: FLOAT\n");
        } else if ($1 == CHAR) {
            printf("Type: CHAR/STRING\n");
        } else {
            printf("Invalid type\n");
        }
   }  ;
statement:
    expression {
        $$ = $1;  // Assign the value of the expression to the statement
    };expression:
    INTEGER {
        $$ = INTEGER;
   }
   | FLOAT {
        $$ = FLOAT;
   }
   | CHAR {
$$ = CHAR;
    };%%
int main() {
    yyparse();
    return 0;
}