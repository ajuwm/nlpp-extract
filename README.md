# NLPP 插画提取工具

New Love Plus+（3DS）插画 / 贴图提取工具。把几轮逆向得出的正确解码规则封成一套可复用的命令行工具。

## 安装依赖

```
pip install numpy pillow
```

## 配置

工具会自动找 `img.bin`（以及可选的解密 ROM）。找不到就设环境变量：

```
set NLPP_IMG=D:\path\to\img.bin
set NLPP_ROM=E:\path\to\kirin-nlppj-dec.3ds
```

`tex_inventory.json` 可选 —— **不提供也行**，先跑一次 `scan` 自己生成，
默认写到工具的上一级目录。

## 文件结构

```
nlpp_extract.py        主工具（CLI + 全部解码逻辑）
etc1.py                ETC1/ETC1A4 块解码
nlp_pack.py            img.bin 的包索引读取
rom.py                 解密 ROM 懒加载读取
test_nlpp_extract.py   测试，14 项
requirements.txt       numpy, pillow
LICENSE                MIT（只覆盖代码，不含游戏素材）
PUBLISH.md             发布改造笔记
```

## 用法

```
python nlpp_extract.py scan    [--img 路径] [--out 路径]  ★ 自己扫出贴图索引
python nlpp_extract.py list [正则]              列出归档（1433 个）
python nlpp_extract.py members <归档>           列出成员：路径 / 大小 / 格式 / 存储尺寸
python nlpp_extract.py export  <归档> [--out D] 导出归档内全部图像
python nlpp_extract.py tex     <名字> [--out D] 导出 TEXI 贴图（如 t999_001a）
python nlpp_extract.py clyt    <归档>           显示布局：纹理表 + 每个 pane 的坐标
python nlpp_extract.py scene   <归档> [--out D] 按布局合成场景（自动分互斥变体）
python nlpp_extract.py audit   [--out D]        全库盘点：按 归属×类型 分类导出 + manifest.tsv
```

**★ `scan` 让它自己生成索引**，不再依赖预先做好的 `tex_inventory.json`：

```
python nlpp_extract.py scan --out tex_inventory.json
# TEXI 9593  TEX 9593  合计 19186
```

索引里每条记录带 `src` 字段（数据源文件路径），所以**扫解密 ROM 还是扫 img.bin 都能用**，
只要读的时候读同一个文件。

例子：

```
python nlpp_extract.py scan --out tex_inventory.json    先建索引
python nlpp_extract.py list "^HV_"                       列出 60 个 HV 归档
python nlpp_extract.py members HV_BG.arc                 婚礼那 14 层
python nlpp_extract.py scene HV_BG.arc --out out\婚礼     合成为 1024x512
python nlpp_extract.py clyt BG.arc                       温泉的 16 个 pane
python nlpp_extract.py tex nlpp_pub_m0000 --out out       公募插画
```

## 快速上手：从 img.bin 到 PNG

假设你已经用 `3dstool` 把 romfs 抽出来了，拿到了 `img.bin`。

### 第 0 步 装依赖

```
pip install -r requirements.txt
```

### 第 1 步 告诉工具 img.bin 在哪

```
set NLPP_IMG=D:\games\nlpp\img.bin
```

（或者每次加 `--img 路径`。Linux/macOS 用 `export NLPP_IMG=...`）

### 第 2 步 建索引（3 秒）

```
python nlpp_extract.py scan --out tex_inventory.json
# TEXI 9593  TEX 9593  合计 19186
```

**这一步只跑一次。** 索引是 TEXI 贴图的名字/尺寸/格式表，
`tex` 命令靠它才知道"`t999_001a` 有多大、什么格式、数据在哪"。
不建也能用 `list` / `export` / `scene`（那些走归档，不走 TEXI）。

### 第 3 步 先看有什么，别急着导

```
python nlpp_extract.py list                    # 1433 个归档，全部列出来
python nlpp_extract.py list "^HV_"             # 按正则筛
python nlpp_extract.py members HV_BG.arc       # 看某个归档里有什么（尺寸/格式都会标）
```

`members` 会把「声明尺寸 → 实际存储尺寸」都打出来，比如：

```
./anim/blyt/timg/M_HV_Eye10.bclim   16424  ETC1A4  106x92 -> 128x128 (padded)
```

`106x92` 是真实精灵尺寸，`128x128` 是 2 的幂次填充 —— **带 `(padded)` 的都要按声明尺寸裁**。

### 第 4 步 按你要的东西选命令

