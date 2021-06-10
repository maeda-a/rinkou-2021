# Syntax (AST) of PCF: sec.2.1.7

from dataclasses import dataclass


@dataclass
class PCFType: pass

@dataclass
class PCFTypeVar(PCFType):
    name: str

@dataclass
class Nat(PCFType): pass

@dataclass
class Function(PCFType):
    source: PCFType
    dest: PCFType

@dataclass
class Term: pass

@dataclass
class Var(Term):
    name: str

@dataclass
class Fun(Term):
    x: Var
    a: PCFType
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
    a: PCFType
    t: Term

@dataclass
class Let(Term):
    x: Var
    a: PCFType
    t: Term
    body: Term
