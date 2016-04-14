from arpeggio import *
from arpeggio import RegExMatch as _

__all__ = ['Evaluator', 'CalcError', 'NotDefinedError', 'ParseError', 'MathError']


class CalcError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotDefinedError(CalcError):
    def __init__(self, msg, symbol, position, *args, **kwargs):
        super().__init__(msg, symbol, position, *args, **kwargs)
        self.symbol = symbol
        self.position = position


class ParseError(CalcError):
    def __init__(self, msg, position, *args, **kwargs):
        super().__init__(msg, position, *args, **kwargs)
        self.position = position


class MathError(CalcError):
    def __init__(self, msg, position, *args, **kwargs):
        super().__init__(msg, position, *args, **kwargs)
        self.position = position


def number():     return _(r'\d*\.\d*|\d+')
def symbol(): return _(r"[a-zA-Z]+")
def function():   return _(r"[a-zA-Z]+"), "(", compare, ")"
def factor():     return Optional(["+","-"]), [function, symbol, number , ("(", compare, ")")]
def term():       return factor, ZeroOrMore(["*","/"], factor)
def expression(): return term, ZeroOrMore(["+", "-"], term)
def compare(): return expression, Optional(["<", ">", "=", "<=", ">="], expression)
def assignment(): return _(r'[a-zA-Z]+'), ":=", compare
def root():       return [OneOrMore(assignment), OneOrMore(compare)], EOF


class CalcVisitor(PTNodeVisitor):
    def __init__(self, env_var, env_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env_var = env_var
        self.env_func = env_func

    def visit_assignment(self, node, children):
        return (children[0], children[1])

    def visit_function(self, node, children):
        if children[0] in self.env_func:
            return self.env_func[children[0]](children[1])
        raise NotDefinedError('Function not defined', node.flat_str(), node.position)

    def visit_symbol(self, node, children):
        if node.value in self.env_var:
            return self.env_var[node.value]
        raise NotDefinedError('Variable not defined', node.value, node.position)

    def visit_number(self, node, children):
        return float(node.value)

    def visit_factor(self, node, children):
        if len(children) == 1:
            return children[0]
        sign = -1 if children[0] == '-' else 1
        return sign * children[-1]

    def visit_term(self, node, children):
        term = children[0]
        for i in range(2, len(children), 2):
            if children[i-1] == "*":
                term *= children[i]
            else:
                if children[i] == 0:
                    raise MathError('Деление на ноль: {0}'.format(node.flat_str()), node.position)

                term /= children[i]
        return term

    def visit_compare(self, node, children):
        if len(children) > 1:
            op = children[1]
            if op == '<':
                return int(children[0] < children[2])
            elif op == '>':
                return int(children[0] > children[2])
            elif op == '=':
                return int(children[0] == children[2])
            elif op == '<=':
                return int(children[0] <= children[2])
            elif op == '>=':
                return int(children[0] >= children[2])
        else:
            return children[0]

    def visit_expression(self, node, children):
        expr = children[0]
        for i in range(2, len(children), 2):
            if i and children[i - 1] == "-":
                expr -= children[i]
            else:
                expr += children[i]
        return expr


class Evaluator:
    def __init__(self, env_var={}, env_func={}):
        self._parser = ParserPython(root)
        self._variables = env_var
        self._functions = env_func

    def eval(self, expr):
        try:
            tree = self._parser.parse(expr)
        except NoMatch as err:
            raise ParseError(err, err.position) from err

        return visit_parse_tree(tree, CalcVisitor(self._variables, self._functions))