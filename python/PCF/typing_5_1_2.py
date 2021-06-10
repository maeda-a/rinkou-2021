from dataclasses import dataclass
from typing import Sequence
from typing import Union

from typed_syntax_5_1_1 import *

TypeEnv = list[tuple[Var,PCFType]]

def searchEnv(x: Var, e: TypeEnv) -> PCFType:
    for (var, val) in e:
        if var == x:
            return val
    raise Exception("Unbound variable: " + str(x))

def checkNumber(a: PCFType) -> None:
    if a != Nat():
        raise Exception("Not a number: " + str(a))

def PCFtype(t: Term, e: TypeEnv) -> PCFType:
    match t:
        case Var(x): return searchEnv(t, e)
        case App(t, u):
            A = PCFtype(u, e)
            A_B = PCFtype(t, e)
            match A_B:
                case Function(t1, t2):
                    if t1 == A:
                        return t2
                    else:
                        raise Exception("Type mismatch: {} expected, given {}.".format(str(t1), str(A)))
                case _: raise Exception("Illegal function type: " + str(A_B))
        case Fun(x, a, t2): return Function(a, PCFtype(t2, [(x, a)] + e))
        case Num(n): return Nat()
        case Op(op, l, r):
            checkNumber(PCFtype(l, e))
            checkNumber(PCFtype(r, e))
            return Nat()
        case Ifz(cond, t2, u):
            checkNumber(PCFtype(cond, e))
            a1 = PCFtype(t2, e)
            a2 = PCFtype(u, e)
            if a1 != a2:
                raise Exception("Type mismatch in {}: {} and {}".format(str(t), str(a1), str(a2)))
            return a1
        case Fix(x, a, t2): return PCFtype(t2, [(x, a)] + e)
        case Let(x, a, t2, u):
            a1 = PCFtype(t2, e)
            if a != a1:
                raise Exception("Type mismatch in {}: {} expected, given {}.".format(str(t), str(a), str(a1)))
            return PCFtype(u, [(x, a)] + e)
        case _: raise Exception("Unknown term: " + str(t))

print(PCFtype(Op('+', Num(1), Num(2)), []))
print(PCFtype(Var('x'), [(Var('x'), Nat())]))
print(PCFtype(Fun(Var('x'), Nat(), Op('*', Var('x'), Var('x'))), []))
print(PCFtype(App(Fun(Var('x'), Nat(), Op('*', Var('x'), Var('x'))), Num(3)), []))
print(PCFtype(App(Fix(Var('x'), Function(Nat(), Nat()), Fun(Var('x'), Nat(), Op('*', Var('x'), Var('x')))), Num(3)), []))
print(PCFtype(App(Fix(Var('f'), Function(Nat(), Nat()), Fun(Var('x'), Nat(), Ifz(Var('x'), Num(1), Op('*', Var('x'), App(Var('f'), Op('-', Var('x'), Num(1))))))), Num(10)), []))
print(PCFtype(App(Fun(Var('x'), Function(PCFTypeVar('A'), PCFTypeVar('B')), App(Var('x'), Var('x'))), Fun(Var('x'), Function(PCFTypeVar('A'), PCFTypeVar('B')), App(Var('x'), Var('x')))), []))
