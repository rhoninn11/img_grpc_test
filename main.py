

import img_transfer_pb2_grpc as grpc_gen
import img_transfer_pb2 as bp2

import grpc
import concurrent.futures as futures
from skimage import io
from matplotlib import pyplot as plt

PATCH_SIZE = 256

class ImageTransferServicer(grpc_gen.ImageTransferServicer):
    def __init__(self):
        img_file = "assets/img.png"
        self.image = io.imread(img_file)
        self.img_size = self.image.shape

        self.actual_pos = bp2.Position(x_pos=0, y_pos=0)
        print(f"+++ service_side | ImageTransferServicer | image shape: {self.img_size}")

    def ShowImgOnServer(self, request, context):
        io.imshow(self.image)
        plt.show()

        return bp2.Empty()
    
    def SetPosition(self, request, context) -> bp2.Empty:
        initial_pos = bp2.Position(x_pos=0, y_pos=0)
        print(f"+++ service_side | SetPosition called | input: {request} | some info: {self.actual_pos}")
        self.actual_pos = request
        return bp2.Empty()
    
    def GetPixels(self, request, context):
        x_idx = self.actual_pos.x_pos
        y_idx = self.actual_pos.y_pos
        img_patch = self.image[x_idx:x_idx+PATCH_SIZE, y_idx:y_idx+PATCH_SIZE,:]
        pixel_bytes = img_patch.tobytes()
        print(f"+++ service_side | GetPixels called | shape of patch: {img_patch.shape} dtype: {img_patch.dtype}")
        return bp2.PatchPixels(pixels=pixel_bytes)

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = ImageTransferServicer()
    grpc_gen.add_ImageTransferServicer_to_server(service, server)

    server.add_insecure_port("localhost:50051")
    server.start()
    print("+++ Server started")
    server.wait_for_termination()

import random
import numpy as np
def start_client():
    channel = grpc.insecure_channel("localhost:50051")
    stub = grpc_gen.ImageTransferStub(channel)
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

def test_imshow():
    img_file = "fs/img.png"
    image = io.imread(img_file)
    img_size = image.shape
    io.imshow(image)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="gRPC testin for python")
    parser.add_argument("-s", action="store_true", help="for starting gRPC server")
    parser.add_argument("-c", action="store_true", help="for starting gRPC client")
    parser.add_argument("-t", action="store_true", help="for simple experimntal test run")
    
    args = parser.parse_args()
    if args.s:
        start_server()
    elif args.c:
        start_client()
        pass
    elif args.t:
        test_imshow()
    else:
        parser.print_help()


main()