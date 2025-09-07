%{
#include "y.tab.h"
#include <stdio.h>
#include <stdlib.h>
%}

%%

"if"             { return IF; }
"else"           { return ELSE; }
"elseif"         { return ELSEIF; }
"for"            { return FOR; }
"while"          { return WHILE; }

[sS][0-9]+       { return S; }

"++"|"--"        { return OP; }

"="              { return EQ; }

"=="|"<="|">="|"!="|"<"|">"  { return RELOP; }

[0-9]+           { yylval = atoi(yytext); return NUMBER; }

[a-zA-Z_][a-zA-Z0-9_]*  { return ID; }

\n               { return NL; }

[ \t]+           { /* skip whitespace */ }

.                { return yytext[0]; }

%%

int yywrap() {
    return 1;
}
