import io
import socket
import time
from PIL import Image

# time_per_client = []

total_start = time.time()
# for i in range(1000):
# s = time.time()
client = socket.socket()
client.connect(('127.0.0.1', 1001))
# r = input("Enter the extension of your received file - jpg , png , bmp: ")
s = "imggg.png"
f = open(s, "wb")

condition = True

while condition:
    image = client.recv(1024)
    if str(image) == "b''":
        condition = False
    f.write(image)

    # img = Image.open(io.BytesIO(image))
    # img.save(io.BytesIO(image), 'PNG')
# for file in glob.glob("*.png"):
#     im = Image.open(file)
#     rgb_im = im.convert('RGB')
#     rgb_im.save(file.replace("png", "jpg"), quality=95)

    # byteImgIO = io.BytesIO(image)
    # byteImg = Image.new("RGB")
    # byteImg.save(byteImgIO, "PNG")

# e = time.time()
# time_per_client.append(e-s)
print(
    f'Total time: {time.time()-total_start}')
# print(f'Avg time per client: {sum(time_per_client)/len(time_per_client)}')
