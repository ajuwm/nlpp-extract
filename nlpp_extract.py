# -*- coding: utf-8 -*-
"""NLPP \u63d2\u753b\u63d0\u53d6\u5de5\u5177  --  New Love Plus+ illustration extractor.

\u628a\u8fd9\u51e0\u8f6e\u8e29\u5751\u5f97\u51fa\u7684\u6b63\u786e\u89e3\u7801\u89c4\u5219\u5c01\u6210\u4e00\u5957\u53ef\u590d\u7528\u7684\u5de5\u5177\u3002\u6240\u6709\u201c\u5fc5\u987b\u8fd9\u4e48\u505a\u201d\u7684\u7406\u7531\u90fd\u5199\u5728\u4ee3\u7801\u91cc\u3002

\u7528\u6cd5
    python nlpp_extract.py list [\u5173\u952e\u8bcd]           \u5217\u51fa\u5f52\u6863
    python nlpp_extract.py members <\u5f52\u6863>             \u5217\u51fa\u6210\u5458\uff08\u542b\u5c3a\u5bf8\u683c\u5f0f\uff09
    python nlpp_extract.py export  <\u5f52\u6863> [--out D]   \u5bfc\u51fa\u5f52\u6863\u5185\u5168\u90e8\u56fe\u50cf
    python nlpp_extract.py tex     <\u540d\u5b57> [--out D]   \u5bfc\u51fa TEXI \u8d34\u56fe
    python nlpp_extract.py clyt    <\u5f52\u6863>             \u663e\u793a CLYT \u5e03\u5c40
    python nlpp_extract.py scene   <\u5f52\u6863> [--out D]   \u6309 CLYT \u5408\u6210\u573a\u666f
    python nlpp_extract.py cg      [--out D]           \u5bfc\u51fa\u753b\u5eca\u5168\u5c3a\u5bf8 CG
    python nlpp_extract.py audit   [--out D]           \u5168\u5e93\u76d8\u70b9\u5206\u7c7b

\u6838\u5fc3\u89c4\u5219\uff08\u90fd\u662f\u9a8c\u8bc1\u8fc7\u7684\uff0c\u4e0d\u8981\u6539\uff09
  1. darc \u540d\u5b57\u8868\uff1aT = \u8282\u70b9\u8868\u8d77\u70b9 + \u8282\u70b9\u6570*12\uff0cT \u5904 6 \u5b57\u8282\u56fa\u5b9a\u4e3a
     00 00 2E 00 00 00\uff08\u6839 "" + \u76ee\u5f55 "."\uff09\u3002\u8282\u70b9\u540d\u504f\u79fb\u76f8\u5bf9 T\u3002
     \u5728 toff+tsize \u9644\u8fd1\u731c\u57fa\u51c6\u4f1a\u62ff\u5230\u771f\u540d\u7684\u540e\u7f00\u3002
  2. CLIM \u5934\u90e8\u5728\u6587\u4ef6\u5757\u3010\u6700\u540e 0x28 \u5b57\u8282\u3011\uff0c\u50cf\u7d20\u5728\u524d\u9762\u3002
  3. \u5c3a\u5bf8\uff1a\u58f0\u660e\u5c3a\u5bf8\u80fd\u6574\u9664\u8f7d\u8377\u65f6\u7528\u58f0\u660e\u5c3a\u5bf8\uff0c\u5426\u5219\u9000\u5230 2 \u7684\u5e42\u6b21\u586b\u5145\u76d2\u5b50\u3002
  4. ETC1A4\uff1a16 \u5b57\u8282/\u5757 = \u3010\u524d 8 \u5b57\u8282 alpha\u3011+\u3010\u540e 8 \u5b57\u8282 ETC1 \u989c\u8272\u3011\uff0c
     8x8 \u74e6\u7247\u88c5 4 \u4e2a 4x4 \u5757\u3002
     alpha \u7684\u5b57\u8282->\u50cf\u7d20\u6620\u5c04\u662f\u3010\u5217\u4f18\u5148 + \u4f4e\u534a\u5b57\u8282\u5728\u524d\u3011\uff1a
         byte j -> \u5217 j//2\uff0c\u884c (j%2)*2 \u548c (j%2)*2+1\uff0c\u4f4e\u534a\u5b57\u8282\u5728\u4e0a\u884c
     \u7528\u9519\u4f1a\u8ba9\u8138\u90e8\u8d34\u56fe\u51fa\u73b0\u9636\u68af\u72b6\u952f\u9f7f\uff08\u7528\u201c\u952f\u9f7f\u91cf\u201d\u6d4b\u51fa\u6765\u7684\uff09\u3002
  5. ETC1\uff1a8 \u5b57\u8282/\u5757\uff0c\u7528 etc1.decode_etc1 (\u5185\u90e8\u6709 _etc1_scramble \u7f6e\u6362)\u3002
  6. TEXI\uff1a\u6570\u636e\u5728\u3010TEX \u8bb0\u5f55\u3011\u91cc\uff08TEXI \u53ea\u662f\u5934\uff09\uff0c\u4e14\u8981\u6309 (name, pack) \u914d\u5bf9\u3002
     \u683c\u5f0f\u53f7\u8d70 .texi \u8868\uff0810=rgba8 11=rgb8 12=etc1 13=etc1a4\uff09\u3002
  7. CLYT\uff1a\u8282\u7684 size \u5b57\u6bb5\u3010\u542b 8 \u5b57\u8282\u6bb5\u5934\u3011\uff0c\u6b65\u8fdb\u662f p += size\u3002
     pane \u7684 (x,y) \u662f\u3010\u4e2d\u5fc3\u3011\uff0cY \u8f74\u5411\u4e0a\u3002
  8. \u5408\u6210\uff1a\u8fb9\u7ebf\u8981\u5148\u5bf9\u9f50\u5230\u540c\u4e00\u6279\u6574\u6570\uff08\u5426\u5219\u7559 1px \u9ed1\u7f1d\uff09\uff1b
     \u5e16\u56fe\u6bd4 pane \u5927\u65f6\u8981\u3010\u88c1\u3011\u4e0d\u8981\u3010\u7f29\u3011\u3002
"""
from __future__ import print_function

