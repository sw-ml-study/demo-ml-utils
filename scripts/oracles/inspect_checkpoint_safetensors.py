#!/usr/bin/env python3
"""Independent stdlib-only fixture/Safetensors oracle; deliberately never unpickles."""
import json
import struct
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def stored_members(path):
    data = open(path, "rb").read()
    cursor = 0
    members = {}
    while data[cursor : cursor + 4] == b"PK\x03\x04":
        fields = struct.unpack_from("<HHHHHIIIHH", data, cursor + 4)
        flags, method, compressed, uncompressed, name_len, extra_len = (
            fields[1], fields[2], fields[6], fields[7], fields[8], fields[9]
        )
        if flags or method or compressed != uncompressed or extra_len:
            raise ValueError("oracle accepts only stored, unflagged fixture members")
        start = cursor + 30 + name_len
        end = start + compressed
        name = data[cursor + 30 : start].decode("utf-8")
        if name in members:
            raise ValueError(f"duplicate ZIP member: {name}")
        members[name] = data[start:end]
        cursor = end
    return data, members


def safetensors(path):
    data = open(path, "rb").read()
    header_len = struct.unpack_from("<Q", data, 0)[0]
    header = json.loads(
        data[8 : 8 + header_len].decode("utf-8"), object_pairs_hook=unique_object
    )
    return data, header, data[8 + header_len :]


source_bytes, members = stored_members(sys.argv[1])
output_bytes, header, payload = safetensors(sys.argv[2])
expected_info = {"dtype": "I16", "shape": [2, 2], "data_offsets": [0, 8]}
if set(members) != {"data.pkl", "data/0"}:
    raise SystemExit("unexpected checkpoint members")
if header != {"tensor_a": expected_info}:
    raise SystemExit("unexpected Safetensors header")
if payload != members["data/0"]:
    raise SystemExit("source/output payload bytes differ")
values = list(struct.unpack("<hhhh", payload))
if values != [1, -2, 300, 512]:
    raise SystemExit("decoded tensor values differ")
print(json.dumps({
    "checkpoint_bytes": len(source_bytes),
    "checkpoint_members": sorted(members),
    "dtype": expected_info["dtype"],
    "output_bytes": len(output_bytes),
    "payload_bytes": len(payload),
    "payload_equal": True,
    "shape": expected_info["shape"],
    "tensor": "tensor_a",
    "values": values,
}, sort_keys=True, separators=(",", ":")))
