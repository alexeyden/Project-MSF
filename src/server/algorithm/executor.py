import asyncio
import copy
import math
from concurrent.futures import ThreadPoolExecutor

from .eval_graph import Evaluator, EvalContext


class Executor:
    def __init__(self):
        self._pool = ThreadPoolExecutor()

    async def run(self, alg, args):
        loop = asyncio.get_event_loop()

        return await loop.run_in_executor(self._pool, self._exec, copy.copy(alg), copy.copy(args))

    @staticmethod
    def _exec(alg, args):
        context = EvalContext()

        context.functions = {
            'abs': abs,
            'cos': math.cos,
            'sin': math.sin,
            'sqrt': math.sqrt
        }

        for var in args:
            context.variables[var] = args.get(var)

        ev = Evaluator(alg.source, context)
        ev.eval()

        results = {}

        if var in context.variables:
            results[var] = context.variables.get(var)

        return results
