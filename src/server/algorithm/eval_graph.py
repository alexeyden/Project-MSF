import time

from .algorithm import *
from .eval_op import *
from .eval_op import Evaluator as BlockEvaluator
from .exceptions import *

class Node:
    START = 1
    OP = 2
    IF = 3
    END = 4
    OUT = 5

    def __init__(self, kind, op, children=[]):
        self.kind = kind
        self.op = op
        self.children = children

    def __str__(self):
        name_dict = {
            self.START: "Начало",
            self.OP: "Действие",
            self.IF: "Условие",
            self.END: "Конец",
            self.OUT: "Вывод"
        }

        if self.kind == self.START or self.kind == self.END:
            return name_dict[self.kind]

        return name_dict[self.kind] + ": " + self.op.replace('\n', '; ')


class EvalContext:
    def __init__(self):
        self.readonly = []
        self.variables = dict()
        self.functions = dict()


class NodeEval:
    def __init__(self, start, context):
        self.context = context
        self.node = start

    def next(self):
        ret = self._eval()

        if self.node.kind == self.node.START:
            if len(self.node.children) == 0:
                raise GraphConnectivityError('Блок "{0}" не связан с другими блоками!'.format(self.node), str(self.node))

            self.node = self.node.children[0]

        elif self.node.kind == self.node.OP:
            if len(self.node.children) == 0:
                raise GraphConnectivityError('Блок "{0}" не связан с другими блоками!'.format(self.node), str(self.node))

            self.node = self.node.children[0]

        elif self.node.kind == self.node.IF:
            if len(self.node.children) < 2:
                raise GraphConnectivityError('Блок "{0}" не связан с другими блоками!'.format(self.node), str(self.node))

            self.node = self.node.children[int(ret)]

        elif self.node.kind == self.node.OUT:
            if len(self.node.children) == 0:
                raise GraphConnectivityError('Блок "{0}" не связан с другими блоками!'.format(self.node), str(self.node))

            self.node = self.node.children[0]

        elif self.node.kind == self.node.END:
            return False

        return True

    def _eval(self):
        if self.node.kind == self.node.OP:
            ops = self.node.op.split('\n')
            ev = BlockEvaluator(self.context.variables, self.context.functions)

            for op in ops:
                try:
                    name, val = ev.eval(op)
                except ParseError as err:
                    msg = "Синтаксическая ошибка в блоке {0}: \n{1}".format(self.node, err.msg)
                    raise BlockSyntaxError(msg, str(self.node), err.position) from err
                except NotDefinedError as err:
                    msg = "Ошибка в блоке {0}: \n{1}".format(self.node, err.msg)
                    raise BlockSymbolError(msg, str(self.node), err.symbol, err.position) from err
                except MathError as err:
                    msg = "Ошибка в блоке {0}: \n{1}".format(self.node, err.msg)
                    raise BlockEvalError(msg, str(self.node)) from err

                if name not in self.context.readonly:
                    self.context.variables[name] = val

        elif self.node.kind == self.node.IF:
            op = self.node.op.replace('\n', ' ')

            ev = BlockEvaluator(self.context.variables, self.context.functions)

            try:
                res = ev.eval(op)
            except ParseError as err:
                msg = "Синтаксическая ошибка в блоке {0}: \n{1}".format(self.node, err.msg)
                raise BlockSyntaxError(msg, str(self.node), err.position) from err
            except NotDefinedError as err:
                msg = "Ошибка в блоке {0}: \n{1}".format(self.node, err.msg)
                raise BlockSymbolError(msg, str(self.node), err.symbol, err.position) from err
            except MathError as err:
                msg = "Ошибка в блоке {0}: \n{1}".format(self.node, err.msg)
                raise BlockEvalError(msg, str(self.node)) from err

            return res > 0


class Evaluator:
    def __init__(self, source, context):
        self.context = context
        self.timeout = 10.0

        try:
            data = json.loads(source)
        except json.JSONDecodeError as err:
            raise AlgorithmParseError(err.msg)

        nodes = dict()

        for node in data['nodeDataArray']:
            kind = self._classify(node)
            op = node['text']
            key = node['key']
            children = [None, None] if kind == Node.IF else []
            nodes[key] = Node(kind, op, children)

        for link in data['linkDataArray']:
            from_ = link['from']
            to = link['to']

            n_from = nodes[from_]
            n_to = nodes[to]

            if n_from.kind == Node.IF:
                if link['fromPort'] == 'L':
                    n_from.children[0] = n_to
                elif link['fromPort'] == 'R':
                    n_from.children[1] = n_to
            else:
                n_from.children.append(n_to)

        self._start = [node for node in nodes.values() if node.kind == Node.START][0]

    def eval(self):
        ev = NodeEval(self._start, self.context)

        start_time = time.time()

        while ev.next():
            cur_time = time.time()

            if (cur_time - start_time) > self.timeout:
                raise GraphTimeoutError(
                    "Превышено время исполнения алгоритма ({0:.1f} сек). "
                    "Возможно алгоритм содержит бесконечный цикл.".format(self.timeout), self.timeout)

    @staticmethod
    def _classify(node):
        if 'category' in node and node['category'] == 'Start':
            return Node.START
        elif 'category' in node and node['category'] == 'End':
            return Node.END
        elif 'figure' in node and node['figure'] == 'Diamond':
            return Node.IF
        elif 'category' in node and node['category'] == 'Out':
            return Node.OUT
        else:
            return Node.OP
