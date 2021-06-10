# Syntax (AST) of PCF: sec.2.1.7

from dataclasses import dataclass

@dataclass
class Term: pass

@dataclass
class Var(Term):
    name: str

@dataclass
class Fun(Term):
    x: Var
    t: Term

@dataclass
class App(Term):
    l: Term
    r: Term

@dataclass
class Value(Term): pass

@dataclass
class Num(Value):
    n: int

@dataclass
class Op(Term):
    op: str
    left: Term
    right: Term

@dataclass
class Ifz(Term):
    cond: Term
    thenTerm: Term
    elseTerm: Term

@dataclass
class Fix(Term):
    x: Var
    t: Term

@dataclass
class Let(Term):
    x: Var
    t: Term
    body: Term

# extension in 3.4.1
@dataclass
class FixFun(Term):
    f: Var
    x: Var
    t: Term
