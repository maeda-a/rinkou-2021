package jp.ac.tsukuba.cs.ialab.postfix;

public abstract class Command {
    public abstract void accept(Processor p);
}
