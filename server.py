from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from datetime import datetime

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/list-wav':
            current_dir = os.path.dirname(os.path.abspath(__file__))
            wav_dir = os.path.join(current_dir, 'wav')
            
            wav_files = []
            if os.path.exists(wav_dir):
                wav_files = [f for f in os.listdir(wav_dir) if f.endswith('.wav')]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(wav_files).encode())
            return
        
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/save-response':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                timestamp = data['timestamp']
                responses = data['responses']
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                results_dir = os.path.join(current_dir, 'results')
                
                if not os.path.exists(results_dir):
                    os.makedirs(results_dir)
                
                filename = f'result_{timestamp}.txt'
                filepath = os.path.join(results_dir, filename)
                
                print(f"保存结果到文件: {filepath}")
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("文件名\t选择\t反应时(ms)\n")
                    for item in responses:
                        line = f"{item['file']}\t{item['choice']}\t{item['reactionTime']}\n"
                        f.write(line)
                        print(f"写入行: {line.strip()}")
                
                print("文件保存成功")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response_data = {
                    "status": "success",
                    "file": filename
                }
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                print(f"保存结果时出错: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    "status": "error",
                    "message": str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
            return

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CustomHandler)
    print('服务器运行在 http://localhost:8000/')
    print('当前工作目录:', os.getcwd())
    print('服务器文件位置:', os.path.abspath(__file__))
    httpd.serve_forever() 