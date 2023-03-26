import os
import base64
with open('11.txt') as f:
    for line in f:
        base64_string =line.strip('\n')
        base64_bytes = base64_string.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        os.system('python3.8 50512.py '+sample_string)
with open('list.txt', 'a') as file:
	file.write('fin')
file.close()
