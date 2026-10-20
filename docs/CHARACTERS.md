# 角色选择

个人主页当前使用 `"character": "hana_old"`，保留此前选定的旧版羽那。这里统一通过 `character` 选择，不使用 `illustration` 字段。

| 选择 | 行为 |
| --- | --- |
| `hana_old` | 旧版羽那，仅固定选择，不进入随机池 |
| `hana` | 新版羽那 |
| 其他角色 ID / 姓名 | 固定使用对应的新立绘 |
| `random` | 每次现有定时或手动构建，从 28 张新立绘中随机选择一位；可能重复 |

修改 `config.json` 的 `character` 字段即可。账号、个人介绍、技能和项目配置都独立保留。

也可使用 **Actions → ✦ Shiny Refresh → Run workflow → character** 下拉菜单。选择 `鈴木羽那（旧版）` 会保存为 `hana_old`；选择 `from-config` 会保留当前设置。定时仍是每天北京时间 00:00，没有增加触发器。

本地试用（使用当前账号缓存，不修改保存的配置）：

```sh
python build.py --list-characters
python build.py --offline --character hana_old
python build.py --offline --character madoka
python build.py --offline --character random
```

随机结果会内嵌到生成的 SVG，访问或刷新 GitHub 主页不会重新抽取；配置保持 `random`，供下次构建继续使用。

## 角色清单

| ID | 姓名 | 组合 | 参与 random |
| --- | --- | --- | --- |
| `mano` | 櫻木真乃 | illumination STARS | 是 |
| `hiori` | 風野灯織 | illumination STARS | 是 |
| `meguru` | 八宮めぐる | illumination STARS | 是 |
| `kogane` | 月岡恋鐘 | L’Antica | 是 |
| `kiriko` | 幽谷霧子 | L’Antica | 是 |
| `yuika` | 三峰結華 | L’Antica | 是 |
| `mamimi` | 田中摩美々 | L’Antica | 是 |
| `sakuya` | 白瀬咲耶 | L’Antica | 是 |
| `kaho` | 小宮果穂 | 放課後クライマックスガールズ | 是 |
| `chiyoko` | 園田智代子 | 放課後クライマックスガールズ | 是 |
| `juri` | 西城樹里 | 放課後クライマックスガールズ | 是 |
| `rinze` | 杜野凛世 | 放課後クライマックスガールズ | 是 |
| `natsuha` | 有栖川夏葉 | 放課後クライマックスガールズ | 是 |
| `chiyuki` | 桑山千雪 | ALSTROEMERIA | 是 |
| `amana` | 大崎甘奈 | ALSTROEMERIA | 是 |
| `tenka` | 大崎甜花 | ALSTROEMERIA | 是 |
| `asahi` | 芹沢あさひ | Straylight | 是 |
| `fuyuko` | 黛冬優子 | Straylight | 是 |
| `mei` | 和泉愛依 | Straylight | 是 |
| `toru` | 浅倉透 | noctchill | 是 |
| `madoka` | 樋口円香 | noctchill | 是 |
| `koito` | 福丸小糸 | noctchill | 是 |
| `hinana` | 市川雛菜 | noctchill | 是 |
| `nichika` | 七草にちか | SHHis | 是 |
| `mikoto` | 緋田美琴 | SHHis | 是 |
| `luca` | 斑鳩ルカ | CoMETIK | 是 |
| `hana` | 鈴木羽那 | CoMETIK | 是 |
| `haruki` | 郁田はるき | CoMETIK | 是 |
| `hana_old` | 鈴木羽那（旧版） | CoMETIK | 否 |

[28 张新立绘预览](https://github.com/Gu-Haojia/shinycolors-profile-template/blob/main/docs/CHARACTERS.md) · [生成提示词与参考](character-prompts.json)
