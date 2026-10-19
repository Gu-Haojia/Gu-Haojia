# 羽那 Coding 立绘与主页动效

项目：`/Users/guhaojia/Desktop/homepage`。日期：2026-10-19。

## 最终采用的立绘

采用用户选定的第一张职场穿搭版（浅灰紫西装、米白内搭、炭灰高腰裙），在这一版上做保守的头发纹理清理。后续从官方原图重生成的两张方案未接入页面。

这是参考官方形象的 AI 二创，并非官方游戏立绘。生成方式为内置 **image_gen**，先生成 Coding 姿势，再编辑职场服装；本次以用户选中的职场版为编辑目标，减轻头发上重复的液体状高光与波纹，保留相近的面部、视线、穿搭和构图。生成式清理不能保证其他像素完全不变，旧版已保留备份。

保存位置：

- 原始透明 PNG：`/Users/guhaojia/Desktop/homepage/assets/illustrations/hana-coding.png`
- 页面使用的无损 WebP：`/Users/guhaojia/Desktop/homepage/assets/illustrations/hana-coding.webp`
- 清理前备份：`/Users/guhaojia/Desktop/homepage/assets/illustrations/hana-coding-original.png` 与同名 `.webp`
- 页面：`/Users/guhaojia/Desktop/homepage/assets/shinycolors.svg`
- 构建代码：`/Users/guhaojia/Desktop/homepage/build.py`

PNG 与 WebP 的 RGBA 像素逐字节一致，均为 1024×1536，透明通道保留。人物在 1136px 逻辑画布内宽 430px，嵌入 SVG 后不依赖外部图片地址。

### 官方参考

