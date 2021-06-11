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

def AST_to_str(t: Term) -> str:
    # 各クラスに __str__ や __repr__ メソッドを定義することもできるが
    # あえてパターンマッチで書いてみる
    a = AST_to_str
    match t:
        case Var(x): return x
        case Fun(x, t2): return "(fun {} -> {})".format(a(x), a(t2))
        case App(u, v): return "({} {})".format(a(u), a(v))
        case Num(n): return str(n)
        case Op(op, left, right): 
            return "({} {} {})".format(a(left), op, a(right))
        case Ifz(cond, thenTerm, elseTerm):
            return "(ifz {} then {} else {})".format(a(cond), a(thenTerm), a(elseTerm))
        case Fix(x, t2):
            return "(fix {} -> {})".format(a(x), a(t2))
        case Let(x, t2, body):
            return "(let {} = {} in {})".format(a(x), a(t2), a(body))
        case FixFun(f, x, t2):
            return "(fixfun {} {} -> {})".format(a(f), a(x), a(t2))
        case _: raise Exception("Unknown term: " + str(t))