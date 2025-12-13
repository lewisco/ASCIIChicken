import http.server
import socketserver
import urllib.request
import ipaddress

PORT = 8081

# A better ASCII Chicken
CHICKEN = r"""
   \\
   (o>
\\_//)
 \_/_)
  _|_
"""

def get_public_ip():
    try:
        # Use a reliable external service to get the public IP
        with urllib.request.urlopen('https://api.ipify.org', timeout=3) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Could not fetch public IP: {e}"

def is_private_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

class ChickenHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """
        Handle GET requests by responding with the client's IP address followed by ASCII chicken art.
        
        Determines the IP to display by using the first IP from the `X-Forwarded-For` header when present; otherwise, if the connecting client IP is private or loopback, it fetches the public IP from the upstream service; if neither case applies, it uses the connecting client IP. Sends an HTTP 200 response with Content-Type `text/plain` and a response body containing the chosen IP, a newline, the chicken ASCII art, and a trailing newline.
        """
        client_ip = self.client_address[0]
        
        # Check for X-Forwarded-For header (used by proxies/load balancers like Cloud Run)
        x_forwarded_for = self.headers.get('X-Forwarded-For')
        
        if x_forwarded_for:
            # The first IP in the list is the original client
            display_ip = x_forwarded_for.split(',')[0].strip()
        elif is_private_ip(client_ip):
            # Fallback for local dev: fetch public IP from upstream
            display_ip = get_public_ip()
        else:
            display_ip = client_ip
        
        response_text = f"{display_ip}\n{CHICKEN}\n"
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_text.encode('utf-8'))

class ReusableThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

with ReusableThreadingTCPServer(("", PORT), ChickenHandler) as httpd:
    print(f"Serving ASCII Chicken at port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass