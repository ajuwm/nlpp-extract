# -*- coding: utf-8 -*-
"""Lazy ROM / img.bin access.  Nothing is opened until it is actually used."""

import os

IMG_CANDIDATES = (
    r'D:/dsh/nlpp/img.bin',
    r'D:/dsh/NLPP/NLPP_CHN_2_1_1/00040000000F4E00/romfs/img.bin',
    r'D:/dsh/nlpp/out/cia_build/full/romfs/img.bin',
)
ROM_CANDIDATES = (
    r'E:/\u6742/kirin-nlppj-dec.3ds',
    r'E:/杂/kirin-nlppj-dec.3ds',
)

_rom = None


def find_img():
    v = os.environ.get('NLPP_IMG')
    if v and os.path.exists(v):
        return v
    for p in IMG_CANDIDATES:
        if os.path.exists(p):
            return p
    raise IOError('img.bin \u672a\u627e\u5230\uff0c\u8bbe NLPP_IMG \u73af\u5883\u53d8\u91cf')


def find_rom():
    v = os.environ.get('NLPP_ROM')
    if v and os.path.exists(v):
        return v
    for p in ROM_CANDIDATES:
        if os.path.exists(p):
            return p
    raise IOError('ROM \u672a\u627e\u5230\uff0c\u8bbe NLPP_ROM \u73af\u5883\u53d8\u91cf')


def rd(off, n):
    """Read n bytes from the decrypted ROM at absolute offset off."""
    global _rom
    if _rom is None:
        _rom = open(find_rom(), 'rb')
    _rom.seek(off)
    return _rom.read(n)
