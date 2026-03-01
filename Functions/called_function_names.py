def called_function_names(code: str) -> set[str]:
    import ast

    class CallNameCollector(ast.NodeVisitor):
        def __init__(self):
            self.called = set()
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                self.called.add(node.func.id)
            self.generic_visit(node)

    try:
        mod = ast.parse(code)
    except SyntaxError:
        return set()

    v = CallNameCollector()
    v.visit(mod)
    return v.called