import argparse
import collections
import json
import os
import re
import struct
import sys
import zlib

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import etc1            # noqa: E402  (\u53ea\u7528 _etc1_decoded_block / _etc1_scramble)
import nlp_pack as N   # noqa: E402
import rom as R        # noqa: E402

HEAD = 0x28
CLIM_FMT = {0: 'L8', 1: 'A8', 2: 'LA4', 3: 'LA8', 4: 'HILO8', 5: 'RGB565',
            6: 'RGB8', 7: 'RGB5A1', 8: 'RGBA4', 9: 'RGBA8', 10: 'ETC1',
            11: 'ETC1A4', 12: 'L4', 13: 'A4'}
CLIM_BITS = {0: 8, 1: 8, 2: 8, 3: 16, 4: 16, 5: 16, 6: 24, 7: 16, 8: 16, 9: 32,
             10: 4, 11: 8, 12: 4, 13: 4}
# .texi (\u6b27\u6d1e) \u683c\u5f0f\u8868 -- \u548c BCLIM \u8868\u4e0d\u540c\uff0c\u4e0d\u80fd\u6df7
TEXI_FMT = {0: 'l4', 1: 'l8', 2: 'a4', 3: 'la4', 4: 'la8', 5: 'hilo8', 6: 'rgb8',
            7: 'rgb565', 8: 'rgba5551', 9: 'rgba4', 10: 'rgba8', 11: 'rgb8',
            12: 'etc1', 13: 'etc1a4'}

TILE = [0, 1, 8, 9, 2, 3, 10, 11, 16, 17, 24, 25, 18, 19, 26, 27, 4, 5, 12, 13,
        6, 7, 14, 15, 20, 21, 28, 29, 22, 23, 30, 31, 32, 33, 40, 41, 34, 35,
        42, 43, 48, 49, 56, 57, 50, 51, 58, 59, 36, 37, 44, 45, 38, 39, 46, 47,
        52, 53, 60, 61, 54, 55, 62, 63]
SECTION_MAGICS = (b'lyt1', b'txl1', b'fnl1', b'mat1', b'pan1', b'pic1', b'txt1',
                  b'wnd1', b'bnd1', b'pas1', b'pae1', b'grp1', b'grs1', b'gre1',
                  b'usd1')


# =====================================================================  darc
def find_name_table(d, toff, doff):
    """T = \u8282\u70b9\u8868\u8d77\u70b9 + \u8282\u70b9\u6570*12\uff0cT \u5904\u56fa\u5b9a\u4e3a 00 00 2E 00 00 00\u3002"""
    sig = b'\x00\x00\x2e\x00\x00\x00'
    lim = min(doff, len(d))
    i = toff
    while True:
        i = d.find(sig, i, lim)
        if i < 0:
            return None
        if (i - toff) % 12 == 0:
            return i
        i += 2


def _cstr(d, o, limit=256):
    """\u540d\u5b57\u662f UTF-16LE\uff0c\u7ec8\u6b62\u7b26\u662f 2 \u5b57\u8282\u7684 00 00\u3002
    \u5fc5\u987b\u6309 2 \u5b57\u8282\u6b65\u8fdb\u627e\uff1a\u7528 d.find(b'\\x00\\x00') \u4f1a\u5728\u5947\u6570\u5b57\u8282\u547d\u4e2d
    \u534a\u4e2a\u5b57\u7b26\uff0c\u5bfc\u81f4\u540d\u5b57\u622a\u65ad\u6216\u4e3a\u7a7a\u3002"""
    e = o
    end = min(len(d), o + limit * 2)
    while e + 1 < end and d[e:e + 2] != b'\x00\x00':
        e += 2
    try:
        return d[o:e].decode('utf-16-le')
    except Exception:
        return ''


def parse_darc(d):
    """-> [{'path','name','off','size','dir'}]  \u542b\u5b8c\u6574\u76ee\u5f55\u8def\u5f84\u3002"""
    if d[:4] != b'darc':
        return []
    toff = struct.unpack_from('<I', d, 0x10)[0]
    doff = struct.unpack_from('<I', d, 0x18)[0]
    T = find_name_table(d, toff, doff)
    if T is None:
        return []
    n = (T - toff) // 12
    nodes = []
    for i in range(n):
        no, fo, sz = struct.unpack_from('<III', d, toff + i * 12)
        nodes.append({'name': _cstr(d, T + (no & 0xFFFFFF)),
                      'dir': bool(no & 0x01000000), 'off': fo, 'size': sz})
    stack = []
    for i, nd in enumerate(nodes):
        while stack and i > stack[-1][0]:
            stack.pop()
        pref = stack[-1][1] if stack else '.'
        nm = nd['name']
        if pref == '.' and nm in ('.', ''):
            nd['path'] = '.'
        elif pref == '.':
            nd['path'] = './' + nm
        else:
            nd['path'] = pref + '/' + nm
        if nd['dir']:
            stack.append((nd['size'], nd['path']))
    return nodes


def darc_files(d):
    return [x for x in parse_darc(d) if not x['dir'] and x['size']]


