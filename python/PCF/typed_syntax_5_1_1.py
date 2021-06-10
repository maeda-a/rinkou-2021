# Syntax (AST) of PCF: sec.2.1.7

from dataclasses import dataclass
from typing import Sequence, Union


@dataclass
class Type: pass

@dataclass
class TypeVar:
    name: str

@dataclass
class Nat(Type): pass

@dataclass
class Function(Type):
    source: Type
    dest: Type

@dataclass
class Term: pass

@dataclass
class Var(Term):
    name: str

@dataclass
class Fun(Term):
    x: Var
    a: Type
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
    a: Type
    t: Term

@dataclass
class Let(Term):
    x: Var
    a: Type
    t: Term
    body: Term
