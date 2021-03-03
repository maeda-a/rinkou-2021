package jp.ac.tsukuba.cs.ialab.postfix;

public class IntLit extends Command {
    final int value;
    public IntLit(int value) { this.value = value; }
    @Override public String toString() { return Integer.toString(value); }
    public void accept(Processor p) { p.process(this); }
}
