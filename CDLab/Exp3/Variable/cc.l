%{
#include "y.tab.h"
%}

%%

[a-zA-Z_][a-zA-Z_0-9]*   return LETTER;   /* identifiers starting with a letter */
[0-9]+                   return DIGIT;    /* numbers */
.                        return yytext[0];/* anything else */
\n                       return 0;        /* end of input */

%%

int yywrap() {
    return 1;
}

