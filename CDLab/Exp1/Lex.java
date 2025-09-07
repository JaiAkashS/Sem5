package Exp1;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class Lex{
    public static void main(String[] args) throws IOException {
        String key = "";
        int glo = 1;

        Pattern patt = Pattern.compile("#include\\s*[<\"]\\w+\\.h[>\"]"); // header file
        Pattern patt1 = Pattern.compile("\\b(printf|main|auto|double|int|struct|break|else|long|switch|case|enum|register|typedef|char|extern|return|union|float|short|unsigned|continue|for|signed|void|default|goto|sizeof|volatile|do|if|static|while)\\b"); // keywords
        Pattern patt2 = Pattern.compile("//.*"); // single-line comment
        Pattern patt3 = Pattern.compile("\\b[0-9]+\\b"); // numbers
        Pattern patt4 = Pattern.compile("\\bconst\\s+[a-zA-Z_]\\w*"); // constants
        Pattern patt5 = Pattern.compile("([+=*!<>/])+"); // operators
        Pattern patt6 = Pattern.compile("[;(){}_]"); // special characters
        Pattern patt7 = Pattern.compile("\\b[a-zA-Z_]\\w*\\b"); // identifiers

        BufferedReader r = new BufferedReader(new FileReader("G:\\CodingStuff\\sem5\\CDLab\\Exp1\\input.txt"));
        ArrayList<STable> stb = new ArrayList<STable>();
        String line;
i
        while ((line = r.readLine()) != null) {
            int h = 0, k = 0, c = 0, con = 0, s = 0;
            String kd = null, kd1 = null;

            // Comments
            Matcher m2 = patt2.matcher(line);
            while (m2.find()) {
                String a = line.substring(m2.start(), m2.end());
                System.out.println(a + " is a comment");
                c = 1;
            }

            // Header files
            Matcher m = patt.matcher(line);
            while (m.find() && c == 0) {
                String a = line.substring(m.start(), m.end());
                System.out.println(a + " is a header file");
                h = 1;
            }

            // Constants
            Matcher m4 = patt4.matcher(line);
            while (m4.find() && c == 0) {
                String a = line.substring(m4.start(), m4.end());
                System.out.println(a + " is a constant");
                con = 1;
            }

            // Keywords
            Matcher m1 = patt1.matcher(line);
            while (m1.find() && c == 0) {
                String a = line.substring(m1.start(), m1.end());
                System.out.println(a + " is a keyword");
                kd = a;
                k = 1;
                key = key + " " + a;
                if (a.equals("main")) {
                    glo = 0;
                }
            }

            // Identifiers
            Matcher m7 = patt7.matcher(line);
            while (m7.find() && h == 0 && con == 0 && c == 0 && s == 0) {
                String a = line.substring(m7.start(), m7.end());
                int present = 0;
                if (!(a.equals(kd)) && (!key.contains(" " + a))) {
                    System.out.println(a + " is an identifier");
                    STable s1 = new STable(a, kd, glo == 0 ? "local" : "global");

                    for (STable p : stb) {
                        if (p.getId().equals(a))
                            present = 1;
                    }
                    if (present == 0)
                        stb.add(s1);
                }
            }

            // Operators
            Matcher m5 = patt5.matcher(line);
            while (m5.find() && h == 0 && c == 0) {
                String a = line.substring(m5.start(), m5.end());
                System.out.println(a + " is an operator");
            }

            // Numbers
            Matcher m3 = patt3.matcher(line);
            while (m3.find() && c == 0) {
                String a = line.substring(m3.start(), m3.end());
                System.out.println(a + " is a number");
            }

            // Special characters
            Matcher m6 = patt6.matcher(line);
            while (m6.find() && c == 0) {
                String a = line.substring(m6.start(), m6.end());
                System.out.println(a + " is a special character");
            }

            System.out.println();
        }

        // Print Symbol Table
        System.out.println("Symbol Table");
        System.out.println("------ -----");
        for (STable p : stb)
            System.out.println(p);
    }
}
