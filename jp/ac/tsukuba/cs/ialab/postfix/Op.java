package jp.ac.tsukuba.cs.ialab.postfix;

public class Op extends Command {
    final String name;
    public Op(String name) { this.name = name; }
    @Override
    public void accept(Processor p) {
        p.process(this);
    }
    @Override public String toString() { return name; }
}
