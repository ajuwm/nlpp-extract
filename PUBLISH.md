# 发布到 GitHub 的改造计划

## 现状：现在的工具是「在已解密 ROM 上再解图」

```
原版 CIA / 3DS ──解密──> kirin-nlppj-dec.3ds ──抽 romfs──> img.bin
                                                              │
                                                 tex_inventory.json（贴图索引）
                                                              │
                                                      nlpp_extract.py ──> PNG
```

三个输入用户都没有：**解密的 ROM、img.bin、tex_inventory.json**。
所以现在这个状态**不能直接发**。

---

## 改造目标：让工具吃「原版 CIA / 3DS」也能跑

### 第一步 ★ 自己扫出贴图索引（去掉 tex_inventory.json 依赖）

这是最大的依赖，也是**最该做的一步**。

`tex_inventory.json` 里的每条记录长这样：
```json
TEXI {"name":"t999_001a.texi","pack":160610176,"dO":88176,"dl":82,
      "info":{"w":512,"h":512,"format":11,"ow":384,"oh":512}}
TEX  {"name":"t999_001a.texi","pack":160610176,"dO":200639232,"dl":786432,
      "comp":true,"cO":93402928,"cl":369959}
```

做法：**在 ROM 里全盘扫 `TEXI` / `TEX ` 两个 magic**，
按 magic 附近的字段解出 name/尺寸/格式，再把同 pack 同名的 TEXI 与 TEX 配起来。

**参考**：`tools/nlpp_tools/kiwiz-nlpp-tools.../img/__init__.py`（26KB）已经能解 `img.bin` 的
TEXI 包，`Notes.md` 里记了 `img.bin` 的完整结构：

```
img.bin 按 0x800 字节块对齐
0x000-0x800          文件头（含 idx_table_entry_count @0x010, off_table_offset @0x014）
0x800                索引表
idx_table_addr + off_table_offset   偏移表（header: 0x000 zero, 0x004 count, 0x008 ?）
包内 header: Type / Count / ? / 表尾偏移 / 数据起始 / 解压后大小 / 压缩后大小 / ?
    'SAB '  -> cmp_len == dec_len, cmp_off == def_off, flags == 0
    'TEXI'  -> cmp_len == 0, cmp_off == 0, flags == 0
```

### 第二步 从解密的 ROM 里自己抽出 img.bin（去掉「手工抽包」依赖）

解密的 `.3ds` 是 NCSD，里面有 NCCH 分区，romfs 是 IVFC 三层。
自己实现不难（都是定长表 + 偏移），**约 200 行**。

或者更省事：调用仓库里已有的 `tools/ctr/3dstool.exe`。

### 第三步 处理密码学那一层（可选，但决定易用性）

```
解密后的 .3ds / .cia   -> 工具直接吃                    ★ 推荐路线
原版加密 .3ds / .cia   -> 需要 boot9.bin 或 aeskeydb.bin
                          用 pycryptodome 做 AES-CBC 解密（约 150 行）
                          CIA 还要先解 title key
```

**建议**：主线只支持「解密后的 ROM」，README 里写清楚用 GodMode9 导出；
把「吃原版 CIA」做成可选功能（装了 pycryptodome 且有 boot9.bin 时启用）。
不要随仓库分发 `ctrtool.exe` 之类的二进制，容易被认为侵权。

---

## 建议的最终 CLI

```
python nlpp_extract.py info                      显示找到了什么、缺什么
python nlpp_extract.py scan  <rom|cia>           扫出贴图索引（替代 tex_inventory.json）
python nlpp_extract.py romfs <rom> --out D       抽出 img.bin 等 romfs 文件
python nlpp_extract.py unpack <img.bin> --out D  解开 img.bin 的包
python nlpp_extract.py list / members / export / tex / clyt / scene / audit   （现有）
```

`info` 这条最有用：用户第一次跑就知道自己缺哪一步，而不是报一堆栈。

---

## 发布前还要补的东西

```
· LICENSE：本工具是解包器，不含游戏素材。README 要写明
  「需要你自己拥有游戏；请勿分发解出的素材」（素材版权属 KONAMI）
· requirements.txt：numpy, pillow（可选 pycryptodome）
· 测试：至少覆盖 5 条路径（剧情CG / 旅游背景 / ExCard印章 / 画廊UI / G场景剪影）
  已经手工验证过，整理成 pytest 更好
· 不要 include：tex_inventory.json（4MB，应由 scan 生成）、任何解出的 PNG
```

---

## 本工具相对已有开源工具（kiwiz-nlpp-tools）的增量价值

```
✓ ETC1A4 的 alpha 是【列优先 + 低半字节在前】—— 已有工具多半用行优先，脸会有锯齿
✓ darc 成员名要按【名字表签名 00 00 2E 00 00 00】定位 —— 否则名字全是后缀
✓ CLYT 场景合成：pane 中心锚点 + Y 轴向上 + 边线对齐整数 + 裁不缩
✓ CLAN 动画格式
✓ 单文件 CLI，不需要 ie/pe/darctool 那一串外部 exe
```
