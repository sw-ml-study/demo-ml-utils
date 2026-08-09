#!/usr/bin/env python3
"""Independent standard-library oracle for the tiny single-tensor GGUF slice."""
import hashlib
import json
import struct
import sys

data = open(sys.argv[1], "rb").read()
cursor = 0

def take(fmt):
    global cursor
    size = struct.calcsize(fmt)
    value = struct.unpack_from(fmt, data, cursor)[0]
    cursor += size
    return value

def text():
    global cursor
    size = take("<Q")
    value = data[cursor:cursor + size].decode("utf-8")
    cursor += size
    return value

assert data[:4] == b"GGUF"
cursor = 4
version, tensors, metadata = take("<I"), take("<Q"), take("<Q")
meta = {}
for _ in range(metadata):
    key, kind = text(), take("<I")
    meta[key] = text() if kind == 8 else take("<I")
name, dimensions = text(), take("<I")
shape = [take("<Q") for _ in range(dimensions)]
type_id, offset = take("<I"), take("<Q")
data_start = (cursor + 31) // 32 * 32
assert data[cursor:data_start] == bytes(data_start - cursor)
values = list(struct.unpack_from("<hhh", data, data_start + offset))
print(json.dumps({
    "architecture": meta["general.architecture"],
    "file_bytes": len(data),
    "metadata": metadata,
    "name": name,
    "offset": offset,
    "sha256": hashlib.sha256(data).hexdigest(),
    "shape": shape,
    "tensors": tensors,
    "type_id": type_id,
    "values": values,
    "version": version,
}, sort_keys=True, separators=(",", ":")))
