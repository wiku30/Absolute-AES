import os
import hashlib


def get_file_hash(path, mode='rb', buffer=3000000):
    hash_obj = hashlib.sha512()
    file_size = os.path.getsize(path) 
    with open(path, mode) as f:
        assert(file_size < buffer)
        while file_size:
            content = f.read(buffer)
            file_size -= len(content)
            hash_obj.update(content)
    return hash_obj.hexdigest()

def int2hex(ini,digits=128):
    return ('{:0' + str(digits) + 'x}').format(ini)

with open("filename.txt",'r',encoding="utf-8") as f:
    file_name = f.read()

file_hash = get_file_hash("../memento_core/" + file_name + ".pdf")
init = int(file_hash,16)

i=0
progress=0

# 1e+7 hashes for one key. 

while(1): 
    st = int2hex(init + i)
    out = hashlib.sha512(st.encode("utf-8")).hexdigest()

    if out[0:5]=="00000": # expected ~1e+6
        init = init ^ int(hashlib.sha512(out[64:128].encode("utf-8")).hexdigest(), 16)
        # To stablize running time. 
        progress += 1
        i=0
        print(str(progress*10) + "%")
    if progress >= 10:
        key = out[64:128]
        break
    i+=1

print(key)
with open('key', 'w') as key_file:
    key_file.write(key)


