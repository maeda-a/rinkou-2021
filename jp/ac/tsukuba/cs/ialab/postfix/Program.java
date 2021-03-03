package jp.ac.tsukuba.cs.ialab.postfix;

import java.util.List;

public class Program {
    final int nParams;
    final CommandSequence body;
    public Program(int nParams, CommandSequence body) {
        this.nParams = nParams;
        this.body = body;
    }
    @Override public String toString() {
        return CommandSequence.listToString(body.commands, "(postfix " + nParams + " ");
    }

    public static CommandSequence seq(Command...children) {
        return new CommandSequence(List.of(children));
    }
    public static Command cmd(String name) { return new Op(name); }
    public static IntLit lit(int n) { return new IntLit(n); }

    // テスト用
    public static void main(String[] args) {
        Program p = new Program(0,
                     seq(lit(10), seq(cmd("swap"), lit(2), cmd("mul"), cmd("sub")),
                         lit(1), cmd("swap"), cmd("exec")));
        System.out.println(p);
    }
}