| 想要什么 | 命令 |
|---|---|
| 单张剧情 CG / 立绘 | `tex <名字> --out out\cg` |
| 一个归档里的全部图 | `export <归档> --out out\xxx` |
| 场景合成图（多层） | 先 `clyt <归档>` 看布局，再 `scene <归档> --out out\xxx` |
| 全库，按类别分好 | `audit --out out\全部` |

### 第 5 步 出图在哪

```
out\
  t999_001a_512x512.png          透明底
  t999_001a_512x512_white.png    白底（方便直接看）
```

`scene` 会为每个互斥变体各出一张，文件名带层名，例如
`BG__M_HV_BG_658x320.png`。

---

## 找图指南：我要的东西叫什么

| 想找 | 正则 / 归档名 | 说明 |
|---|---|---|
| 剧情 CG / 立绘 | `^t` `^a` `^k` | TEXI 贴图，用 `tex` 导 |
| 公募 / 特殊 CG | `^nlpp_pub` `^big_` `^etc_` | 同上 |
| 人物分层（脸/身体/服装） | `^HV_` | 60 个归档，用 `export` |
| 梦境剪影 | `^G_M_` `^G_N_` `^G_R_` | 爱花11 / 宁宁6 / 凛子8 场 |
| 脸部部件 | `Eye.arc` `Mouth.arc` | 106×92 脸补丁、30×24 嘴 |
| 旅游地点背景 | `^stm_` `^stn_` `^str_` `^bs_` | TEXI |
| 印章 / 卡片 | `^ExCard` | 1000+ 个归档 |
| 画廊预览缩略图 | `^Gallery_` | TEXI |
| 角色（简写） | `M_`=爱花 `N_`=宁宁 `R_`=凛子 | 所有命名都这个规则 |

**递归探索的姿势**：

```
python nlpp_extract.py list "^G_"          # 有哪些
python nlpp_extract.py members G_M_00.arc  # 里面是什么
python nlpp_extract.py export  G_M_00.arc --out out\dream00
```

## 数据来源（发布前必读）

现在的工具需要**解密后的数据**，两种输入都行：

| 输入 | 说明 |
|---|---|
| 解密后的 `.3ds` / `.cia` | 用 GodMode9 从你自己的机器上导出 |
| `img.bin`（从 romfs 抽出） | 自己用下面的工具抽，或用 `NLPP_IMG` 指向它 |
| `tex_inventory.json` | **不需要了**，`scan` 自己建 |

### 怎么拿到解密后的数据？自己动手，用这些工具

本工具**不做**解密、解包、CIA 转换 —— 那部分交给成熟工具，这里只给友情链接：

