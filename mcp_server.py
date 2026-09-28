import sys
import json
from client import TriColorGC

gc = TriColorGC()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "trigger_tri_color_gc",
                        "description": "Simulate and trigger tri-color mark-and-sweep GC cycle",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "objects": {"type": "array", "items": {"type": "string"}},
                                "roots": {"type": "array", "items": {"type": "string"}},
                                "edges": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}
                            },
                            "required": ["objects", "roots"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "trigger_tri_color_gc":
            nodes = {name: TriColorGC.Object(name) for name in args["objects"]}
            for u, v in args.get("edges", []):
                if u in nodes and v in nodes:
                    nodes[u].references.append(nodes[v])
            gc.heap = list(nodes.values())
            gc.roots = [nodes[r] for r in args["roots"] if r in nodes]
            swept = gc.run_gc()
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"swept_objects": [o.name for o in swept], "survivors": [o.name for o in gc.heap]})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
