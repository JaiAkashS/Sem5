letter [a-zA-Z]
digit [0-9]
symbol [{}();,]
op [+<>=/*\-.]
%%
"#include<"{letter}+".h>" printf("\n%s is a header file",yytext);
"const "{letter}({letter}|{digit})* printf("\n%s is a constant",yytext);
"//".* printf("\n%s is a comment",yytext);
"/*"(.|\n)*"*/" printf("\n%s is a comment",yytext);
"\"".*"\"" printf("\n%s is string",yytext);
{digit}+ printf("\n%s is number",yytext);
"if"|"else"|"int"|"char"|"scanf"|"printf"|"void"|"for"|"float"|"main" printf("\n%s is keyword",yytext);
{op}+ printf("\n%s is a operator",yytext);
{symbol} printf("\n%s is a special character",yytext);
{letter}({letter}|{digit})* printf("\n%s is a identifier",yytext);
%%
int yywrap()
{
return 1;
}
int main(int argc,char *argv[])
{
yyin=fopen(argv[1],"r");
yylex();
fclose(yyin);
return 0;
}
