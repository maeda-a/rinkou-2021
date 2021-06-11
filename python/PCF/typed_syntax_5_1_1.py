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

def type_to_str(tt: PCFType) -> str:
    match tt:
        case PCFTypeVar(x): return x
        case Nat(): return "nat"
        case Function(src, dst): return "({}->{})".format(type_to_str(src), type_to_str(dst))
        case _: raise Exception("Unknown type: " + str(tt))

def typed_AST_to_str(t: Term) -> str:
    a = typed_AST_to_str
    match t:
        case Var(x): return x
        case Fun(x, aa, t2): return "(fun {}:{} -> {})".format(a(x), type_to_str(aa), a(t2))
        case App(u, v): return "({} {})".format(a(u), a(v))
        case Num(n): return str(n)
        case Op(op, left, right): 
            return "({} {} {})".format(a(left), op, a(right))
        case Ifz(cond, thenTerm, elseTerm):
            return "(ifz {} then {} else {})".format(a(cond), a(thenTerm), a(elseTerm))
        case Fix(x, aa, t2):
            return "(fix {}:{} -> {})".format(a(x), type_to_str(aa), a(t2))
        case Let(x, aa, t2, body):
            return "(let {}:{} = {} in {})".format(a(x), type_to_str(aa), a(t2), a(body))
        case _: raise Exception("Unknown term: " + str(t))