# =====================================================================  \u5b58\u50a8\u5c42
class Store(object):
    """img.bin \u91cc\u6240\u6709 .arc\uff0c\u4ee5\u53ca tex_inventory.json\u3002\u4e00\u6b21\u8bfb\u5165\u590d\u7528\u3002"""

    def __init__(self, inv=None):
        self.img = R.find_img()
        self.inv = inv or os.path.join(os.path.dirname(HERE), 'tex_inventory.json')
        self._arcnames = None
        self._arcs = {}
        self._texi = None
        self._tex = None

    def arc_names(self):
        if self._arcnames is None:
            out = []
            with open(self.img, 'rb') as f:
                for p in N.iter_packs(self.img):
                    for pf in p.files:
                        if (pf.name or '').lower().endswith('.arc'):
                            out.append(pf.name)
            self._arcnames = sorted(set(out))
        return self._arcnames

    def arc(self, name):
        """\u8bfb\u4e00\u4e2a\u5f52\u6863\uff1b\u5e26\u7f13\u5b58\u3002\u3010\u5fc5\u987b\u7f13\u5b58\u3011\u5426\u5219\u6bcf\u5f20\u56fe\u90fd\u91cd\u626b img.bin\u3002"""
        if name not in self._arcs:
            got = None
            with open(self.img, 'rb') as f:
                for p in N.iter_packs(self.img):
                    for pf in p.files:
                        if pf.name == name:
                            got = N.pack_bytes(f, pf)
                            break
                    if got is not None:
                        break
            self._arcs[name] = got
        return self._arcs[name]

    def arcs(self, names):
        want = set(names)
        out = {}
        with open(self.img, 'rb') as f:
            for p in N.iter_packs(self.img):
                for pf in p.files:
                    if pf.name in want and pf.name not in out:
                        out[pf.name] = N.pack_bytes(f, pf)
                if len(out) >= len(want):
                    break
        self._arcs.update(out)
        return out

    def _load_inv(self):
        if self._texi is None:
            recs = json.load(open(self.inv, encoding='utf-8'))
            self._texi = {}
            self._tex = {}
            for r in recs:
                if r.get('sig') == 'TEXI' and 'info' in r:
                    key = (r['name'], r['pack'])
                    self._texi.setdefault(key, r)
                elif r.get('sig') == 'TEX':
                    self._tex.setdefault((r['name'], r['pack']), r)

    def texi_list(self):
        self._load_inv()
        return list(self._texi.values())

    def texi_find(self, name):
        """name \u53ef\u4ee5\u5e26\u6216\u4e0d\u5e26 .texi \u540e\u7f00\u3002"""
        self._load_inv()
        if not name.endswith('.texi'):
            name += '.texi'
        hits = [(k, v) for k, v in self._texi.items() if k[0] == name]
        if not hits:
            return None
        key, t = hits[0]
        return t, self._tex.get(key)


