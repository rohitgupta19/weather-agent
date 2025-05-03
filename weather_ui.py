from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from weather_model import process_query

class WeatherHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the HTML form for user input."""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather AI Agent</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background: #ffffff;
                    padding: 60px;
                    border-radius: 12px;
                    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
                    text-align: center;
                    width: 800px;
                }
                h1 {
                    font-size: 28px;
                    color: #333;
                }
                label {
                    font-size: 16px;
                    color: #555;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 15px;
                    margin: 15px 0;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    font-size: 16px;
                }
                input[type="submit"] {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 6px;
                    font-size: 16px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Weather AI Agent</h1>
                <form method="POST">
                    <label for="query">Enter your query (e.g., 'What is the weather in Paris?'):</label><br>
                    <input type="text" id="query" name="query" required><br><br>
                    <input type="submit" value="Submit">
                </form>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        """Handle the form submission and display the result."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        query_params = parse_qs(post_data)
        user_input = query_params.get("query", [""])[0]

        try:
            result = process_query(user_input)
        except Exception as e:
            result = f"Error: {e}"

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather AI Agent</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .container {{
                    background: #ffffff;
                    padding: 60px;
                    border-radius: 12px;
                    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
                    text-align: center;
                    width: 800px;
                }}
                h1 {{
                    font-size: 28px;
                    color: #333;
                }}
                p {{
                    font-size: 16px;
                    color: #555;
                }}
                a {{
                    text-decoration: none;
                    color: #007BFF;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Weather AI Agent</h1>
                <p><strong>Query:</strong> {user_input}</p>
                <p><strong>Result:</strong> {result}</p>
                <a href="/">Go back</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(response.encode("utf-8"))

def run_server():
    """Run the HTTP server to serve the Weather AI Agent."""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, WeatherHTTPRequestHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
