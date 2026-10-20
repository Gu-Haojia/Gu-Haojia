# GitHub 部署与自动更新

- 个人主页：https://github.com/Gu-Haojia
- 主页仓库：https://github.com/Gu-Haojia/Gu-Haojia
- 工作流：https://github.com/Gu-Haojia/Gu-Haojia/actions/workflows/shiny-refresh.yml
- 原桌面工作目录已清理；部署与定时刷新独立运行于 GitHub。需要本地预览时可重新克隆仓库到自选目录。

## 定时任务

GitHub Actions 工作流 `✦ Shiny Refresh` 已启用，使用 GitHub 托管的 Ubuntu 运行器。计划每天北京时间 **00:00** 执行（UTC 16:00），实际启动时间可能受运行器排队影响，无需保持本机开机。

每次运行会安装固定版本依赖、运行 23 项测试、联网刷新公开 GitHub 数据、重新生成 SVG/README，并由 github-actions[bot] 提交回 main。抓取失败时任务会报错，保留上一版数据和页面，不会把旧缓存当作成功刷新。

工作流使用仓库自带的 GITHUB_TOKEN，不需要额外的个人令牌。任务串行执行，并在开始时获取默认分支最新版本，避免排队任务基于过时版本提交。

## 手动更新与日常维护

1. 修改 `projects.json` 的 `items` 管理项目页；首页最新项目独立读取默认分支的实际提交时间，并排除主页仓库；修改 `config.json` 管理其他文字、技能与背景。
2. 提交并推送到 main，相关配置、代码和素材变更会自动触发构建。
3. 临时刷新数据可在 Actions → ✦ Shiny Refresh → Run workflow 中运行，分支选择 main。
4. 失败时打开对应运行记录的 Build / Commit 步骤查看错误。

其他仓库的提交在下一次已有构建运行时刷新到首页，不额外触发本仓库。卡片展示项目、Star 和提交时间，近 7 天有提交时显示 NEW!!；不展示语言标记、摘要或短 SHA。README 图片 URL 包含内容哈希，构建产生新图时同步更新。

本地克隆后可用 `python build.py --offline --watch` 预览配置修改，或 `python build.py --strict-refresh` 执行一次联网刷新。详细配置字段见 CONFIGURATION.md。

部署形式是 GitHub 个人资料页的 README，图像和动画都在自包含 SVG 中，不依赖 GitHub Pages。
