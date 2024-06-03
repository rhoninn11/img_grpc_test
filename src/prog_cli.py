

import proto.img_patch_pb2_grpc as pb2_grpc
import proto.img_patch_pb2 as bp2

import grpc
import concurrent.futures as futures
from skimage import io
from matplotlib import pyplot as plt


import img_patch
from img_patch import PATCH_SIZE

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = img_patch.ImgPatchService()
    pb2_grpc.add_ImgPatchServicer_to_server(service, server)

    server.add_insecure_port("localhost:50051")
    server.start()
    print("+++ Server started")
    server.wait_for_termination()

import random
import numpy as np

def start_client():
    channel = grpc.insecure_channel("localhost:50051")
    stub = pb2_grpc.ImgPatchStub(channel)
    print("+++ Client started")
    for i in range(3):
        rand_x = random.randint(0, 512)
        rand_y = random.randint(0, 512)
        print(f"+++ random x: {rand_x} y: {rand_y}")
        position = bp2.Position(x_pos=rand_x, y_pos=rand_y)

        _ = stub.SetPosition(position)
        pixels = stub.GetPixels(bp2.Empty())
        img_patch = np.frombuffer(pixels.pixels, dtype=np.uint8).reshape(PATCH_SIZE, PATCH_SIZE, 3)
        io.imshow(img_patch)
        plt.show()

import argparse
from async_server import start_server_asyn

def test_imshow():
    img_file = "fs/img.png"
    image = io.imread(img_file)
    img_size = image.shape
    io.imshow(image)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="gRPC testin for python")
    parser.add_argument("-s", action="store_true", help="start gRPC server")
    parser.add_argument("-c", action="store_true", help="start gRPC client")
    parser.add_argument("-sa", action="store_true", help="start async gRPC server")
    parser.add_argument("-t", action="store_true", help="for simple experimntal test run")
    
    args = parser.parse_args()
    if args.s:
        start_server()
    elif args.c:
        start_client()
        pass
    elif args.sa:
        start_server_asyn()
        pass
    elif args.t:
        test_imshow()
    else:
        parser.print_help()

