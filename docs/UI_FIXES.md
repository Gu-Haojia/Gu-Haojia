# 主页 UI 修正与素材清晰度记录

项目：`/Users/guhaojia/Desktop/homepage`。修正日期：2026-10-19。

后续更新：培育页中央照片立牌已替换为用户选定的羽那 Coding 职场版，动效也已统一；当前状态见 [ARTWORK_AND_MOTION.md](ARTWORK_AND_MOTION.md)。以下为该次基础修正记录。

## 本次修正

- 首页档案头像框与语言胶囊之间保留 16 个 SVG 逻辑像素，卡片内部统计区随之下移。
- 培育页“正在培育”信息条按右侧 18px 边距对齐。
- 休息、回顾各自的“近30天”和数值合并进同一个气泡，去掉零散说明；四个操作标题统一基线。
- 平板外壳和三个排行条改为矢量；字形、数字、颜色条共用同一个单应透视变换。
- 培育页使用桌面照片立牌，制作人详情使用完整档案照片；移除圆形羽化大头像。
- 气泡、操作标题、首页 Produce/任务按钮、页标题、等级条、黄色统计行矢量化。

## 背景增强

原图保留在 `assets/game/bg_001.webp` 和 `bg_003.webp`。首页的 **1.22 倍**放大及 48 秒移动、培育页的 **1.3 倍**放大及 44 秒移动保持原样。

增强版路径：

- `/Users/guhaojia/Desktop/homepage/assets/game/bg_001_hd.webp`：1671×941。
- `/Users/guhaojia/Desktop/homepage/assets/game/bg_003_hd.webp`：1672×941。

使用内置 **image_gen**，分别以对应原图为编辑输入进行清晰度增强，然后编码为质量 96 的 WebP。它们是 AI 增强版本，**不是新找到的官方高清原图**；细小纹理和标识可能存在重建差异。生成 PNG 留存于本次会话的 generated_images 目录。生成提示要求更高像素，但以上尺寸是实际收到并检查的输出尺寸。

### 使用的提示词（两张图相同，各自绑定对应原图）

```text
Use case: precise-object-edit. Asset type: high-resolution background asset for an enza Shiny Colors themed GitHub profile. Input image is the EXACT edit target, a 1136x640 original anime visual-novel office background. Perform strictly conservative resolution and clarity enhancement of this image. Output at least 2272x1280, preferably 3408x1920, preserving its 71:40 aspect ratio. Preserve the exact camera, crop, perspective, geometry, every piece of furniture, shelving, TV, cushions, desk, rug, plants, window, wall and floor. Preserve identical time of day, brightness, color palette, linework and flat hand-painted anime game style. Preserve all logos, window numbers and tiny signage as in the original. Reconstruct only blurred or blocky edge pixels and JPEG/WebP artifacts into clean, sharp, antialiased contours and restrained painted surface details. No new objects, no removal, no spatial shift, no redesign, no realistic textures, no photographic rendering, no bloom, no oversharpening halos, no characters, no UI overlay. This must look like the exact source game background delivered at higher resolution, not a new version of the scene.
```

## 原生界面参考与提取

- [汉化项目原生培育图集](https://github.com/ShinyGroup/SCTranslationData/blob/master/data/image/produce_top_parts.png)：核对四个桌面操作的轮廓、标题和排行风格。
- [游戏内 Produce 说明图](https://github.com/ShinyGroup/SCTranslationData/blob/master/data/image/tips/produce/produce/001.jpg)：核对培育主界面的道具布局。
- [原生界面介绍](https://dengekionline.com/elem/000/001/697/1697383/)：核对右上信息区与桌面功能分区。

新增 `assets/game/papers_plain.webp` 来自汉化图集坐标 `(783,543)-(1080,636)`，尺寸 297×93，无损提取。使用没有内嵌低分辨率“回顾”文字的资料图，再叠加矢量标题。游戏素材版权归 Bandai Namco Entertainment Inc.。

## 头像与保留的位图

GitHub 返回的头像原图只有 300×300。已去掉“放大为 600×600 再压缩”的处理，缓存使用原始图像字节。培育页头像显示为 192×192，详情页为 178×178；没有用生成式重画替换用户头像。

台历、杯子、资料、叶月、金币等保留原生素材，按原尺寸或缩小显示。背景图像、角色与道具仍为位图，不能声称所有元素均为无限分辨率。细线框、标题、数字和操作控件已尽量改为 SVG。

## 验证

- 使用现有 GitHub 数据缓存离线构建，未刷新贡献数字。
- 4 项测试：屏幕四角、直线保持性、退化几何拒绝、整张 SVG 的 ID/引用/自包含验证。
- 浏览器核对原始 1136px 画布与 README 预览，检查浅色及深色外框。
- 所有修改保存在本地项目；未推送或部署到 GitHub。

