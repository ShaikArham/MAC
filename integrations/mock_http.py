"""Loopback-only fixture HTTP service; no external calls."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import build_opener, ProxyHandler, HTTPRedirectHandler
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
def server(fixtures):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in fixtures:
                self.send_error(404); return
            body=json.dumps({"simulated":True,"records":fixtures[self.path]}).encode()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
        def log_message(self,*args): pass
    return ThreadingHTTPServer(("127.0.0.1",0),Handler)
def fetch(port, kind):
    if kind not in {"accounting","crm"} or not isinstance(port,int) or not 1<=port<=65535: raise ValueError("invalid local endpoint")
    opener=build_opener(ProxyHandler({}),NoRedirect())
    with opener.open(f"http://127.0.0.1:{port}/{kind}",timeout=3) as response:
        payload=json.loads(response.read(1048577))
    if payload.get("simulated") is not True or not isinstance(payload.get("records"),list) or any(not isinstance(r,dict) for r in payload["records"]): raise ValueError("invalid fixture")
    return payload["records"]
