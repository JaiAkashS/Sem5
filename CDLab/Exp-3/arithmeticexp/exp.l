%{
#include <stdio.h>
#include "y.tab.h"
%}

%%

[a-zA-Z_][a-zA-Z0-9_]*    { return IDENTIFIER; }
[0-9]+(\.[0-9]+)?         { return NUMBER; }
[+\-*/]                   { return yytext[0]; }
[ \t]+                    { /* skip whitespace */ }
\n                        { return 0; }
.                         { return yytext[0]; }

%%

int yywrap() {
    return 1;
}
