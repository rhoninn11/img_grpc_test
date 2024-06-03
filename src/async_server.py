import proto.img_patch_pb2_grpc as pb2_grpc
import proto.img_patch_pb2 as bp2

import grpc
from img_patch import ImgPatchService

async def start_server() -> None:
    server = grpc.aio.server()

    pb2_grpc.add_ImgPatchServicer_to_server(
        ImgPatchService(), server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()

import asyncio
def start_server_asyn() -> None:
    asyncio.run(start_server())