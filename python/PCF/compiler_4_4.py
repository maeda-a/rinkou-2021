# Compiler: sec.4.4

from dataclasses import dataclass
from typing import Sequence
from typing import Union

from syntax_2_1_7 import *

@dataclass
class Instruction: pass

@dataclass
class Ldi(Instruction): 
    n: int

@dataclass
class Push(Instruction): pass

@dataclass
class Extend(Instruction): pass

@dataclass
class Search(Instruction):
    n: int

@dataclass
class Pushenv(Instruction): pass

@dataclass
class Popenv(Instruction): pass

@dataclass
class Mkclos(Instruction):
    i: Sequence[code]

@dataclass
class Apply(Instruction): pass

@dataclass
class Test(Instruction):
    i: Sequence[code]
    j: Sequence[code]

@dataclass
class Add(Instruction): pass

@dataclass
class Sub(Instruction): pass

@dataclass
class Mult(Instruction): pass

@dataclass
class Div(Instruction): pass

@dataclass
class MachineClosure(Value):
    i: Sequence[Code]
    e: Sequence[value]

Stack: TypeAlias = Sequence[Value | Sequence[Value]]

def trimValue(v): # for debug
    match v:
        case Num(n): return v
        case [item, *items]: return "[{}, ...]".format(trimValue(item))
        case []: return "[]"
        case _: return type(v).__name__

# stackは教科書と逆に末尾に破壊的にpushし、末尾からpopする。
# envは教科書と逆に先頭にコピーして追加する。Searchの引数は先頭からの位置を表す。
# codeは先頭から破壊的にpopし、先頭にコピーして結合する。
def PCFmachine(acc: Value, stack: Stack, env: Sequence[Value], code: Sequence[Instruction]) -> Value:
    while code:
        # print("acc={}, stack={}, env={}, code={}".format(acc, trimValue(stack), trimValue(env), trimValue(code)))
        insn = code.pop(0)
        match insn:
            case Mkclos(i):
                acc = MachineClosure(i, env)
            case Push():
                stack.append(acc)
            case Extend():
                env = [acc] + env
            case Search(n):
                acc = env[n]
            case Pushenv():
                stack.append(env)
            case Popenv():
                env = stack.pop()
            case Apply():
                w = stack.pop()
                match acc:
                    case MachineClosure(i, env):
                        env = [w, acc] + env
                        code = i + code
                    case _:
                        raise Exception("Not a closure: " + str(acc))
            case Ldi(n):
                acc = Num(n)
            case Add():
                m = stack.pop(); acc = Num(acc.n + m.n)
            case Sub():
                m = stack.pop(); acc = Num(acc.n - m.n)
            case Mult():
                m = stack.pop(); acc = Num(acc.n * m.n)
            case Div():
                m = stack.pop(); acc = Num(acc.n / m.n)
            case Test(i, j):
                match acc:
                    case Num(0):
                        code = i + code
                    case Num(_):
                        code = j + code
                    case _:
                        raise Exception("Not a number: " + str(acc))
    return acc

def compilePCF(t: term, env: Sequence[Var]) -> Sequence[Code]:
    match t:
        case Var(name):
            for (index, v) in enumerate(env):
                if v.name == name:
                    return [Search(index)]
            raise Exception("Unbound variable: " + name)
        case App(t, u):
            return [Pushenv()] + compilePCF(u, env) + [Push()] + compilePCF(t, env) + [Apply(), Popenv()]
        case Fun(x, t):
            return [Mkclos(compilePCF(t, [x, Var('')] + env))]
        case FixFun(f, x, t):
            return [Mkclos(compilePCF(t, [x, f] + env))]
        case Num(n):
            return [Ldi(n)]
        case Op(op, t, u):
            dic = {'+': Add(), '-': Sub(), '*': Mult(), '/': Div()}
            return compilePCF(u, env) + [Push()] + compilePCF(t, env) + [dic[op]]
        case Ifz(t, u, v):
            return compilePCF(t, env) + [Test(compilePCF(u, env), compilePCF(v, env))]
        case Let(x, t, u):
            return [Pushenv()] + compilePCF(t, env) + [Extend()] + compilePCF(u, [x] + env) + [Popenv()]
        case _:
            raise Exception("Illegal term: " + str(t))

import pprint

def compileTest(t: Term) -> None:
    print("# Source term")
    pprint.pp(t)
    print("# Compiled code")
    code = compilePCF(t, [])
    pprint.pp(code)
    print("# Result")
    pprint.pp(PCFmachine(Num(0), [], [], code))
    print()


compileTest(App(Fun(Var('x'), Var('x')),Num(1))) # => 1
compileTest(App(Fun(Var('x'), Op('*', Var('x'), Var('x'))),Num(3))) # => 9
compileTest(App(App(FixFun(Var('f'),Var('x'), Fun(Var('y'),Op('*', Var('x'), Var('y')))),Num(2)),Num(3))) # => 6

factcall = Let(Var('f'), 
                FixFun(Var('g'), Var('x'), 
                       Ifz(Var('x'), Num(1), 
                            Op('*', Var('x'),
                                    App(Var('g'), Op('-', Var('x'), Num(1)))))),
                App(Var('f'), Num(6)))
compileTest(factcall)
