package jp.ac.tsukuba.cs.ialab.postfix;

import java.util.List;

public class CommandSequence extends Command {
    final List<Command> commands;
    public CommandSequence(List<Command> commands) {
        this.commands = commands;
    }
    protected static String listToString(List<Command> elements, String prefix) {
        return elements.stream().map(Command::toString)
                .reduce(prefix, (l,r)->(l + " " + r))
                + ")";
    }
    protected static String listToString(List<Command> elements) {
        return listToString(elements, "(");
    }
    @Override
    public String toString() {
        return listToString(commands);
    }
    public void accept(Processor p) { p.process(this); }
}
