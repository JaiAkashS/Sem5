package Exp1;

public class STable {
    String id;
    String type;
    String scope;

    STable(String id, String type, String scope) {
        this.id = id;
        this.type = type;
        this.scope = scope;
    }

    public String toString() {
        return "[" + id + "," + type + "," + scope + "]";
    }

    public String getId() {
        return id;
    }
}
