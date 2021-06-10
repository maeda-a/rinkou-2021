# optimized interpreter in 3.4.2
# new syntax: FixFun(f, x, term): short hand for Fix(f, Fun(x, term))

from interp_3_2 import *

@dataclass
class RecClosure(Value):
    f: Var
    x: Var
    t: Term
    e: Environment

# 差し替える部分
def searchEnv(x: Var, e: Environment) -> Value:
    for (var, val) in e:
        if var == x:
            return val
    raise Exception("Unbound variable: " + str(x))

def interp(t: Term, e: Environment) -> Value:
    match t:
        case Var(x): return searchEnv(t, e)
        case App(t, u):
            w = interp(u, e)
            v = interp(t, e)
            match v:
                case RecClosure(f, x, t2, e2):
                    return interp(t2, extendEnv(x, w, extendEnv(f, v, e2)))
                case _: raise Exception("Illegal function: " + str(v))
        case Fun(x, t2): return RecClosure(Var(''), x, t2, e)
        case Num(n): return t
        case Op(op, l, r):
            lv = checkNumber(interp(l, e))
            rv = checkNumber(interp(r, e))
            match op:
                case '+': return Num(lv + rv)
                case '-': return Num(lv - rv)
                case '*': return Num(lv * rv)
                case '/': return Num(lv / rv)
                case '%': return Num(lv % rv)
                case '<': return Num(1 if lv < rv else 0)
                case '=': return Num(1 if lv == rv else 0)
                case _: raise Exception("Unknown op: " + str(op))
        case Ifz(cond, t, u):
            c = interp(cond, e)
            match c:
                case Num(0): return interp(t, e)
                case Num(_): return interp(u, e)
                case _: raise Exception("Condition not a number: " + str(c))
        case FixFun(f, x, t2):
            return RecClosure(f, x, t2, e)
        case Let(x, t, u):
            w = interp(t, e)
            return interp(u, extendEnv(x, w, e))

print(interp(App(FixFun(Var('f'), Var('x'), Ifz(Var('x'), Num(1), Op('*', Var('x'), App(Var('f'), Op('-', Var('x'), Num(1)))))), Num(10)), [])) # Recursive function call using FixFun
