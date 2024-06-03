


import os
import sys
src_root = 'src'
proto_root = 'src/proto'

src_root = os.path.abspath(src_root)
proto_root = os.path.abspath(proto_root)

paths = []
if src_root not in sys.path:
    sys.path.append(src_root)

if proto_root not in sys.path:
    sys.path.append(proto_root)

from src.prog_cli import main

main()