%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int yylex(void);
%}

%token IF ELSE ELSEIF FOR WHILE S OP EQ RELOP NUMBER ID NL

%%

start:
    stmt NL { printf("Statement is valid!\n"); exit(0); }
    ;

stmt:
      if_stmt
    | for_stmt
    | while_stmt
    | s_stmt
    ;

stmt_block:
      '{' stmt_list '}'
    ;

stmt_list:
      stmt
    | stmt stmt_list
    ;

if_stmt:
      IF '(' cond ')' stmt_block
    | IF '(' cond ')' stmt_block ELSE stmt_block
    | IF '(' cond ')' stmt_block elif_stmt ELSE stmt_block
    ;

elif_stmt:
      ELSEIF '(' cond ')' stmt_block
    | ELSEIF '(' cond ')' stmt_block elif_stmt
    ;

for_stmt:
      FOR '(' initi ';' cond ';' adi ')' stmt_block
    ;

while_stmt:
      WHILE '(' cond ')' stmt_block
    ;

s_stmt:
      S
    ;

initi:
      ID EQ NUMBER
    ;

cond:
      x RELOP x
    ;

adi:
      ID OP
    ;

x:
      ID
    | NUMBER
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax error\n");
    exit(1);
}

int main() {
    printf("Enter a statement:\n");
    yyparse();
    return 0;
}
