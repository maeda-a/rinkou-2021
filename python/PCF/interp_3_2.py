# Basic interpreter in sec. 3.2 Call by Value

from dataclasses import dataclass

from syntax_2_1_7 import *

Environment = list[tuple[Var,Term]]

@dataclass
class Closure(Value):
    x: Var
    t: Term
    e: Environment

@dataclass
class Thunk(Term):
    term: Fix
    e: Environment

def searchEnv(x: Var, e: Environment) -> Value:
    for (var, val) in e:
        if var == x:
            match val:
                case Thunk(term, e2):
                    return interp(term, e2)
                case Value(): return val
    raise Exception("Unbound variable: " + str(x))

def extendEnv(x: Var, t: Term, e: Environment) -> Environment:
    return [(x, t)] + e

def checkNumber(num: Value) -> int:
    match num:
        case Num(n): return n
    raise Exception("Not a number: " + str(num))

def interp(t: Term, e: Environment) -> Value:
    match t:
        case Var(x): return searchEnv(t, e)
        case App(t, u):
            w = interp(u, e)
            v = interp(t, e)
            match v:
                case Closure(x, t2, e2):
                    return interp(t2, extendEnv(x, w, e2))
                case _: raise Exception("Illegal function: " + str(v))
        case Fun(x, t2): return Closure(x, t2, e)
        case Num(n): return t
        case Op(op, l, r):
            lv = checkNumber(interp(l, e))
            rv = checkNumber(interp(r, e))
            match op:
                case '+': return Num(lv + rv)
                case '-': return Num(lv - rv)
                case '*': return Num(lv * rv)
                case '/': return Num(lv // rv)
                case _: raise Exception("Unknown op: " + str(op))
        case Ifz(cond, t, u):
            c = interp(cond, e)
            match c:
                case Num(0): return interp(t, e)
                case Num(_): return interp(u, e)
                case _: raise Exception("Condition not a number: " + str(c))
        case Fix(x, t2):
            return interp(t2, extendEnv(x, Thunk(t, e), e))
        case Let(x, t, u):
            w = interp(t, e)
            return interp(u, extendEnv(x, w, e))
        case _: raise Exception("Unknown term: " + str(t))

print(interp(Op('+', Num(1), Num(2)), []))
print(interp(Var('x'), [(Var('x'), Num(1))]))
print(interp(App(Fix(Var('x'), Fun(Var('x'), Op('*', Var('x'), Var('x')))), Num(3)), []))
print(interp(App(Fix(Var('f'), Fun(Var('x'), Ifz(Var('x'), Num(1), Op('*', Var('x'), App(Var('f'), Op('-', Var('x'), Num(1))))))), Num(10)), []))