# =====================================================================  CLIM \u89e3\u7801
def fit_dims(w, h, nbytes, bits):
    """\u6700\u5c0f\u7684 2 \u7684\u5e42\u6b21\u76d2\u5b50\u3002

    \u4e24\u4e2a\u65b9\u5411\u90fd\u8981\u7b97\uff1a
      * \u58f0\u660e\u5c3a\u5bf8\u592a\u5c0f -> \u8981\u653e\u5927\uff08M_HV_Eye01_01 \u58f0\u660e 64x128\u3001\u5b9e\u5b58 128x128\uff09
      * \u58f0\u660e\u5c3a\u5bf8\u592a\u5927 -> \u8981\u7f29\u5c0f\uff08ExCard \u58f0\u660e 400x400\u3001\u5b9e\u5b58 512x512\uff09
    """
    def pw2(v):
        return max(8, 1 << max(0, (int(v) - 1).bit_length()))
    W0, H0 = pw2(w or 8), pw2(h or 8)
    W, H = W0, H0
    while W * H * bits // 8 < nbytes:          # \u653e\u5927\uff0c\u4f18\u5148\u653e\u5927\u77ed\u8fb9
        if W <= H:
            W *= 2
        else:
            H *= 2
    changed = True
    while changed:                              # \u7f29\u5c0f\uff0c\u4f46\u4e0d\u80fd\u5c0f\u4e8e\u58f0\u660e\u5c3a\u5bf8
        changed = False
        if W > W0 and (W // 2) * H * bits // 8 >= nbytes:
            W //= 2
            changed = True
        elif H > H0 and W * (H // 2) * bits // 8 >= nbytes:
            H //= 2
            changed = True
    return W, H


def dims_for(w, h, nbytes, bits):
    """\u58f0\u660e\u5c3a\u5bf8\u80fd\u7cbe\u786e\u89e3\u91ca\u8f7d\u8377\u5c31\u7528\u58f0\u660e\u5c3a\u5bf8\uff0c\u5426\u5219\u7528 2 \u7684\u5e42\u6b21\u586b\u5145\u3002"""
    if w and h and bits and w * h * bits // 8 == nbytes:
        return w, h, 'declared'
    W, H = fit_dims(w or 8, h or 8, nbytes, bits)
    return W, H, 'padded'


def untile(buf, w, h, bpp):
    buf = np.asarray(bytearray(buf), np.uint8).reshape(-1, bpp)
    out = np.zeros((h, w, bpp), np.uint8)
    off = 0
    for ty in range(h // 8):
        for tx in range(w // 8):
            for p2 in range(64):
                if off >= len(buf):
                    return out
                x = TILE[p2] % 8
                y = (TILE[p2] - x) // 8
                out[ty * 8 + y, tx * 8 + x] = buf[off]
                off += 1
    return out


def etc1a4(pay, w, h):
    """ETC1A4\uff1aalpha \u5728\u524d\uff0c8x8 \u74e6\u7247 4 \u5757\uff0calpha \u5217\u4f18\u5148+\u4f4e\u534a\u5b57\u8282\u5728\u524d\u3002"""
    out = np.zeros((h, w, 4), np.uint8)
    k = 0
    for ty in range(h // 8):
        for tx in range(w // 8):
            for iy in range(2):
                for ix in range(2):
                    o = k * 16
                    k += 1
                    if o + 16 > len(pay):
                        out[:, :, 3] = 255
                        return out
                    a8 = pay[o:o + 8]
                    rgb = np.frombuffer(etc1._etc1_decoded_block(bytes(pay[o + 8:o + 16])),
                                        np.uint8).reshape(16, 4)[:, :3].reshape(4, 4, 3)
                    by, bx = ty * 2 + iy, tx * 2 + ix
                    out[by * 4:by * 4 + 4, bx * 4:bx * 4 + 4, :3] = rgb
                    ab = np.frombuffer(bytes(a8), np.uint8)
                    lo = (ab & 0x0F) * 17
                    hi = ((ab >> 4) & 0x0F) * 17
                    a = np.empty((4, 4), np.uint8)
                    for j in range(8):
                        c = j // 2
                        r0 = (j % 2) * 2
                        a[r0, c] = lo[j]
                        a[r0 + 1, c] = hi[j]
                    out[by * 4:by * 4 + 4, bx * 4:bx * 4 + 4, 3] = a
    return out


def decode_clim(pay, fmt, w, h):
    """\u6309\uff08\u5df2\u77e5\u5b58\u50a8\u5c3a\u5bf8\uff09\u89e3\u4e00\u5f20 CLIM \u50cf\u7d20\u6570\u636e\u3002"""
    bits = CLIM_BITS.get(fmt, 0)
    W, H, how = dims_for(w, h, len(pay), bits)
    f = CLIM_FMT.get(fmt, str(fmt))
    if fmt == 11:
        return etc1a4(pay, W, H), (W, H, how)
    if fmt == 10:
        raw = etc1.decode_etc1(bytes(pay), W, H, alpha=False)
        arr = np.frombuffer(raw, np.uint8)
        return (arr.reshape(H, W, 4) if arr.size == W * H * 4 else None), (W, H, how)
    if fmt == 9:
        t = untile(pay[:W * H * 4], W, H, 4)
        return np.dstack([t[:, :, 3], t[:, :, 2], t[:, :, 1], t[:, :, 0]]), (W, H, how)
    if fmt == 8:
        t = untile(pay[:W * H * 2], W, H, 2).astype(np.uint16)
        v = t[:, :, 0] | (t[:, :, 1] << 8)
        return np.dstack([((v >> 12) & 0xF).astype(np.uint8) * 17,
                          ((v >> 8) & 0xF).astype(np.uint8) * 17,
                          ((v >> 4) & 0xF).astype(np.uint8) * 17,
                          (v & 0xF).astype(np.uint8) * 17]), (W, H, how)
    if fmt == 7:
        t = untile(pay[:W * H * 2], W, H, 2).astype(np.uint16)
        v = t[:, :, 0] | (t[:, :, 1] << 8)
        r = (((v >> 11) & 0x1F) << 3).astype(np.uint8)
        g = (((v >> 5) & 0x3F) << 2).astype(np.uint8)
        bb = ((v & 0x1F) << 3).astype(np.uint8)
        r |= r >> 5
        g |= g >> 6
        bb |= bb >> 5
        return np.dstack([r, g, bb, np.full((H, W), 255, np.uint8)]), (W, H, how)
    if fmt == 6:
        t = untile(pay[:W * H * 3], W, H, 3)
        return np.dstack([t[:, :, 2], t[:, :, 1], t[:, :, 0],
                          np.full((H, W), 255, np.uint8)]), (W, H, how)
    if fmt == 5:
        t = untile(pay[:W * H * 2], W, H, 2).astype(np.uint16)
        v = t[:, :, 0] | (t[:, :, 1] << 8)
        r = (((v >> 11) & 0x1F) << 3).astype(np.uint8)
        g = (((v >> 5) & 0x3F) << 2).astype(np.uint8)
        bb = ((v & 0x1F) << 3).astype(np.uint8)
        r |= r >> 5
        g |= g >> 6
        bb |= bb >> 5
        return np.dstack([r, g, bb, np.full((H, W), 255, np.uint8)]), (W, H, how)
    if fmt == 3:
        t = untile(pay[:W * H * 2], W, H, 2)
        return np.dstack([t[:, :, 0], t[:, :, 0], t[:, :, 0], t[:, :, 1]]), (W, H, how)
    if fmt == 2:
        t = untile(pay[:W * H], W, H, 1)[:, :, 0]
        l = ((t >> 4) & 0xF).astype(np.uint8) * 17
        a = (t & 0xF).astype(np.uint8) * 17
        return np.dstack([l, l, l, a]), (W, H, how)
    if fmt == 1:
        t = untile(pay[:W * H], W, H, 1)
        return np.dstack([t[:, :, 0]] * 3 + [np.full((H, W), 255, np.uint8)]), (W, H, how)
    if fmt == 0:
        t = untile(pay[:W * H], W, H, 1)
        return np.dstack([t[:, :, 0]] * 3 + [np.full((H, W), 255, np.uint8)]), (W, H, how)
    return None, (W, H, how)


def clim_member(d, nd):
    """\u4ece\u5f52\u6863\u91cc\u53d6\u4e00\u4e2a CLIM \u6210\u5458\u7684\u5934\u4fe1\u606f\u3002\u5934\u5728\u5757\u7684\u6700\u540e 0x28 \u5b57\u8282\u3002"""
    if nd['size'] <= HEAD or nd['off'] + nd['size'] > len(d):
        return None
    cl = d[nd['off'] + nd['size'] - HEAD:nd['off'] + nd['size']]
    if cl[:4] != b'CLIM' or cl[0x14:0x18] != b'imag':
        return None
    w, h = struct.unpack_from('<HH', cl, 0x1C)
    f = struct.unpack_from('<I', cl, 0x20)[0]
    pay = d[nd['off']:nd['off'] + nd['size'] - HEAD]
    return {'w': w, 'h': h, 'fmt': f, 'pay': pay}


# =====================================================================  TEXI \u89e3\u7801
def texi_decode(data, w, h, fmt):
    """TEXI \u7528 .texi \u8868\u3002fmt 13 = etc1a4\uff0c\u4e5f\u662f alpha \u5728\u524d\u3002"""
    n = w * h
    if fmt == 13:
        return etc1a4(data, w, h)
    if fmt == 12:
        raw = etc1.decode_etc1(bytes(data), w, h, alpha=False)
        arr = np.frombuffer(raw, np.uint8)
        return arr.reshape(h, w, 4) if arr.size == n * 4 else None
    if fmt == 10:
        t = untile(data[:n * 4], w, h, 4)
        return np.dstack([t[:, :, 3], t[:, :, 2], t[:, :, 1], t[:, :, 0]])
    if fmt == 11:
        t = untile(data[:n * 3], w, h, 3)
        return np.dstack([t[:, :, 2], t[:, :, 1], t[:, :, 0],
                          np.full((h, w), 255, np.uint8)])
    if fmt == 9:
        t = untile(data[:n * 2], w, h, 2).astype(np.uint16)
        v = t[:, :, 0] | (t[:, :, 1] << 8)
        return np.dstack([((v >> 12) & 0xF).astype(np.uint8) * 17,
                          ((v >> 8) & 0xF).astype(np.uint8) * 17,
                          ((v >> 4) & 0xF).astype(np.uint8) * 17,
                          (v & 0xF).astype(np.uint8) * 17])
    if fmt in (7, 8, 6, 5, 4, 3, 1, 2, 0):
        return None          # \u7528\u5230\u518d\u8865\uff0c\u76ee\u524d\u4e3b\u6d41\u5c31\u4e0a\u9762\u51e0\u79cd
    return None


def texi_payload(t, x):
    """t = TEXI \u8bb0\u5f55\uff0cx = \u5339\u914d\u7684 TEX \u8bb0\u5f55\u3002\u6570\u636e\u5728 TEX \u91cc\u3002
    \u4ece\u8bb0\u5f55\u81ea\u5e26\u7684 src \u8bfb\uff1b\u6ca1\u6709 src \u7684\uff08\u65e7\u7248 tex_inventory.json\uff09\u624d\u8bfb ROM\u3002"""
    if x is None:
        return None
    off = x['pack'] + x['cO']
    n = x['cl']
    src = x.get('src')
    if src and os.path.exists(src):
        with open(src, 'rb') as f:
            f.seek(off)
            data = f.read(n)
    else:
        data = R.rd(off, n)
    if x.get('comp'):
        return zlib.decompress(data)
    return data


# =====================================================================  CLYT
def walk_sections(d, base):
    """\u6309\u8282\u957f\u9012\u8fdb\u3002\u3010size \u542b 8 \u5b57\u8282\u6bb5\u5934\u3011\uff0c\u6240\u4ee5\u6b65\u8fdb\u662f p += size\u3002"""
    if d[base:base + 4] != b'CLYT':
        return
    fsize = struct.unpack_from('<I', d, base + 0x0C)[0]
    end = min(len(d), base + max(fsize, 0x14))
    p = base + 0x14
    while p + 8 <= end:
        sig = d[p:p + 4]
        if sig not in SECTION_MAGICS:
            break
        size = struct.unpack_from('<I', d, p + 4)[0]
        if size < 8 or p + size > end:
            break
        yield p, sig, size
        p += size


def clyt_textures(d, base):
    for p, sig, size in walk_sections(d, base):
        if sig != b'txl1':
            continue
        n = struct.unpack_from('<I', d, p + 8)[0]
        out = []
        for k in range(n):
            off = struct.unpack_from('<I', d, p + 0x0C + k * 4)[0]
            e = d.find(b'\x00', p + 0x0C + off, p + size)
            out.append(d[p + 0x0C + off:e].decode('latin1'))
        return out
    return []


def clyt_panes(d, base):
    """pane \u7684 (x,y) \u662f\u3010\u4e2d\u5fc3\u3011\uff0cz \u8d8a\u5c0f\u8d8a\u9760\u540e\u3002"""
    lyt = d.find(b'lyt1', base, base + 0x200)
    cw, ch = struct.unpack_from('<2f', d, lyt + 0x0C)
    out = []
    for p, sig, size in walk_sections(d, base):
        if sig != b'pic1':
            continue
        nm = d[p + 0x0C:p + 0x1C].split(b'\x00')[0].decode('latin1')
        tx, ty, tz = struct.unpack_from('<3f', d, p + 0x24)
        w, h = struct.unpack_from('<2f', d, p + 0x44)
        out.append({'name': nm, 'x': tx, 'y': ty, 'z': tz, 'w': w, 'h': h})
    return int(cw), int(ch), out


def resolve_tex(matname, texnames):
    """\u6750\u8d28\u540d -> \u8d34\u56fe\u540d\u3002\u4e24\u79cd\u5f62\u6001\uff1aPic_Manaka04 -> M_HV_Manaka04\uff08\u540e\u7f00\uff09\uff1b
    R_HV_A_BG_00_00 -> R_HV_A_BG_00\uff08\u591a\u4e00\u4e2a _NN \u5b9e\u4f8b\u53f7\uff09\u3002\u53d6\u6700\u957f\u5339\u914d\u3002"""
    key = matname.split('_', 1)[1] if '_' in matname else matname
    best, score = None, -1
    for t in texnames:
        b = t[:-6] if t.endswith('.bclim') else t
        parts = b.split('_')
        for i in range(len(parts)):
            suf = '_'.join(parts[i:])
            for a, c in ((suf, key), (key, suf)):
                if a == c or c.startswith(a + '_'):
                    if len(a) > score:
                        score, best = len(a), t
    return best


# =====================================================================  \u5408\u6210
def snap_edges(ps, tol=1.5):
    """\u628a\u6240\u6709\u8fb9\u5750\u6807\u805a\u7c7b\u5230\u540c\u4e00\u6279\u6574\u6570\uff0c\u7531\u6574\u6570\u8fb9\u754c\u53cd\u63a8\u6bcf\u5757\u5bbd\u9ad8\u3002
    \u5426\u5219 0.5px \u7684\u504f\u79fb\u4f1a\u53d8\u6210 1 \u50cf\u7d20\u9ed1\u7f1d\u3002"""
    def cluster(vals):
        vals = sorted(set(vals))
        groups, cur = [], [vals[0]]
        for v in vals[1:]:
            if v - cur[-1] <= tol:
                cur.append(v)
            else:
                groups.append(cur)
                cur = [v]
        groups.append(cur)
        reps, m = [], {}
        for g in groups:
            r = int(round(sum(g) / len(g)))
            if reps and r <= reps[-1]:
                r = reps[-1] + 1
            reps.append(r)
            for v in g:
                m[v] = r
        return m
    xs, ys = [], []
    for p in ps:
        xs += [p['x'] - p['w'] / 2.0, p['x'] + p['w'] / 2.0]
        ys += [p['y'] - p['h'] / 2.0, p['y'] + p['h'] / 2.0]
    rx, ry = cluster(xs), cluster(ys)
    out = []
    for p in ps:
        lo, hi = rx[p['x'] - p['w'] / 2.0], rx[p['x'] + p['w'] / 2.0]
        bo, to = ry[p['y'] - p['h'] / 2.0], ry[p['y'] + p['h'] / 2.0]
        out.append((lo, bo, hi - lo, to - bo))
    return out


def compose(pairs, bg=(0, 0, 0, 0)):
    """pairs = [(PIL RGBA, pane)]\u3002pane \u4e2d\u5fc3\u951a\u70b9 + Y \u8f74\u5411\u4e0a\u3002
    \u5e16\u56fe\u6bd4 pane \u5927\u65f6\u88c1\u4e0d\u662f\u7f29\u3002\u8fd4\u56de\u5408\u6210\u540e\u7684 RGBA\u3002"""
    if not pairs:
        return None
    snapped = snap_edges([p for _, p in pairs])
    xs = [s[0] for s in snapped] + [s[0] + s[2] for s in snapped]
    ys = [s[1] for s in snapped] + [s[1] + s[3] for s in snapped]
    ox, oy = min(xs), min(ys)
    ow, oh = max(xs) - ox, max(ys) - oy
    canvas = Image.new('RGBA', (ow, oh), bg)
    order = sorted(range(len(pairs)), key=lambda i: pairs[i][1]['z'])
    for i in order:
        im, p = pairs[i]
        lo, bo, w2, h2 = snapped[i]
        if im.width > w2 or im.height > h2:
            im = im.crop((0, 0, min(w2, im.width), min(h2, im.height)))
        if im.size != (w2, h2):
            im = im.resize((max(1, w2), max(1, h2)), Image.LANCZOS)
        lay = Image.new('RGBA', (ow, oh), (0, 0, 0, 0))
        lay.paste(im, (lo - ox, (oy + oh) - (bo + h2)))     # Y \u8f74\u5411\u4e0a
        canvas = Image.alpha_composite(canvas, lay)
    return canvas


def scenegroup(panes):
    """\u5224\u5b9a\u54ea\u4e9b pane \u662f\u4e92\u65a5\u53d8\u4f53\u3002
    \u540c\u524d\u7f00\uff08\u53bb\u6389\u672b\u5c3e\u4e0b\u5212\u7ebf\u6570\u5b57\u6bb5\uff09\u4e14\u591a\u5757 = \u4e00\u4e2a\u53d8\u4f53\u7684\u74e6\u7247\u65cf\uff1b
    \u5168\u90e8\u90fd\u662f\u5355\u5757 = \u6ca1\u6709\u53d8\u4f53\uff0c\u5168\u90e8\u53e0\u6210\u4e00\u5f20\u3002"""
    groups = collections.OrderedDict()
    for p in panes:
        parts = p['name'].split('_')
        while len(parts) > 1 and parts[-1].isdigit():
            parts.pop()
        groups.setdefault('_'.join(parts), []).append(p)
    multi = collections.OrderedDict((k, v) for k, v in groups.items() if len(v) > 1)
    if not multi:
        return [('all', panes)]
    shared = [p for v in groups.values() if len(v) == 1 for p in v]
    return [(k, v + shared) for k, v in multi.items()]


# =====================================================================  \u5206\u7c7b
KIND_RULES = [
    ('scene', ('_bg', 'bg_', 'bg0', 'bg1', 'bg2', 'shakou', 'yuge', 'potechi',
               'messageboard')),
    ('face', ('eye', 'mouth', 'eyebrow', 'cheek', 'face', 'lip', 'brow')),
    ('cloth', ('t_shirt', 't-shirt', 'zipper', 'tail', 'beard', 'leaf', 'ribon')),
    ('effect', ('effect', 'ef', 'bubble', 'fire', 'firefly', 'petal', 'sakura',
                'shabon', 'shadow', 'smoke', 'spray', 'star', 'steam', 'sweat',
                'water', 'num', 'skip', 'kira', 'hotaru', 'obj', 'letter',
                'missile', 'mp3', 'pcmonitor', 'plaster', 'mogura')),
    ('body', ('body', 'arm', 'hip')),
]


def classify(name):
    n = name.lower()
    for kind, keys in KIND_RULES:
        for w in keys:
            if w in n:
                return kind
    return 'other'


def owner(name):
    m = re.match(r'^([MNRmnr])_', name)
    if not m:
        return 'common'
    return {'M': 'M', 'N': 'N', 'R': 'R'}[m.group(1).upper()]


# =====================================================================  CLI
def build_inventory(img, out=None, verbose=False):
    """\u81ea\u5df1\u626b\u51fa\u8d34\u56fe\u7d22\u5f15\uff0c\u53d6\u4ee3 tex_inventory.json\u3002

    TEXI \u662f SERI \u5e8f\u5217\u5316\u5757\uff0c\u5b57\u6bb5\u5728\u5305\u7684 strptr/strtab \u91cc\u3002
    \u6bcf\u4e2a\u5305\u90fd\u6709\u81ea\u5df1\u7684 strptr/strtab\uff0c\u6240\u4ee5\u5fc5\u987b\u9010\u5305\u53d6\u3002
    """
    recs = []
    with open(img, 'rb') as f:
        for p in N.iter_packs(img):
            if not getattr(p, 'file_count', 0):
                continue
            try:
                f.seek(p.strptrs_off)
                strptrs = struct.unpack_from('<%dI' % p.file_count,
                                             f.read(p.file_count * 4), 0)
                f.seek(p.strtab_off)
                strtab = f.read(max(0x1000, min(0x100000,
                                                max(0, p.end - p.strtab_off))))
            except Exception:
                continue
            for pf in p.files:
                sig = (pf.signature_str or '').strip()
                if sig not in ('TEXI', 'TEX'):
                    continue
                try:
                    blk = N.pack_bytes(f, pf)
                except Exception:
                    continue
                base = getattr(pf, 'pack_base', None) or getattr(p, 'base', None) or 0
                # \u3010\u5173\u952e\u3011pf.comp_off / pf.raw_off \u662f\u5305\u5185\u7edd\u5bf9\u504f\u79fb\uff0c
                # \u800c\u8bb0\u5f55\u91cc\u7684 cO/dO \u5e94\u8be5\u662f\u3010\u76f8\u5bf9\u5305\u57fa\u5740\u3011\u7684\u3002
                # \u9a8c\u8bc1\uff1a356436736-155797504 = 200639232 \u6070\u7b49\u4e8e\u65e7\u8bb0\u5f55\u7684 dO\uff1b
                #       249200432-155797504 =  93402928 \u6070\u7b49\u4e8e\u65e7\u8bb0\u5f55\u7684 cO\u3002
                rec = {'name': pf.name, 'sig': 'TEXI' if sig == 'TEXI' else 'TEX',
                       'pack': base,
                       'dO': getattr(pf, 'raw_off', 0) - base,
                       'dl': getattr(pf, 'raw_len', 0),
                       'comp': bool(getattr(pf, 'compressed', False)),
                       'cO': getattr(pf, 'comp_off', 0) - base,
                       'cl': getattr(pf, 'comp_len', 0),
                       # \u8bb0\u5f55\u6570\u636e\u6e90\u3002\u65e7\u7248 tex_inventory.json \u7528\u89e3\u5bc6 ROM \u7684\u7edd\u5bf9\u504f\u79fb\uff1b
                       # \u626b img.bin \u5f97\u5230\u7684\u662f img.bin \u5185\u7684\u504f\u79fb\u3002\u8bfb\u7684\u65f6\u5019\u8981\u8bfb\u540c\u4e00\u4e2a\u6587\u4ef6\u3002
                       'src': os.path.abspath(img)}
                if sig == 'TEXI':
                    s = N.parse_seri_block(blk, strptrs, strtab)
                    if s is None:
                        continue
                    rec['info'] = s.params
                recs.append(rec)
                if verbose and len(recs) % 2000 == 0:
                    print('   ... %d' % len(recs), flush=True)
    if out:
        json.dump(recs, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    return recs


def cmd_scan(st, args):
    img = args.img or st.img
    out = args.out or os.path.join(os.path.dirname(st.inv), 'tex_inventory.json')
    print('\u626b\u63cf %s' % img)
    recs = build_inventory(img, out, verbose=True)
    n_texi = sum(1 for r in recs if r['sig'] == 'TEXI')
    n_tex = sum(1 for r in recs if r['sig'] == 'TEX')
    print('TEXI %d  TEX %d  \u5408\u8ba1 %d -> %s' % (n_texi, n_tex, len(recs), out))
    return 0


def cmd_list(st, args):
    names = st.arc_names()
    pat = re.compile(args.pattern, re.I) if args.pattern else None
    hit = [n for n in names if not pat or pat.search(n)]
    for n in hit:
        print(n)
    print('-- %d / %d' % (len(hit), len(names)))


def cmd_members(st, args):
    d = st.arc(args.arc)
    if d is None:
        print('\u627e\u4e0d\u5230 %s' % args.arc)
        return 1
    for nd in darc_files(d):
        c = clim_member(d, nd)
        if not c:
            print('%-44s %8d  %s' % (nd['path'], nd['size'], d[nd['off']:nd['off'] + 4]))
            continue
        W, H, how = dims_for(c['w'], c['h'], len(c['pay']), CLIM_BITS.get(c['fmt'], 8))
        print('%-44s %8d  %-8s %4dx%-4d -> %dx%d (%s)'
              % (nd['path'], nd['size'], CLIM_FMT.get(c['fmt'], c['fmt']),
                 c['w'], c['h'], W, H, how))
    return 0


def cmd_export(st, args):
    d = st.arc(args.arc)
    if d is None:
        print('\u627e\u4e0d\u5230 %s' % args.arc)
        return 1
    out = args.out or os.path.join('out', args.arc[:-4])
    os.makedirs(out, exist_ok=True)
    n = 0
    for nd in darc_files(d):
        c = clim_member(d, nd)
        if not c:
            continue
        img, _ = decode_clim(c['pay'], c['fmt'], c['w'], c['h'])
        if img is None:
            continue
        base = os.path.basename(nd['path'])
        base = base[:-6] if base.endswith('.bclim') else base
        Image.fromarray(img).save(os.path.join(out, '%s.png' % base))
        n += 1
    print('%d \u5f20 -> %s' % (n, out))
    return 0


def cmd_tex(st, args):
    hit = st.texi_find(args.name)
    if not hit:
        print('\u627e\u4e0d\u5230 %s' % args.name)
        return 1
    t, x = hit
    data = texi_payload(t, x)
    if data is None:
        print('\u6ca1\u6709 TEX \u6570\u636e')
        return 1
    i = t['info']
    img = texi_decode(data, i['w'], i['h'], i['format'])
    if img is None:
        print('\u683c\u5f0f %s \u5c1a\u672a\u652f\u6301' % i['format'])
        return 1
    out = args.out or 'out'
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, '%s_%dx%d.png' % (args.name.replace('.texi', ''),
                                            i['w'], i['h']))
    Image.fromarray(img).save(p)
    print('-> %s  %dx%d %s' % (p, i['w'], i['h'], TEXI_FMT.get(i['format'], '?')))
    return 0


def cmd_clyt(st, args):
    d = st.arc(args.arc)
    if d is None:
        print('\u627e\u4e0d\u5230 %s' % args.arc)
        return 1
    for nd in darc_files(d):
        if d[nd['off']:nd['off'] + 4] != b'CLYT':
            continue
        secs = list(walk_sections(d, nd['off']))
        cw, ch, ps = clyt_panes(d, nd['off'])
        texs = clyt_textures(d, nd['off'])
        print('=== %s  \u8282=%d  pane=%d  \u753b\u5e03 %dx%d'
              % (nd['path'], len(secs), len(ps), cw, ch))
        print('  \u7eb9\u7406 %d: %s' % (len(texs), ', '.join(texs[:10])))
        for p in sorted(ps, key=lambda q: q['z']):
            t = resolve_tex(p['name'], texs)
            print('   z=%7.2f %-24s %-26s \u4e2d\u5fc3(%7.1f,%7.1f) %4.0fx%-4.0f'
                  % (p['z'], p['name'], t or '-', p['x'], p['y'], p['w'], p['h']))
    return 0


def cmd_scene(st, args):
    d = st.arc(args.arc)
    if d is None:
        print('\u627e\u4e0d\u5230 %s' % args.arc)
        return 1
    idx = {}
    for nd in darc_files(d):
        base = os.path.basename(nd['path'])
        base = base[:-6] if base.endswith('.bclim') else base
        c = clim_member(d, nd)
        if c:
            img, _ = decode_clim(c['pay'], c['fmt'], c['w'], c['h'])
            if img is not None:
                idx[base] = img
    out = args.out or 'out'
    made = 0
    for nd in darc_files(d):
        if d[nd['off']:nd['off'] + 4] != b'CLYT':
            continue
        cw, ch, ps = clyt_panes(d, nd['off'])
        texs = clyt_textures(d, nd['off'])
        for gname, group in scenegroup(ps):
            pairs = []
            miss = 0
            for p in group:
                t = resolve_tex(p['name'], texs)
                key = t[:-6] if t and t.endswith('.bclim') else t
                if key not in idx:
                    miss += 1
                    continue
                pairs.append((Image.fromarray(idx[key]), p))
            if not pairs:
                continue
            img = compose(pairs)
            os.makedirs(out, exist_ok=True)
            base = os.path.basename(nd['path'])[:-6]
            nm = '%s__%s_%dx%d.png' % (args.arc[:-4], gname, img.width, img.height)
            Image.fromarray(np.asarray(img)).save(os.path.join(out, nm))
            wh = Image.new('RGBA', img.size, (255, 255, 255, 255))
            Image.alpha_composite(wh, img).convert('RGB').save(
                os.path.join(out, nm.replace('.png', '_white.png')))
            print('  %-46s %dx%d  \u5c42%d  \u7f3a%d'
                  % (nm, img.width, img.height, len(pairs), miss))
            made += 1
    print('%d \u5f20 -> %s' % (made, out))
    return 0


def cmd_audit(st, args):
    """\u628a\u5168\u5e93 CLIM \u6210\u5458\u6309 \u5f52\u5c5e x \u7c7b\u578b \u5206\u7c7b\u5bfc\u51fa\u3002"""
    names = st.arc_names()
    print('\u5f52\u6863 %d \u4e2a' % len(names))
    out = args.out or 'out'
    rows = []
    n = 0
    for nm in names:
        d = st.arc(nm)
        if d is None or d[:4] != b'darc':
            continue
        for nd in darc_files(d):
            c = clim_member(d, nd)
            if not c:
                continue
            base = os.path.basename(nd['path'])
            stem = base[:-6] if base.endswith('.bclim') else base
            who, kind = owner(stem), classify(stem)
            sub = os.path.join(out, '%s_%s' % (who, kind))
            os.makedirs(sub, exist_ok=True)
            img, dim = decode_clim(c['pay'], c['fmt'], c['w'], c['h'])
            if img is None:
                continue
            Image.fromarray(img).save(os.path.join(sub, '%s__%s.png' % (nm[:-4], stem)))
            rows.append((who, kind, nm, stem, c['w'], c['h'], c['fmt'], dim[2]))
            n += 1
            if n % 200 == 0:
                print('   ... %d' % n, flush=True)
    with open(os.path.join(out, 'manifest.tsv'), 'w', encoding='utf-8') as f:
        f.write('owner\tkind\tarchive\tmember\tw\th\tfmt\tsize\n')
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    c = collections.Counter((r[0], r[1]) for r in rows)
    for k in sorted(c):
        print('   %-8s %-8s %d' % (k[0], k[1], c[k]))
    print('%d \u5f20 -> %s' % (n, out))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='NLPP \u63d2\u753b\u63d0\u53d6\u5de5\u5177')
    sub = ap.add_subparsers(dest='cmd')

    p = sub.add_parser('list', help='\u5217\u51fa\u5f52\u6863')
    p.add_argument('pattern', nargs='?')
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser('members', help='\u5217\u51fa\u5f52\u6863\u6210\u5458')
    p.add_argument('arc')
    p.set_defaults(fn=cmd_members)

    p = sub.add_parser('export', help='\u5bfc\u51fa\u5f52\u6863\u5185\u56fe\u50cf')
    p.add_argument('arc')
    p.add_argument('--out')
    p.set_defaults(fn=cmd_export)

    p = sub.add_parser('tex', help='\u5bfc\u51fa TEXI \u8d34\u56fe')
    p.add_argument('name')
    p.add_argument('--out')
    p.set_defaults(fn=cmd_tex)

    p = sub.add_parser('clyt', help='\u663e\u793a\u5e03\u5c40')
    p.add_argument('arc')
    p.set_defaults(fn=cmd_clyt)

    p = sub.add_parser('scene', help='\u6309\u5e03\u5c40\u5408\u6210\u573a\u666f')
    p.add_argument('arc')
    p.add_argument('--out')
    p.set_defaults(fn=cmd_scene)

    p = sub.add_parser('scan', help='\u626b\u51fa\u8d34\u56fe\u7d22\u5f15\uff08\u53d6\u4ee3 tex_inventory.json\uff09')
    p.add_argument('--img')
    p.add_argument('--out')
    p.set_defaults(fn=cmd_scan)

    p = sub.add_parser('audit', help='\u5168\u5e93\u76d8\u70b9\u5206\u7c7b')
    p.add_argument('--out')
    p.set_defaults(fn=cmd_audit)

    args = ap.parse_args(argv)
    if not getattr(args, 'fn', None):
        ap.print_help()
        return 0
    st = Store()
    return args.fn(st, args)


if __name__ == '__main__':
    sys.exit(main())
