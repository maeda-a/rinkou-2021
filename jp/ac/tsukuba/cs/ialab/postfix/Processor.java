package jp.ac.tsukuba.cs.ialab.postfix;

public interface Processor {
    public void process(IntLit n);
    public void process(CommandSequence q);
    public void process(Op c);
}
