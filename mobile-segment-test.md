# 手机分段渲染测试

[打开同一份数据的原版长图对照](https://github.com/Gu-Haojia/Gu-Haojia/blob/650b5b923f19ef8c3d56f701f70160e238d4af28/README.md)

此页把原图拆成 7 张独立 SVG，保留底纹、文字、人物及动画参数。请用同一个手机浏览器分别停留首页、培育、任务，再上下滚动比较流畅度、发热和拼接处。测试快照：2026-10-21；本页不会每日更新。

版本 v2：修正 Safari 分段边缘对齐，图片使用新文件名以避开旧缓存。

<p align="center"><img src="assets/mobile-segment-test/01-home-v2.svg" width="100%" align="top" alt="首页"/><img src="assets/mobile-segment-test/02-projects-v2.svg" width="100%" align="top" alt="项目"/><img src="assets/mobile-segment-test/03-produce-v2.svg" width="100%" align="top" alt="培育"/><img src="assets/mobile-segment-test/04-producer-v2.svg" width="100%" align="top" alt="制作人详情"/><img src="assets/mobile-segment-test/05-missions-v2.svg" width="100%" align="top" alt="任务"/><img src="assets/mobile-segment-test/06-about-v2.svg" width="100%" align="top" alt="关于"/><img src="assets/mobile-segment-test/07-footer-v2.svg" width="100%" align="top" alt="页脚"/></p>

测试页独立于正式主页。数据与画面来源：`650b5b9`；复现脚本：[`tools/build_segment_test.py`](tools/build_segment_test.py)。
