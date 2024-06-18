import http.server
import socketserver
import urllib.parse
import subprocess
import threading
import os

PORT = 8080
processes = {}

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        
        if parsed_path.path == '/start':
            self.handle_start(query)
        elif parsed_path.path == '/stop':
            self.handle_stop(query)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid endpoint")
    
    def handle_start(self, query):
        if 'id' in query:
            id = query['id'][0]
            command = "sar -P ALL 1 > {}".format(id)
            print("Start : ",id, command)
            if id in processes:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Process with this ID already running\n")
                return

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processes[id] = process
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Started process with ID: {id}\n".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing id or command parameter\n")

    def handle_stop(self, query):
        if 'id' in query:
            id = query['id'][0] 
            print("Stop : ",id)
            if id in processes:
                process = processes[id]
                process.terminate()
                process.wait()
                del processes[id]
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Stopped process with ID: {id}\n".encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No process found with this ID")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing id parameter")

def run_server():
    with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()

