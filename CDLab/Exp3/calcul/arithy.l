%{
#include "arithy.tab.h"  // Yacc generated header file with tokens
#include <stdio.h>
#include <stdlib.h>
%}

%%

[ \t]+            ;               // Skip whitespace and tabs

[0-9]+            { 
                     yylval = atoi(yytext); 
                     return NUMBER; 
                  }

"+"               { return '+'; }
"-"               { return '-'; }
"*"               { return '*'; }
"/"               { return '/'; }
"("               { return '('; }
")"               { return ')'; }
"\n"              { return '\n'; }

.                 { 
                    fprintf(stderr, "Invalid character: %s\n", yytext); 
                    return 0; 
                  }

%%

int yywrap() {
    return 1;
}
