#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os

import grpc
from google.protobuf.any_pb2 import Any

import gobgp_pb2
import gobgp_pb2_grpc
import attribute_pb2

_TIMEOUT_SECONDS = 1000


def run():
    bgppeer_ip = os.environ.get("PEER_IP")
    channel = grpc.insecure_channel(f'{bgppeer_ip}:50051')
    stub = gobgp_pb2_grpc.GobgpApiStub(channel)

    nlri = Any()
    nlri.Pack(attribute_pb2.IPAddressPrefix(
        prefix_len=24,
        prefix="12.0.0.0",
    ))

    res = stub.ListPath(
        gobgp_pb2.ListPathRequest(
            table_type=gobgp_pb2.GLOBAL,
            family=gobgp_pb2.Family(afi=gobgp_pb2.Family.AFI_IP, safi=gobgp_pb2.Family.SAFI_UNICAST)
           ),
        _TIMEOUT_SECONDS,
    )

    for r in res:
        print(r)

if __name__ == '__main__':
    run()
