

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
    patches: list[bp2.Image] = []
    print("+++ Client started")

    for i in range(15):
        rand_pos_x = random.randint(0, 512)
        rand_pos_y = random.randint(0, 512)
        print(f"+++ random x: {rand_pos_x} y: {rand_pos_y}")
        position = bp2.Position(x_pos=rand_pos_x, y_pos=rand_pos_y)

        rand_size_x = random.randint(0, 300)
        rand_size_y = random.randint(0, 300)
        info = bp2.ImgInfo(width=rand_size_x, height=rand_size_y, img_type=bp2.ImgType.RGB)

        _ = stub.SetPosition(position)

        img: bp2.Image = stub.GetPixels(info)
        print(f"+++ image received | width: {img.info.width} height: {img.info.height}")
        print(f"+++ image received | first couple of pixels: {img.pixels[:10]}")


        patches.append(img)
    print("+++ patches sampled")
    
    for i in range(40):
        rand_pos_x = random.randint(0, 800)
        rand_pos_y = random.randint(0, 800)

        pos = bp2.Position(x_pos=rand_pos_x, y_pos=rand_pos_y)
        _ = stub.SetPosition(pos)

        rand_idx = random.randint(0, len(patches)-1)
        img = patches[rand_idx]
        print(f"+++ image sending | width: {img.info.width} height: {img.info.height}")
        print(f"+++ image sending | first couple of pixels: {img.pixels[:10]}")
        _ = stub.SetPixels(img)
    print("+++ patches shuffled")

    # np.

    _ = stub.SaveImage(bp2.Empty())
    print("+++ image saved | client done")


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