- [enza 羽那官方角色页](https://shinycolors.idolmaster-official.jp/idol/cometik/hana/)
- [官方日常服立绘](https://shinycolors.idolmaster-official.jp/assets/img/idol/cometik/hana/idol_main_1_pc.png)：人物发型、面部及线条参考。
- [官方【優You】卡面](https://shinycolors.idolmaster-official.jp/assets/img/idol/cometik/hana/card/card_1.png)：面部、色彩及画风参考。

角色与原始游戏素材归原权利人所有；新增图用于此个人主页同人展示。

### 初次生成提示词

```text
Use case: illustration-story. Asset type: transparent game character sprite for compositing into the original enza THE IDOLM@STER SHINY COLORS 283 office Produce UI. Reference image 1 is the official Hana Suzuki 鈴木羽那 everyday-outfit sprite: identity, face, eye design, hair color, proportions, clothing and line/cel-shading style reference ONLY. Reference image 2 is official Hana artwork as a secondary face/style reference. Create ONE new illustration of Hana Suzuki coding on a laptop, rendered as if it were an original Shiny Colors enza dialogue standing sprite. Preserve recognizable Hana: long pale periwinkle/lavender-blue hair, layered side locks and fine parted bangs, large soft lavender-gray eyes with subtle mint highlights, fine dark plum lashes, warm friendly small smile, slender natural anime proportions. Reproduce the outfit in reference 1: white cable-knit sleeveless V-neck sweater layered over a muted lavender long-sleeve high-neck blouse with tiny scalloped collar/cuffs, a white pleated skirt. Pose: upright behind an invisible desk, gently leaning forward, facing viewer at a subtle three-quarter angle; both relaxed hands naturally touching the keyboard and trackpad of an open thin silver-lavender laptop at waist level, gaze slightly lowered toward the screen while face remains fully visible. Laptop rests on the invisible desk, not held in midair. The viewer sees its softly angled back and a small part of keyboard; no text, no logo, no labels. Full head through knees composition, entire head/hair/arms/laptop inside canvas, modest transparent padding. Character occupies most of portrait canvas. Laptop bottom at about 75 percent of image height, thighs continue below; intended later occlusion by an existing foreground desk. Style is extremely close to official 2D enza sprite: crisp thin organic outline, two or three delicate flat cel-shading tones, restrained blush, sparse controlled hair highlights, no painterly rendering, no photorealism, no 3D. Transparent alpha background, clean anti-aliased cutout edges. Include only Hana and laptop. Do not draw any table, chair, room, background, floor, halo, border, UI, sparkles, shadow rectangle, caption or watermark. Do not copy the pose from reference 2. No chibi, no giant eyes or giant head, no extra fingers. High-resolution portrait sprite, approximately 1024x1536.
```

### 最终选用的职场穿搭编辑提示词

编辑输入为初次生成的 Coding 立绘。

```text
Use case: precise-object-edit. Edit the attached transparent Hana Suzuki coding character sprite. Change ONLY her clothing to a tasteful slightly fashionable Japanese business-casual office outfit. A softly tailored pale greige/lavender-gray blazer worn open, sleeves casually pushed up just below elbows, an ivory simple high round-neck blouse underneath, and a high-waisted charcoal-gray A-line knee-length skirt with a slim dark belt and a small understated brushed silver buckle. Clean smart silhouette, a little relaxed and stylish, not a formal uniform. Keep the original Shiny Colors 2D cel-shaded thin-line sprite art style. Crucial invariants: exactly preserve Hana's face and expression, her pale periwinkle long hair and eyes, the current body proportions, same lean and pose, identical hands on keyboard and laptop shape/position, exactly the same framing and transparent canvas dimensions. Keep all limbs and laptop in their current positions so this is a drop-in replacement. Maintain clean fully transparent alpha around the sprite with no shadow halo or solid background. Do not change pose, hair, identity, laptop, crop or art style. Do not add text, logos, UI, jewelry, glasses, background, chair or desk.
```

### 本次头发清理提示词

使用内置 image_gen 编辑模式，输入为选定职场版，透明背景。输出复制到上述项目路径后，另做无损 WebP 格式转换，没有用 Python 修图。

```text
Use case: precise-object-edit.
Input image: exact edit target, the attached Hana Suzuki coding illustration with transparent background. This composition and this face are the user-selected version and must be retained.
Primary request: conservative texture cleanup, especially on her HAIR. Remove the unnatural small ripples, wavy watery streaks, blotchy repeated highlights and mottled AI texture from the pale blue/lavender hair. Replace just those artifacts with broad, smooth, coherent flat cel-shaded regions following the existing strand direction. Use a few clean continuous highlight shapes and clean solid shadow planes like a polished 2D visual-novel sprite. Preserve the original fine dark hair contour lines and strand boundaries. Do not smooth away the line art. Hair should remain the same pale lavender-blue hue with its existing overall light and shadow placement; no new detailed strands.
Strict invariants: same face, eye shapes and pupil positions, same direct gaze, same friendly open smile, exactly same head tilt, same hairstyle silhouette and bangs, same blazer/blouse/skirt and colors, same body proportions, hands, fingers, laptop, pose and framing. Do NOT redesign her, change her expression or shift her gaze. Do NOT simplify or change her facial features. Do NOT change pose or clothing. Avoid painterly, liquid or watercolor marks, hatching, noise, blurry surfaces and added texture.
Preserve all 1024x1536 canvas coordinates and the existing transparent alpha silhouette. Truly transparent background, no new halo, no background, no added props or text. Outside the hair, preserve the illustration as closely as possible; this is a small restoration edit, not a new character generation.
```

## 页面接入

- 移除培育页中央照片立牌。羽那位于桌面后方，电脑下沿与桌沿对齐，下半身由前景桌面遮挡。
- 休息气泡向左上微调，回顾气泡落到资料上方，避开电脑与手部。
- GitHub 用户头像仍在首页与制作人详情中作为制作人档案照片显示。

## 动效

| 层次 | 动效与节奏 |
| --- | --- |
| 操作提示 | 按钮、当前日期、图表端点统一 3.2 秒轻脉冲 |
| 气泡 | 4.2 秒、4.5px 小幅悬浮，错开相位 |
| 人物 | 4.6 秒、整张立绘上下平移 5px；人物比例保持不变，底部由前景桌面遮挡 |
| 环境 | 三缕淡蒸汽错相上升，少量四角光点缓慢闪烁 |
| 卡片与信息条 | 6.4 秒的低强度掠光；制作人详情卡面也有斜向反光，限于照片卡面内，卡片主体保持稳定 |
| 贡献图 | 完整底线、面积和数据点始终可见；上层强调线每 6.4 秒重播，3.2 秒描完整条线，再停留、淡出；光点同步跟随描线 |
| 对话与底部提示 | 初次逐行展开，之后完整保留，不再循环清空 |

这是单张立绘的轻微 SVG 变换，不是 Live2D，也没有生成眨眼或逐帧打字动画。

背景保留放大比例与慢移周期：首页 1.22 倍 / 48 秒，位移从 34×12px 微增至 44×16px；培育页 1.3 倍 / 44 秒，位移从 24×6px 微增至 32×8px。跑光边框、环绕光点和大片粒子已撤掉。

所有效果均写入自包含 SVG，README 仍只使用一个 img 标签，不需要网页脚本。最终 SVG 约 2.81 MiB。实际已验证本地浏览器的 img 嵌入渲染，已部署到 GitHub 个人主页并核对线上图片显示。

## 验证

- 使用现有 GitHub 数据缓存离线构建，未刷新贡献数字。
- 17 项测试通过：包括透视几何、SVG 自包含与时间轴、正文不循环清空、图表底线常驻，以及项目配置、元数据覆盖、自动扩行和无效配置保留旧页。另完成真实监听进程的配置变更与错误恢复验证。
- 浏览器以 1136px 原始画布及完整 README 预览核对布局。
- 两帧对比确认人物和蒸汽有变化、底部操作文字保持稳定。
- 已部署至 Gu-Haojia/Gu-Haojia，后续自动刷新配置见 DEPLOYMENT.md。

重新构建：`python build.py --offline`（需要 pillow、fonttools、brotli）。
测试：`python -m unittest discover -s tests -v`。

## 图表延迟滚动修正

原先图表只在图片加载后的 2.4 秒内描线，用户滚到页面下方时往往已经播放结束。现在把数据底图和动画强调线分开：底图始终完整，上层循环描线，不会把读到一半的数据擦掉。

浏览器验证先加载整张主页，经过首轮时间后再滚到图表；两帧对比确认描线继续变化，日期刻度和统计文字保持稳定。新增回归用例在修改前失败、修改后通过。

这仍然是自动循环，不是进入视口触发。README 采用一个 img 嵌入 SVG，SVG 图片中的 JavaScript 受到禁用限制，无法在图片内部监听外层页面滚动；参见 [MDN 的 SVG 图片限制](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image#restrictions)。
