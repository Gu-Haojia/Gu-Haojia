# 项目配置与自动生成

实际编辑目录：`/Users/guhaojia/Desktop/homepage`。此文件的 outputs 副本仅供查阅，修改项目里的配置才会生效。

## 日常只需改 projects.json

`config.json` 中的 `"projects_file": "projects.json"` 指向项目清单。首页推荐和项目页共用该清单，不必修改 Python 或 SVG。

```json
{
  "home_recommendation": "Ai_Agent",
  "items": [
    {
      "repo": "Ai_Agent",
      "title": "Ai_Agent",
      "description": null,
      "language": null,
      "color": "blue",
      "show_on_projects": true
    },
    {
      "repo": "RepArchive",
      "title": "资源归档工具",
      "description": "这里也可以自己写一句介绍",
      "color": "pink",
      "show_on_projects": true
    }
  ]
}
```

| 字段 | 用法 |
| --- | --- |
| home_recommendation | 首页推荐的仓库名，必须与 items 中的 repo 一致；null 隐藏推荐 |
| repo | 仓库名，按 config.json 的 GitHub 用户获取数据；不可重复 |
| title | 展示名，省略、空字符串或 null 使用 repo |
| description / language | 省略或 null 自动读取 GitHub；文字可覆盖，空字符串可留空 |
| color | blue / pink / orange / yellow；省略则依次配色 |
| show_on_projects | 是否显示在项目页，默认 true |

项目页按 items 顺序排列，每行两项；超过四项会自动增加行数和画布高度。首页推荐独立于排列顺序，也可以推荐 show_on_projects 为 false 的项目。

Star、推送时间自动来自 GitHub 数据；缓存中不存在的仓库显示未知值，不会伪造零星数。当前数据抓取范围是该用户的公开非 fork 仓库。培育页“正在培育”继续表示最近推送的仓库，与手动首页推荐分开。

## 本地自动生成

在项目目录执行（Python 依赖：pillow、fonttools、brotli）：

```sh
python build.py --offline --watch
```

保存 config.json、projects.json 或更新页面使用的 hana-coding.webp 后，约一秒内自动重新生成 assets/shinycolors.svg、README.md 和 preview.html。浏览器刷新即可看到新结果。Ctrl+C 结束监听。

- `python build.py --offline`：只构建一次，使用已有 GitHub 缓存。
- `python build.py`：联网刷新 GitHub 数据并构建。
- JSON 暂时不完整或配置值错误时保留上一版页面，修正保存后继续生成。
- 修改 build.py 后，需要重启监听进程。

已部署到公开仓库 Gu-Haojia/Gu-Haojia。GitHub Actions 工作流已接入 projects.json：main 分支相关文件变更、每日北京时间 00:00 及手动运行均可触发构建。更换配置文件名时，也需修改工作流 push.paths。部署与运行方式见 DEPLOYMENT.md。

## 动效与立绘

按最后反馈小幅加强呼吸和场景移动，卡片与正文保持稳定：

- 人物呼吸：4.6 秒一轮，整张立绘上下平移 5px，保持人物比例，底部由前景桌面遮挡。
- 气泡、提示浮动：4.2 秒一轮，最大 4.5px。
- 首页场景：1.22 倍，48 秒一轮，最大移动 44×16px。
- 培育场景：1.3 倍，44 秒一轮，最大移动 32×8px。
- 保留轻微蒸汽、闪光和按钮呼吸。图表完整底线常驻，上层强调线每 6.4 秒重播。

羽那采用用户选中的职场版，经内置 image_gen 清理发丝波纹；旧版保存在 assets/illustrations/hana-coding-original.png 与 .webp。清理版与完整编辑提示词见同目录 ARTWORK_AND_MOTION.md。

## 验证

17 项测试覆盖配置、自动扩行、透视、SVG 自包含、动画时间轴、正文与图表可读性，以及定时刷新失败时的缓存保护。独立目录内实际运行监听，验证“更换首页推荐 → 自动重建 → 无效 JSON 保留旧页 → 修正后恢复”。
