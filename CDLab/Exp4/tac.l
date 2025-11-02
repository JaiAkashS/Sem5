%{
#include "y.tab.h"
#include <stdio.h>
#include <stdlib.h>
%}

%%

[0-9]+      { yylval.num = atoi(yytext); return NUMBER; }

[a-z]       { yylval.symbol = yytext[0]; return LETTER; }

[ \t]+      { /* ignore whitespace */ }

\n          { return 0; }

.           { return yytext[0]; }   /* +, -, *, /, =, ;, etc. */

%%

int yywrap() { return 1; }
