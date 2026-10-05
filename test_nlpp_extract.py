# -*- coding: utf-8 -*-
"""\u6d4b\u8bd5\u3002\u8dd1\u6cd5\u4e8c\u9009\u4e00\uff1a

    pytest -q                       (\u88c5\u4e86 pytest)
    python test_nlpp_extract.py     (\u6ca1\u88c5 pytest \u4e5f\u80fd\u8dd1\uff0c\u672c\u6587\u4ef6\u5e26\u4e00\u4e2a\u6781\u7b80\u8dd1\u5668)

\u6570\u636e\u4e0d\u5728\u5c31\u81ea\u52a8 skip\uff0c\u6240\u4ee5\u5728 CI \u4e0a\u4e5f\u80fd\u8dd1\u3002
"""
import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nlpp_extract as X          # noqa: E402

try:
    import pytest
    _HAVE_PYTEST = True
except ImportError:
    _HAVE_PYTEST = False

    class _Skip(Exception):
        pass

    class _Mark(object):
        def __getattr__(self, _):

            def deco(*a, **k):
                if len(a) == 1 and callable(a[0]):
                    return a[0]

                def wrap(f):
                    return f
                return wrap
            return deco

    class _Pytest(object):
        mark = _Mark()

        @staticmethod
        def skip(msg=''):
            raise _Skip(msg)
    pytest = _Pytest()


def _store():
    try:
        return X.Store()
    except IOError:
        pytest.skip('\u6ca1\u6709 img.bin\uff0c\u8bbe NLPP_IMG \u73af\u5883\u53d8\u91cf')


# ============================================================ \u7eaf\u51fd\u6570
def test_owner():
    assert X.owner('M_HV_Body') == 'M'
    assert X.owner('R_HV_A_BG_00') == 'R'
    assert X.owner('n_eye') == 'N'
    assert X.owner('Com_black_00') == 'common'


def test_classify():
    assert X.classify('M_HV_BG_00') == 'scene'
    assert X.classify('M_HV_Eye01a_01') == 'face'
    assert X.classify('N_HV_T-shirt01') == 'cloth'
    assert X.classify('M_HV_Sakura00') == 'effect'
    assert X.classify('M_HV_Body') == 'body'
    assert X.classify('Com_black_00') == 'other'


def test_dims_declared_vs_padded():
    # 128x128 ETC1A4 = 16384 \u5b57\u8282 -> \u58f0\u660e\u5c3a\u5bf8\u6210\u7acb
    assert X.dims_for(128, 128, 16384, 8) == (128, 128, 'declared')
    # \u58f0\u660e 64x128\uff08M_HV_Eye01_01\uff09\u4f46\u8f7d\u8377 16384 -> \u5b9e\u5b58 128x128\uff0c\u5fc5\u987b\u653e\u5927
    assert X.dims_for(64, 128, 16384, 8) == (128, 128, 'padded')
    # ExCard\uff1a\u58f0\u660e 400x400\uff0c\u5b9e\u5b58 512x512 ETC1
    assert X.dims_for(400, 400, 131072, 4) == (512, 512, 'padded')
    # \u58f0\u660e\u592a\u5927 -> \u7f29\u5c0f
    assert X.dims_for(1024, 1024, 262144, 8) == (1024, 1024, 'padded')


def test_snap_edges_no_gap():
    ps = [{'name': 'a', 'x': -293.0, 'y': 0.0, 'z': 0, 'w': 73.0, 'h': 160.0},
          {'name': 'b', 'x': -128.0, 'y': 0.0, 'z': 0, 'w': 256.0, 'h': 160.0}]
    s = X.snap_edges(ps)
    assert s[0][0] + s[0][2] == s[1][0], '\u5de6\u5757\u53f3\u8fb9\u5fc5\u987b\u7b49\u4e8e\u53f3\u5757\u5de6\u8fb9'


