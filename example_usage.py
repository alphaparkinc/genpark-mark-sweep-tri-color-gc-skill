from client import TriColorGC

gc = TriColorGC()
r = TriColorGC.Object("root")
child = TriColorGC.Object("child")
orphan = TriColorGC.Object("orphan")

r.references.append(child)
gc.heap = [r, child, orphan]
gc.roots = [r]

swept = gc.run_gc()
print(f"Swept {len(swept)} unreachable objects: {[o.name for o in swept]}")
print(f"Remaining heap objects: {[o.name for o in gc.heap]}")
