
import proto.img_patch_pb2_grpc as pb2_grpc
import proto.img_patch_pb2 as bp2

import os
import grpc
import asyncio

import numpy as np
from skimage import io
from matplotlib import pyplot as plt

PATCH_SIZE = 256

class ImgPatchService(pb2_grpc.ImgPatchServicer):
    def __init__(self):
        img_file = "assets/img.png"
        self.image = io.imread(img_file)
        self.img_size = self.image.shape

        self.actual_pos = bp2.Position(x_pos=0, y_pos=0)
        print(f"+++ service_side | ImageTransferServicer | image shape: {self.img_size}")

    def size_validation(self, img_info: bp2.ImgInfo):
        x_pos = self.actual_pos.x_pos
        y_pos = self.actual_pos.y_pos

        x_posible = self.img_size[0] - x_pos
        y_posible = self.img_size[1] - y_pos

        x_size = x_posible if img_info.width > x_posible else img_info.width
        y_size = y_posible if img_info.height > y_posible else img_info.height

        return x_pos, y_pos, x_size, y_size
    
    def SetPosition(self, request: bp2.Position, context) -> bp2.Empty:
        initial_pos = bp2.Position(x_pos=0, y_pos=0)
        print(f"+++ service_side | SetPosition called")
        self.actual_pos = request
        return bp2.Empty()
    
    def GetPixels(self, request: bp2.ImgInfo, context) -> bp2.Image:
        print(f"+++ service_side | GetPixels called")
        x_pos, y_pos, x_size, y_size = self.size_validation(request)

        img_patch = self.image[x_pos:x_pos+x_size, y_pos:y_pos+y_size,:]
        pixel_bytes = img_patch.tobytes()

        info = bp2.ImgInfo(width=x_size, height=y_size, img_type=bp2.ImgType.RGB)
        img = bp2.Image(info=info, pixels=pixel_bytes)

        return img
    
    def SetPixels(self, request: bp2.Image, context) -> bp2.ImgInfo:
        print(f"+++ service_side | SetPixels called")
        x_pos, y_pos, x_size, y_size = self.size_validation(request.info)
        np_pix = np.frombuffer(request.pixels, dtype=np.uint8)
        np_pix = np_pix.reshape((request.info.width, request.info.height, 3))

        print(f"+++ service_side | SetPixels | np_pix shape: {np_pix.shape}")
        self.image[x_pos:x_pos+x_size, y_pos:y_pos+y_size,:] = np_pix[0:x_size, 0:y_size,:]
        request.info.width = x_size
        request.info.height = y_size
        return request.info
    
    def SaveImage(self, request: bp2.Empty, context) -> bp2.Empty:
        os.makedirs("fs", exist_ok=True)
        io.imsave("fs/img.png", self.image)
        print(f"+++ service_side | SaveImage called")
        return bp2.Empty()