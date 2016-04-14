import json

from .algorithm import *
from .eval_op import Evaluator as BlockEvaluator


class Node:
    START = 1
    OP = 2
    IF = 3
    END = 4

    def __init__(self, kind, op, children=[]):
        self.kind = kind
        self.op = op
        self.children = children


class EvalContext:
    def __init__(self):
        self.variables = dict()
        self.functions = dict()


class NodeEval:
    def __init__(self, start, context):
        self.context = context
        self.node = start

    def next(self):
        ret = self._eval()

        # TODO: verify graph structure

        if self.node.kind == self.node.START:
            self.node = self.node.children[0]
        elif self.node.kind == self.node.OP:
            self.node = self.node.children[0]
        elif self.node.kind == self.node.IF:
            self.node = self.node.children[int(ret)]
        elif self.node.kind == self.node.END:
            return False

        return True

    def _eval(self):
        if self.node.kind == self.node.OP:
            ops = self.node.split('\n')
            ev = BlockEvaluator(self.context.variables, self.context.functions)

            for op in ops:
                name, val = ev.eval(op)
                self.context.variables[name] = val

        elif self.node.kind == self.node.IF:
            op = self.node.op.replace('\n', ' ')

            ev = BlockEvaluator(self.context.variables, self.context.functions)

            res = ev.eval(op)

            return res > 0


class Evaluator:
    def __init__(self, context, source):
        self.context = context

        data = json.loads(source)

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

        while ev.next():
            pass

    @staticmethod
    def _classify(node):
        if 'category' in node and node['category'] == 'Start':
            return Node.START
        elif 'category' in node and node['category'] == 'End':
            return Node.END
        elif 'figure' in node and node['figure'] == 'Diamond':
            return Node.IF
        else:
            return Node.OP
