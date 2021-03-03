package jp.ac.tsukuba.cs.ialab.postfix;

import java.util.LinkedList;

import static jp.ac.tsukuba.cs.ialab.postfix.Program.*;

public class SmallStep {
    private Program p;
    // Configuration
    private final LinkedList<Command> stack;
    private LinkedList<Command> commands;

    public SmallStep(Program p) {
        this.p = p;
        stack = new LinkedList<Command>();
        commands = new LinkedList<Command>(p.body.commands);
    }
    
    // Input Function
    private void inputFunction(int...inputs) {
        if (p.nParams != inputs.length) { 
            throw new RuntimeException("Number of input mismatch.");
        }
        for (int i : inputs) {
            stack.addLast(lit(i));
        }
    }

    private static int calculate_compare(String op, int v1, int v2) {
        switch (op) {
            case "add": return v2 + v1;
            case "sub": return v2 - v1;
            case "mul": return v2 * v1;
            case "div": return v2 / v1;
            case "rem": return v2 % v1;
            case "lt": return v2 < v1 ? 1 : 0;
            case "eq": return v2 == v1 ? 1 : 0;
            case "gt": return v2 > v1 ? 1 : 0;
            default: throw new RuntimeException("Unknown op: " + op);
        }
    }

    // Transition rules
    class Rules implements Processor {

        @Override
        public void process(IntLit n) {
            stack.push(n);
        }

        @Override
        public void process(CommandSequence q) {
            stack.push(q);
        }
        @Override
        public void process(Op c) {
            switch (c.name) {
                case "pop": stack.pop(); break;
                case "swap": {
                    Command v1 = stack.pop();
                    Command v2 = stack.pop();
                    stack.push(v1);
                    stack.push(v2);
                    break;
                }
                case "sel": {
                    Command v1 = stack.pop();
                    Command v2 = stack.pop();
                    IntLit v3 = (IntLit)stack.pop();
                    if (v3.value == 0) {
                        stack.push(v1);
                    } else {
                        stack.push(v2);
                    }
                    break;
                }
                case "nget": {
                    IntLit v_index = (IntLit)stack.pop();
                    Command v_i = stack.get(v_index.value - 1);
                    stack.push(v_i);
                    break;
                }
                case "exec": {
                    CommandSequence q = (CommandSequence) stack.pop();
                    var newSeq = new LinkedList<Command>(q.commands);
                    newSeq.addAll(commands);
                    commands = newSeq;
                    break;
                }
                default: {
                    IntLit v1 = (IntLit)stack.pop();
                    IntLit v2 = (IntLit)stack.pop();
                    stack.push(lit(calculate_compare(c.name, v1.value, v2.value)));
                    break;
                }
            }
        }
    }
    public void run(int...inputs) {
        inputFunction(inputs);
        var rules = new Rules();
        while (! commands.isEmpty()) {
            System.out.println(stack + ":" + commands);
            var cmd = commands.removeFirst();
            cmd.accept(rules);
        }
        System.out.println(((IntLit)stack.pop()).value);
    }
    // テスト用
    private static class TestCase {
        Program p; int[] inputs;
        TestCase(Program p, int...inputs) { this.p = p; this.inputs = inputs; }
    }
    public static void main(String[] args) {
        TestCase[] tests = {
            new TestCase(new Program(0,
                     seq(lit(10), seq(cmd("swap"), lit(2), cmd("mul"), cmd("sub")),
                         lit(1), cmd("swap"), cmd("exec")))),
            new TestCase(new Program(4,
                  seq(cmd("lt"), seq(cmd("add")), seq(cmd("mul")), cmd("sel"), cmd("exec"))),
                  3, 4, 5, 6),
            new TestCase(new Program(1,
                    seq(lit(1), cmd("nget"), lit(0), cmd("lt"),
                        seq(lit(0), cmd("swap"), cmd("sub")),
                        seq(),
                        cmd("sel"), cmd("exec"))),
                    -7)
        };
        for (var t: tests) {
            System.out.println("program: " + t.p);
            System.out.print("input: [");
            for (int i : t.inputs) {
                System.out.print(i + ", ");
            }
            System.out.println("]");
            new SmallStep(t.p).run(t.inputs);
        }
    }
}
