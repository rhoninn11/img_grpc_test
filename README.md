
# Image grpc test

Simple test for grpc ussage for image transfer. Server load image, and allow client to do some read/write operation of image memory

Img that script operate on:
![image from assets](assets/img.png)

#### setting environment:
```
pip install -r req.txt
python proto_gen.py
```

#### start server
```
pthon main.py -s
```

#### start client
```
pthon main.py -c
```

