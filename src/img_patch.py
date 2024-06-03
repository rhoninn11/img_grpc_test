
import proto.img_patch_pb2_grpc as pb2_grpc
import proto.img_patch_pb2 as bp2

import grpc
import asyncio

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