def test_clyt_section_walk_size_includes_header():
    """\u8282\u7684 size \u542b 8 \u5b57\u8282\u6bb5\u5934\uff0c\u6b65\u8fdb\u662f +size\u3002
    \u5199\u6210 +8+size \u5c31\u4f1a\u8d8a\u8fc7\u7b2c\u4e8c\u8282\u3002
    """
    body = bytearray()
    body += b'lyt1' + struct.pack('<I', 20) + struct.pack('<I', 1) \
        + struct.pack('<2f', 400.0, 240.0)
    blob = bytearray(b'CLYT' + b'\xff\xfe' + struct.pack('<H', 0x14)
                     + struct.pack('<I', 0x02020000)
                     + struct.pack('<I', 0x14 + len(body))
                     + struct.pack('<H', 1) + b'\x00\x00')
    blob += body
    sigs = [s for _, s, _ in X.walk_sections(bytes(blob), 0)]
    assert sigs == [b'lyt1']


def test_etc1a4_alpha_column_major():
    """col = j//2\uff0crow = (j%2)*2 \u548c +1\uff0c\u4f4e\u534a\u5b57\u8282\u5728\u4e0a\u884c\u3002"""
    pay = bytearray(64)
    for j in range(4):
        pay[j] = 0x0F
    for j in range(4, 8):
        pay[j] = 0xF0
    a = X.etc1a4(bytes(pay), 8, 8)[:4, :4, 3]
    assert a[0, 0] == 0x0F * 17      # byte0 lo -> [0,0]
    assert a[1, 0] == 0x00           # byte0 hi -> [1,0]
    assert a[2, 0] == 0x0F * 17      # byte1 lo -> [2,0]
    assert a[3, 0] == 0x00
    assert a[0, 1] == 0x0F * 17      # byte2 -> \u5217 1
    assert a[0, 2] == 0x00           # byte4 lo -> [0,2]
    assert a[1, 2] == 0x0F * 17      # byte4 hi -> [1,2]


def test_resolve_tex_both_shapes():
    texs = ['M_HV_Manaka04.bclim', 'R_HV_A_BG_00.bclim', 'R_HV_A_BG02_00.bclim']
    assert X.resolve_tex('Pic_Manaka04', texs) == 'M_HV_Manaka04.bclim'
    assert X.resolve_tex('R_HV_A_BG_00_00', texs) == 'R_HV_A_BG_00.bclim'
    assert X.resolve_tex('R_HV_A_BG02_00_00', texs) == 'R_HV_A_BG02_00.bclim'


# ============================================================ \u9760\u6570\u636e
def test_darc_names_are_full():
    st = _store()
    d = st.arc('HV_BG.arc')
    if d is None:
        pytest.skip('HV_BG.arc \u4e0d\u5728')
    names = [os.path.basename(x['path']) for x in X.darc_files(d)]
    assert 'M_HV_Manaka07.bclim' in names
    assert 'BG.bclyt' in names


def test_clim_header_at_end_of_block():
    st = _store()
    d = st.arc('HV_BG.arc')
    if d is None:
        pytest.skip('HV_BG.arc \u4e0d\u5728')
    got = 0
    for nd in X.darc_files(d):
        c = X.clim_member(d, nd)
        if not c:
            continue
        assert nd['size'] - X.HEAD == len(c['pay'])
        got += 1
    assert got >= 14


def test_clyt_section_count_matches_header():
    """\u8d70\u51fa\u7684\u8282\u6570\u5fc5\u987b\u7b49\u4e8e\u6587\u4ef6\u5934\u58f0\u660e\u7684 nsec\u3002"""
    st = _store()
    for arc, want in (('HV_BG.arc', 27), ('BG.arc', 29), ('HV_BG01.arc', 45),
                      ('HV_BG02.arc', 13)):
        d = st.arc(arc)
        if d is None:
            continue
        for nd in X.darc_files(d):
            if d[nd['off']:nd['off'] + 4] != b'CLYT':
                continue
            nsec = struct.unpack_from('<H', d, nd['off'] + 0x10)[0]
            got = len(list(X.walk_sections(d, nd['off'])))
            assert got == nsec, '%s: \u8d70\u51fa %d \u8282\uff0c\u5934\u90e8\u58f0\u660e %d' % (arc, got, nsec)
            assert nsec == want


def test_scene_pane_counts():
    st = _store()
    want = {'HV_BG.arc': (14, 'M_HV_Manaka07.bclim'),
            'BG.arc': (16, 'M_HV_BG_04.bclim'),
            'HV_BG01.arc': (24, 'R_HV_A_BG_00.bclim')}
    for arc, (n, sample) in want.items():
        d = st.arc(arc)
        if d is None:
            continue
        for nd in X.darc_files(d):
            if d[nd['off']:nd['off'] + 4] != b'CLYT':
                continue
            cw, ch, ps = X.clyt_panes(d, nd['off'])
            texs = X.clyt_textures(d, nd['off'])
            assert len(ps) == n
            assert (cw, ch) == (400, 240)
            assert sample in texs


