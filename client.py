"""Tri-Color Mark-and-Sweep Garbage Collection Engine.
100% Python Standard Library.
"""

class TriColorGC:
    """Tri-color abstraction mark-and-sweep garbage collection engine."""
    WHITE = 0
    GRAY = 1
    BLACK = 2

    class Object:
        def __init__(self, name):
            self.name = name
            self.color = TriColorGC.WHITE
            self.references = []

    def __init__(self):
        self.heap = []
        self.roots = []

    def run_gc(self):
        gray_stack = []
        for r in self.roots:
            r.color = self.GRAY
            gray_stack.append(r)

        while gray_stack:
            obj = gray_stack.pop()
            for ref in obj.references:
                if ref.color == self.WHITE:
                    ref.color = self.GRAY
                    gray_stack.append(ref)
            obj.color = self.BLACK

        survivors = []
        garbage = []
        for obj in self.heap:
            if obj.color == self.WHITE:
                garbage.append(obj)
            else:
                obj.color = self.WHITE
                survivors.append(obj)

        self.heap = survivors
        return garbage
