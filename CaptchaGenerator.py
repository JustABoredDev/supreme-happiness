import os
from captcha.image import ImageCaptcha
import random
from cv2 import imshow
from http.server import BaseHTTPRequestHandler, HTTPServer
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [Middleware(CORSMiddleware, allow_origins=['*'])]



app = Starlette(middleware = middleware)


letters = "abcdefghijklmnopqrstuvwxyz123456789"
CAPTCHA_TEXT_LENGTH = 5

def createSamples(count):
	os.system("rmdir /s samples")
	os.system("mkdir samples")
	for i in range(0, count):
		captcha_text = ''.join(random.choices(letters, k=CAPTCHA_TEXT_LENGTH))

	# image2 = ImageCaptcha()
		image = ImageCaptcha(width=200, height=50, font_sizes=(30,))

		image.character_offset_dx = (0, 0)
		image.character_rotate = (-10, 10)
		image.character_warp_dx = (0.1, 0.3)
		image.word_space_probability = 0

		data = image.generate(captcha_text)
		image.write(captcha_text, "samples/" + captcha_text + ".png", format="png", bg_color=(0, 0, 0),
				fg_color=(255, 255, 255, 255))


def generateCaptcha():
	
	# generate the text and init the image
	captcha_text = ''.join(random.choices(letters, k=CAPTCHA_TEXT_LENGTH))
	image = ImageCaptcha(width=200, height=50, font_sizes=(30,))
	
	# set captcha params
	image.character_offset_dx = (0, 0)
	image.character_rotate = (-10, 10)
	image.character_warp_dx = (0.1, 0.3)
	image.word_space_probability = 0
	
	# generate the captcha
	data = image.generate(captcha_text,format="png", bg_color=(0, 0, 0),
				fg_color=(255, 255, 255, 255))

	return (captcha_text, data)

print(generateCaptcha())
codes = {}

@app.route("/AI")
async def get_ai_captcha(request):
    captcha_data = generateCaptcha()
    codes["AI"] = captcha_data[0]
    return Response(captcha_data[1].read(), media_type="image/png")

@app.route("/user")
async def get_user_captcha(request):
    captcha_data = generateCaptcha()
    codes["user"] = captcha_data[0]
    return Response(captcha_data[1].read(), media_type="image/png")

@app.route("/submit/{user_type}")
async def submit_captcha(request):
    user_type = request.path_params["user_type"]
    res = request.query_params["res"]
    if user_type not in ["AI", "user"]:
        return {"error": "Invalid user type"}
    
    correct = codes[user_type] == res
    return Response("correct" if correct else "wrong", media_type="text/plaintext")

# class HttpProcessor(BaseHTTPRequestHandler):
# 	codes = {}

# 	def address_string(self):
# 		host, port = self.client_address[:2]
# 		#return socket.getfqdn(host)
# 		return host

# 	def do_GET(self):

# 		if("favicon" in self.path):
# 			return

# 		if("submit" not in self.path):
# 			captcha_data = generateCaptcha()
# 			self.codes["AI" if "AI" in self.path else "user"] = captcha_data[0]
# 			self.send_response(200)
# 			self.send_header('content-type', 'image/png')
# 			self.send_header("Access-Control-Allow-Origin", "*")
# 			self.end_headers()
# 			self.wfile.write(captcha_data[1].read())
# 		else:
# 			self.send_response(200)
# 			self.send_header('content-type', 'text/text')
# 			self.send_header("Access-Control-Allow-Origin", "*")
# 			self.end_headers()
# 			print("is AI in the path? ", "AI" in self.path)
# 			print(self.codes["AI" if "AI" in self.path else "user"])
# 			print(self.path[self.path.find("?res=") + 5 : ])
# 			correct = self.codes["AI" if "AI" in self.path else "user"] == self.path[self.path.find("?res=") + 5 : ]

# 			self.wfile.write(b"correct" if correct else b"wrong")




# # localhost:8080/AI/
# # localhost:8080/submit/AI?res=AAAAA

# # localhost:8080/user/
# # localhost:8080/submit/user?res=AAAAA


# serv = HTTPServer(('localhost', 8080), HttpProcessor)
# serv.serve_forever()