def _bg_scene_pairs(st):
    from PIL import Image
    d = st.arc('BG.arc')
    idx = {}
    for nd in X.darc_files(d):
        c = X.clim_member(d, nd)
        if not c:
            continue
        base = os.path.basename(nd['path'])
        base = base[:-6] if base.endswith('.bclim') else base
        img, _ = X.decode_clim(c['pay'], c['fmt'], c['w'], c['h'])
        if img is not None:
            idx[base] = img
    out = []
    for nd in X.darc_files(d):
        if d[nd['off']:nd['off'] + 4] != b'CLYT':
            continue
        cw, ch, ps = X.clyt_panes(d, nd['off'])
        texs = X.clyt_textures(d, nd['off'])
        for gname, group in X.scenegroup(ps):
            if 'M_HV_BG_' not in gname:
                continue
            pairs = []
            for p in group:
                t = X.resolve_tex(p['name'], texs)
                key = t[:-6] if t and t.endswith('.bclim') else t
                if key in idx:
                    pairs.append((Image.fromarray(idx[key]), p))
            if pairs:
                out.append((gname, pairs))
    return out


def test_scene_compose_no_seam():
    st = _store()
    if st.arc('BG.arc') is None:
        pytest.skip('BG.arc \u4e0d\u5728')
    for gname, pairs in _bg_scene_pairs(st):
        img = X.compose(pairs)
        a = np.asarray(img.convert('RGB')).astype(int)
        assert a.shape[:2] == (320, 658)
        bad = [x for x in range(1, a.shape[1] - 1)
               if abs(a[:, x] - a[:, x - 1]).mean() > 60]
        assert not bad, '\u53d1\u73b0\u7ad6\u7f1d %s' % bad


def test_texi_decode_roundtrip():
    st = _store()
    hit = st.texi_find('t999_001a')
    if not hit:
        pytest.skip('t999_001a \u4e0d\u5728')
    t, x = hit
    d = X.texi_payload(t, x)
    assert d is not None and len(d) == 786432
    i = t['info']
    img = X.texi_decode(d, i['w'], i['h'], i['format'])
    assert img is not None and img.shape == (512, 512, 4)
    assert len(np.unique(img[:, :, :3].reshape(-1, 3), axis=0)) > 500


def test_inventory_builder_offsets():
    """\u81ea\u5efa\u7d22\u5f15\u7684\u504f\u79fb\u5fc5\u987b\u548c\u5df2\u77e5\u6b63\u786e\u503c\u4e00\u81f4\u3002"""
    st = _store()
    try:
        inv = X.build_inventory(st.img)
    except Exception as e:
        pytest.skip('scan \u5931\u8d25: %s' % e)
    rec = None
    for r in inv:
        if r['name'] == 't999_001a.texi' and r['sig'] == 'TEX':
            rec = r
            break
    if rec is None:
        pytest.skip('t999_001a \u4e0d\u5728')
    assert rec['cl'] == 369959
    assert rec['dl'] == 786432
    assert sum(1 for r in inv if r['sig'] == 'TEXI') > 9000


# ============================================================ \u6ca1\u88c5 pytest \u65f6\u7684\u8dd1\u5668
def _run_standalone():
    import traceback
    ns = dict(globals())
    tests = [(k, v) for k, v in sorted(ns.items())
             if k.startswith('test_') and callable(v)]
    ok = fail = skip = 0
    for name, fn in tests:
        try:
            fn()
            print('  PASS  %s' % name)
            ok += 1
        except Exception as e:
            if not _HAVE_PYTEST and e.__class__.__name__ == '_Skip':
                print('  SKIP  %-44s %s' % (name, e))
                skip += 1
                continue
            print('  FAIL  %s' % name)
            traceback.print_exc()
            fail += 1
    print('')
    print('%d \u901a\u8fc7  %d \u5931\u8d25  %d \u8df3\u8fc7  (\u5171 %d)'
          % (ok, fail, skip, len(tests)))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(_run_standalone())
