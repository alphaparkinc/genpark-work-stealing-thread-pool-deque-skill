import sys
import json
from client import ChaseLevDeque

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-work-stealing-thread-pool-deque-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_work_stealing",
                        "description": "Simulate Chase-Lev deque local push/pop vs stealer threads",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "tasks": {"type": "array", "items": {"type": "string"}},
                                "steal_count": {"type": "integer", "default": 1}
                            },
                            "required": ["tasks"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "simulate_work_stealing":
            deque = ChaseLevDeque()
            for t in args.get("tasks", []):
                deque.push(t)
            stolen = []
            for _ in range(args.get("steal_count", 1)):
                s = deque.steal()
                if s:
                    stolen.append(s)
            popped = []
            while True:
                p = deque.pop()
                if p is None:
                    break
                popped.append(p)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"stolen_fifo": stolen, "popped_lifo": popped})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