- **[3dstool](https://github.com/dnasdw/3dstool)** —— 3DS 镜像解包/重打包，抽 romfs 用它
  ```
  3dstool -x -t cxi -f game.cxi --romfs romfs.bin      # 或按你的格式
  ```
- **[ctrtool](https://github.com/3DSGuy/Project_CTR)** —— CIA/NCCH 解析与解密
- **[GodMode9](https://github.com/d0k3/GodMode9)** —— 在真机上导出解密后的 romfs（最省事）
- **[3dsconv](https://github.com/ihaveamac/3dsconv)** —— CIA → 可解密的格式
- **[Ohana3DS Rebirth](https://github.com/gdkchan/Ohana3DS-Rebirth)** —— 3DS 模型/贴图查看

**注意**：解密需要你自己机器的密钥（`boot9.bin` 等），本仓库不提供、也不提供任何游戏文件。

### 数据流向

```
原版卡带 / CIA
      │  GodMode9 或 3dstool + ctrtool   ← 用上面的工具，不是本工具
      ▼
解密后的 romfs
      │  3dstool -x
      ▼
img.bin  ──┐
           │   python nlpp_extract.py scan --out tex_inventory.json
           ▼
    nlpp_extract.py list / export / tex / clyt / scene / audit
           ▼
         PNG
```

### 工具自检

```
python test_nlpp_extract.py        # 没装 pytest 也能跑
pytest -q                          # 装了 pytest 的话
# 14 通过  0 失败
```



## 文件

```
nlpp_extract.py        主工具（CLI + 全部解码逻辑）
etc1.py                ETC1/ETC1A4 块解码（只用 _etc1_decoded_block / _etc1_scramble）
nlp_pack.py            img.bin 的包索引读取
rom.py                 解密 ROM 的懒加载读取
test_nlpp_extract.py   测试，14 项
requirements.txt       numpy, pillow
LICENSE                MIT（只覆盖代码）+ 不含游戏素材的声明
PUBLISH.md             发布改造笔记
```

## ★ 八条解码规则（都验证过，改之前先看理由）

| # | 规则 | 不这么做会怎样 |
|---|---|---|
| 1 | **darc 名字表**：`T = 节点表起点 + 节点数×12`，T 处 6 字节固定 `00 00 2E 00 00 00`（根 `""` + 目录 `"."`）。节点名偏移相对 T | 在 `toff+tsize` 附近猜基准，拿到的是真名的**后缀**（`anaka01.bclim` 其实是 `M_HV_Manaka01.bclim`） |
| 2 | **名字是 UTF-16LE**，找终止符要按 **2 字节步进** | 用 `find(b'\x00\x00')` 会在奇数字节命中半个字符，名字被截断或为空 |
| 3 | **CLIM 头部在文件块的【最后 0x28 字节】**，像素在前面 | 读头部之后的字节，那里没数据 |
| 4 | **尺寸**：声明尺寸能整除载荷长度就用声明尺寸，否则用 2 的幂次填充盒子 | ExCard 声明 400×400 实存 512×512 |
| 5 | **ETC1A4**：16 字节/块 = 前 8 字节 alpha + 后 8 字节 ETC1 颜色，8×8 瓦片装 4 个 4×4 块 | 颜色和 alpha 对调 → 满屏噪点 |
| 6 | **alpha 映射是【列优先 + 低半字节在前】**：`byte j → 列 j//2，行 (j%2)*2 和 +1` | 行优先会让脸部贴图边缘出**阶梯状锯齿**（用"锯齿量"实测：colLH 7.63 vs rowHL 18.33） |
| 7 | **TEXI 数据在配对的 TEX 记录里**（TEXI 只是头），且要按 `(name, pack)` 配对；格式号走 `.texi` 表（10=rgba8 11=rgb8 12=etc1 13=etc1a4） | 读 TEXI 记录拿到的是头部；不按 pack 配对会张冠李戴 |
| 8 | **CLYT**：节的 `size` 字段**含 8 字节段头**，步进是 `p += size`；pane 的 `(x,y)` 是**中心**，**Y 轴向上**；贴图比 pane 大时**裁**不是**缩**；边线要先对齐到同一批整数 | 步进多加 8 → 只走完一半的节；Y 轴搞反 → 图层散开；边线各自取整 → 留 1 像素黑缝 |

## 已知限制

- `texi_decode` 目前只实现了主流的几种格式（10/11/12/13/9）。`la8`(4)、`rgb565`(7)、`rgba5551`(8) 等还没接，遇到会返回 `None`。
- 不支持 `.bclan` 动画、`.bclyt` 的旋转/缩放字段（实测这两个字段在 HV 场景里都是默认值）。
- `.mdl/.smat/.smes/.bone/.mot` 3D 模型那条线不在本工具范围内。
- **梦境（`G_` 归档）目前只导出了剪影层。** 每场梦境确认有的是
  一张 512×256 的剪影贴图 + 1~2 帧的 `.bclan` 淡入淡出动画 + 一个 `.bclyt` 布局。
  我们**还没找到**其它彩色图层或背景图存在哪里 —— 但这不代表它不存在，
  更可能是我们没定位到。已知**预切好的**多层场景栈只有 4 个
  （愛花婚礼 `HV_BG.arc`、愛花温泉 `BG.arc`、凛子房间 `HV_BG01/02.arc`），
  其余场景的图层来源**待查**。欢迎有线索的人开 issue。

- **动作（`.mot`）的骨骼语义未解决。** 这条属于 3D 模型那条线，不影响本工具的插图导出，
  但一并记在这里：`.mot` 的容器、记录、通道掩码、插值、记录→骨骼表
  （值 = 骨骼号 + 225×bank）都已用 `code.bin` 反汇编确证，能读能出画面，
  **但姿势不对** —— 套上动作后角色悬空、双腿蜷曲、手臂僵在 T-pose。
  卡住的是最后一层语义：手臂网格绑定骨骼 191~224，而绝大多数动作只驱动 12~43，两段几乎不重合；
  `m_lowerNNN` / `m_skirt_NNN` 驱动的其实是**头发骨骼 78~96** 而不是下半身；
  动作 ↔ 分层变体的配对规则在 `code.bin`（`.mot` 字符串命中 0）和 577 个 `.dbin2` 里都找不到明文。
  模型 / 骨骼 / 材质 / 贴图 / 渲染这条链已验证正确，**只有动作姿势没对上**。
