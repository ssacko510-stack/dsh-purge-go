<p align="center">
  <img src="docs/banner.svg" alt="dsh-purge" width="720">
</p>

<h1 align="center">⚔️ dsh-purge — DSH Go 适配线</h1>

<p align="center"><strong>版本 1.1.71-g17 · DSH Go 1.1.0（内置 dsh 0.2.2-rc.1）</strong></p>

<p align="center">
  <em>DeepSeek Harness 破甲，面向 DSH Go 客户端：导入即生效，宿主回忆段原样透传，CLI --apply 自动写戳。</em>
</p>

<p align="center">
  <a href="https://github.com/ssacko510-stack/dsh-purge-go/stargazers"><img src="https://img.shields.io/github/stars/ssacko510-stack/dsh-purge-go?logo=github&label=Stars" alt="GitHub stars"></a>
  <a href="https://github.com/ssacko510-stack/dsh-purge-go/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-65a30d?style=flat" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/DSH%20Go-1.1.0-1a73e8" alt="DSH Go 1.1.0">
  <br>
  <img src="https://img.shields.io/badge/Node.js-%3E%3D22.13.0-339933?logo=node.js&logoColor=fff" alt="Node.js">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000" alt="JavaScript">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a>
</p>

> **两条线别混装。** 本仓库只做 **DSH Go 线** —— 给 DSH Go 客户端当插件导入的那份 tgz。**电脑桌面线**（dsh web / 官方桌面版，dsh 0.2.x，靠 app.asar 打引擎）在另一个仓库：[ssacko510-stack/dsh-purge-fork](https://github.com/ssacko510-stack/dsh-purge-fork)。两边共用同一张补丁表，只有宿主适配层不一样，别互相覆盖。
>
> **署名链路。** 原始作者（设计 / 提示词 / 技能）：[YuJunZhiXue/dsh-purge](https://github.com/YuJunZhiXue/dsh-purge) —— Apache-2.0，见 NOTICE。本线从社区 dsh 0.2.x 兼容构建 [realMisakaMikoto/dsh-purge](https://github.com/realMisakaMikoto/dsh-purge) 切出，再叠 DSH Go 宿主适配，逐条记在 [FORK-NOTES.md](FORK-NOTES.md) 与 [MAINTENANCE.md](MAINTENANCE.md)。

## 目录

- [赞助](#sponsor)
- [介绍](#介绍)
- [署名要求](#署名要求)
- [违规商用公示](#违规商用公示)
- [适配范围](#适配范围)
- [安装](#安装)
- [界面](#界面预览)
- [使用](#使用)
- [工作原理](#工作原理)
- [还原](#还原)
- [更新](#更新)

---

<a id="sponsor"></a>

## ☕ 赞助

这个项目要是帮到你了，欢迎打赏。我是讨口子，施舍点~


| 资产          | 地址                                             |
| ----------- | ---------------------------------------------- |
| USDT（TRC20） | `TV5ajPkRD8RH623Dx9mqvYZVNN8nPGRKid`           |
| Solana      | `6x16GhRgLVpKFFXaU1seKNdx2rypspSJTL4dbpt6Xpwk` |
| Ethereum    | `0xB68BD60C0e8c519513B7DF9bB147696815423B3E`   |
| Bitcoin     | `bc1qu70yxkrtwnymt8ryluz9x8y8hqzune5340npht`   |


---

## 介绍

**dsh-purge** 是装在本机 **DSH Go**（DeepSeek Harness 官方手机端）上的网络安全红队评测插件。本条线适配 **DSH Go 1.1.0 / 1.0.16 / 1.0.15**（内置 dsh `0.2.2-rc.1`）。

电脑桌面线——`dsh web` 与官方桌面 EXE——单独维护在 [`ssacko510-stack/dsh-purge-fork`](https://github.com/ssacko510-stack/dsh-purge-fork)。两条线共用同一张补丁表，宿主适配层不同。**只装一条**，别混装；对照表见 [`MAINTENANCE.md`](MAINTENANCE.md)。

Harness 不只是把问题交给模型。它还会在运行时改提示词、审批门、沙箱和会话格式。只看「模型答不答」，会把宿主拦截误当成模型拒绝。这个插件在你自己的安装里把这两层分开，用来做受控评测，也用来看默认策略该不该收紧。


| 你会用到             | 它做什么                                            |
| ---------------- | ----------------------------------------------- |
| **dsh-purge 侧栏** | 会话标题旁的按钮打开右侧栏。里面两页：清洗、演练台                       |
| **清洗**           | 分组查看补丁，应用、还原、卸载；编辑提示词和多套规则                      |
| **演练台**          | 正式版内置。授权后查看资产、技能和本机环境。只用于你有权管理的本机、离线靶标或已书面授权的演练 |
| **宿主策略**         | 调整默认文案、权限策略和工具上限。官方能力保留，不另写一套身份                 |
| **启动时**          | 自动再检查并应用。npm 升级盖掉 `node_modules` 之后不用手改文件       |


不写死路径。先看 `$DSH_HOME`，再看 DSH Go 主目录下的 `plugins/dsh-purge`，最后退回 `~/.dsh`。不碰 DSH Go 的二进制和签名包。在 **dsh-purge** 的「清洗」里点「应用」才写入。身份来自插件里的加密提示词，也就是提示词框默认显示的那一份。不读取宿主磁盘上的提示词文件；宿主自有的回忆段（`dsh-go:confirmed-memory`）逐字节原样透传。

本插件只处理使用者本机已安装的官方 `@deepseek-ai` 包和本机配置。它不是公网扫描器，也不是针对第三方站点的攻击套件。仓库内不含木马、未授权渗透脚本或对外攻击载荷。

---

## 📌 非盈利公益项目，严禁任何主体用于商业售卖、付费倒卖或黑灰产牟利，仅供技术参考。

## 署名要求

**借用本项目的名称、思路、代码或提示词，必须署名，并写明来源仓库：** [YuJunZhiXue/dsh-purge](https://github.com/YuJunZhiXue/dsh-purge)。

不署名、隐瞒来源、改头换面据为己有，作者将依法追究责任。

---

## 违规商用公示

抖音直播账号 **「老张的ai」**（直播间显示 **「老张AI讲堂」**）把本仓库当收费货卖：直播间问价、当场收钱，不署名，也不守上面的非盈利条款。作者人就在场，对方照收。

本项目免费、非盈利。拿它卖课、卖插件、卖 token、倒卖，许可当场作废，作者保留追究权利。

2026-10-12 直播记录：

<p align="center">
  <img src="docs/notice/laozhang-live-1.jpg" width="360" alt="老张的ai 直播问价">
  <img src="docs/notice/laozhang-live-2.jpg" width="360" alt="老张的ai 直播收钱">
</p>

对方微信名 **「老张的ai科技」**，直播间观众榜同号。被问到是不是本仓库开发者时，自称「老厉害了」；作者当场表示要投诉。

<p align="center">
  <img src="docs/notice/laozhang-wechat-1.jpg" width="420" alt="老张的ai科技 微信自称开发者">
</p>

---

### ⚠️ 严正法律免责与合规使用声明



**免责声明：** 本项目为非营利开源项目，遵守国家法律法规及所在平台的相关规范，仅供学习与研究使用。不得将本项目用于任何违法违规用途；由此产生的后果由使用者自行承担。

**【零容忍严正申明】**：本项目坚决反对并严禁任何形式的违法犯罪行为！本项目开发者绝不支持、不鼓励、不协助任何未授权网络攻击、漏洞利用、数据窃取、非法侵入计算机信息系统或生成违法违禁内容的活动。**任何将本项目用于违法犯罪的行为，均与开发者无关，由行为人依法独立承担全部法律责任。**

1. **本仓库不含违法内容**：`dsh-purge` 发布的代码、文档、补丁与默认提示词**不是**木马、后门、未授权渗透工具、勒索软件、撞库脚本，也**不是**针对公网或第三方系统的攻击载荷。项目本身不提供违法内容，也不教唆、组织、协助实施违法犯罪。
2. **只作用于本机官方 Harness**：安全评测补丁、提示词注入全部发生在使用者**本机已安装的官方 DeepSeek Harness**（`@deepseek-ai` 包、本机 profile / `$DSH_HOME`）上。对象是使用者自己的官方本地软件，**不是**他人的网站、服务器、账号或信息系统。
3. **评测补丁不对外网目标联网**：应用补丁、写入注入、回滚、卸载均在本机文件与本机进程内完成，**不对任何公网主机、未授权系统进行扫描、探测、入侵或攻击发包**。不得把本项目当作跳板去打外网。插件若开启「检测更新」，仅可能访问本插件自己的 GitHub 仓库以核对版本，**与对第三方系统的网络攻击无关**，也不能被解释为授权对外渗透。
4. **合法受控范围限定**：本项目定位为使用者在**自己有权管理的本机官方 Harness**上，进行红队科研与鲁棒性评测的辅助工具。**严禁在未经所有者合法书面授权的目标、公网在线系统或生产业务上运行本项目**。一切测试必须限制在**本机已授权安装的官方 Harness、离线本地合成靶标、授权网络安全演练靶场及合规实验室受控环境**中进行。
5. **目标选择。** 本社区构建不再按地区、行业或自有服务器名单限制红队目标。
6. **严禁违法与违禁用途**：使用者严禁利用本项目直接或间接从事任何违反下列法律法规的行为（必须逐条遵守，不得以任何理由规避）：
  - **《中华人民共和国刑法》**
  - **《中华人民共和国网络安全法》**
  - **《中华人民共和国数据安全法》**
  - **《中华人民共和国个人信息保护法》**
  - 以及其他现行有效的法律、行政法规与监管规定；
  - 同时严禁：
  - 未经授权渗透、攻击公私机构计算机信息系统，实施勒索、破坏、撞库或传播恶意载荷；
  - 诱导、生成或传播危害国家安全、恐怖主义、暴力血腥、涉黄涉赌、诈骗、侵犯公民隐私或知识产权等任何法律明令禁止的违法违禁内容；
  - 违反相关大模型提供商的《服务条款》与《滥用政策》。
7. **使用者独立承担全部责任**：本项目依据 MIT 开源协议“按现状”提供，开发者不对软件的完整性、安全性与适用性作任何明示或暗示的保证。**使用者应对自身的所有下载、部署、运行、修改、传播行为以及由此产生的全部输入与输出后果承担独立、完全的民事、行政及刑事法律责任**。项目作者与贡献团队绝不承担任何因使用者滥用导致的直接、间接或连带责任。
8. **违约即终止授权**：任何将本项目用于非法攻击、恶意活动或违规行为的个人或实体，其开源软件使用许可将自违法违规行为发生之日起**自动且不可撤销地立即终止**。该主体须立即停止使用并永久销毁本项目的所有代码、脚本与衍生数据，并依法承担相应法律制裁。
9. **第三方独立性声明**：本项目属于完全独立的开源安全评测研究项目，与 DeepSeek 官方或其关联主体无任何隶属、商业合作、授权或官方背书关系。文中「官方」仅指评测对象为使用者本机安装的官方 DeepSeek Harness 软件包，**不代表** DeepSeek 官方开发、认可或担保本插件。
10. **必须署名**：借用本项目的名称、思路、代码或提示词，必须署名并标明本仓库。不署名将依法追究责任。详见 [署名要求](#署名要求)。





---

## 适配范围

本构建只针对 **DSH Go 客户端**里内置的那套引擎。别拿去打桌面端 app.asar，也别把桌面端的包喂给 DSH Go。

| DSH Go | 内置 dsh | 插件版本 | 状态 |
| --- | --- | --- | --- |
| **1.1.0** | 0.2.2-rc.1 | **1.1.71-g17**（本仓库 main） | 已实测 —— 85 条补丁，`applied 65 / already 6 / missing_file 6 / skipped 2 / na 6`，与 1.0.16 状态差异 0，`agent.steer(message);` 残留 0 |
| 1.0.16 | 0.2.2-rc.1 | 1.1.71-g16（标签 `v1.1.71-g16`） | 已实测 —— 内含带守卫的 #86 锚点 |
| 1.0.15 | 0.2.2-rc.1 | 1.1.71-g15（标签 `v1.1.71-g15`） | 已实测 |
| 1.0.14 | 0.2.2-rc.1 | 1.1.71-g14 | 宿主自有段 `dsh-go:confirmed-memory` 从这版开始出现 |
| <= 1.0.13 | — | 未验证 | 没有回忆段，行为未测 |

对不上的补丁只会显示 `skipped` / `missing_file`，不会乱改文件。

1.0.16 → 1.1.0 的变化：上游引擎补丁系列从 145 条涨到 149 条（新增 4 条、零删除 —— `deepseek-attachment-error`、`fork-default-effort`、`config-editor-lock-order`、`piai-overflow-output-limit`），但引擎树里真正变的文件只有 **4 个**：`dsh-api-session-controller/lib/index.js`、`dsh-config-editor/lib/index.js`、`dsh-llm-deepseek/lib/index.js`、`@earendil-works/pi-ai/dist/utils/overflow.js`。这 4 个里没有一个锚点漂移 —— 本补丁表只碰 `dsh-llm-deepseek`，而 `dsh-config-editor` 与 pi-ai overflow 压根不在表里。所以 g17 只是版本号与文档的升级：同样 85 条补丁、同样的状态计数。历史留档：1.0.15 → 1.0.16 变了 22 个文件、交集 3 个，唯一真漂移是 #86（1.0.16 在 steer 分支首行插了删除守卫，老锚点整段命中不到却仍报 applied；g16 补了带守卫的锚点，这条锚点在 1.1.0 上照样命中）。

---
## 安装

DSH Go 只能导 **tgz**。三种方式挑一种。

**1. Release 附件**（要长期稳定就用这个）

```text
https://github.com/ssacko510-stack/dsh-purge-go/releases/download/v1.1.71-g17/dsh-purge-1.1.71-g17.tgz
```

**2. 分支归档**（永远是最新的 main）

```text
https://codeload.github.com/ssacko510-stack/dsh-purge-go/tar.gz/refs/heads/main
```

**3. 本地目录** —— 仓库已经 clone 过，就让导入器指这个目录。

- **应用内：** 设置 -> 插件 -> 导入本地 tgz，选 .tgz。解出来必须是 `package/package.json`。
- **手机上不好找文件：** 把 URL 粘进插件的导入框，客户端自己拉。
- **本机有引擎树时走命令行：** `node bin/dsh-purge.js --apply`。

### 导入完要做这三步

1. **彻底退出 DSH Go** 再打开 —— 插件只在启动时进进程。
2. 在新会话点会话标题旁的 **dsh-purge**，进 **清洗** 页点 **「应用」**。
3. 「应用」跑完会自动重启一次让补丁生效；没跑完不会重启。

### 怎样算装上了

- 会话标题旁出现 **dsh-purge**，点开后在「清洗」里有「应用」。
- 聊天里 `/purge status` 能打出 DSH_HOME 和补丁列表，路径应是你正在用的那份。
- 应用后，装好的 @deepseek-ai 树里 `lib/index.js` 带 `// [dsh-purge-...]` 标记 —— 1.1.0 上是 5 个。

### 手动安装

解包后把内层文件夹命名保持 `dsh-purge`，放到 `$DSH_HOME/plugins/dsh-purge`（里面必须有 package.json，name 为 dsh-purge），再写进该 profile 的 bundle 列表并导入。复制整个目录，不要只拷几个 .js。

### 卸载

**dsh-purge** -> **清洗** -> **卸载**：回滚已应用的补丁、还原引擎、重启当前宿主。

```sh
dsh-purge --uninstall
```

---
## 界面预览

会话标题旁有 **dsh-purge**。点开是右侧栏，两页：**清洗** 和 **演练台**。白 / 墨可切换。补丁按组展开，进度只计真正已应用的项。规则集在上方列表启用或删除，下方编辑正文。

第一次进演练台要先读声明、等倒计时、滚到文末并勾选三项。清洗不需要这一步。演练台只用于你有权管理的本机、离线靶标，或已经书面授权的演练环境。

**清洗**

![清洗](docs/preview/dock-clean.png)

**演练台授权**

![演练台授权](docs/preview/dock-auth.png)

**演练台**

![演练台](docs/preview/dock-drill.png)

**补丁**

![补丁](docs/preview/settings.png)

**规则集**

![规则集](docs/preview/rules.png)


| 区域        | 说明                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------- |
| dsh-purge | 会话标题旁的按钮，打开或收起右侧栏                                                                                          |
| 清洗        | 原来的规则设定：补丁、提示词、规则集、Skill                                                                                   |
| 演练台       | 授权后的资产、技能与环境页。未授权时按钮标「未授权」                                                                                 |
| 补丁        | 分组查看状态，应用、还原或卸载                                                                                            |
| 提示词       | 编辑 `prompt-inject.md`，作为会话覆盖段                                                                              |
| 规则集       | 多套 `AGENTS.md` / `CLAUDE.md`；启用写入 `$DSH_HOME`，删除从列表去掉                                                      |
| Skill     | 导入压缩包或文件夹到 `$DSH_HOME/skills/<id>/SKILL.md`（DSH Go 主目录，不写死路径）；命中、加载、`/名称` 由 DSH 负责。也可自己删该文件夹 |


---

## 目录结构

`bin/` 是命令行，`lib/` 是补丁和演练台，`presets/redteam/` 是红队预设，`skills/redteam/` 是随包技能，`client.js` 是侧栏。

运行时文件在 `$DSH_HOME`：`prompt-inject.md`、`rules/`、`skills/`、`redteam/`。未设 `DSH_HOME` 时，先看 DSH Go 主目录下的 `plugins/dsh-purge`，再退回 `~/.dsh`。Skill 不进注入段，也不顶替提示词。

---

## 使用

```sh
# CLI
dsh-purge --status
dsh-purge --apply
dsh-purge --revert
dsh-purge --uninstall
dsh-purge --edit

# 聊天
/purge status | apply | revert | uninstall | edit | help
/rules list | use <id> | create <id> | delete <id> | reset | help
/skills list | import <压缩包或文件夹> | create <id> [说明] | delete <id> | help
/rewind

# 模型工具
purge_status   purge_apply   purge_revert
```

设置页「应用」成功后 DSH Go 会自动重启一次，以加载已改的引擎包；也可手动点「重启」。补丁标题下的版本行显示当前安装的构建（例如 `1.1.71-g17`）。这条线**关掉了面板内自动更新**：更新器只认 `vX.Y.Z` 形态的标签，而本线用 `-g<minor>` 后缀，拿不到就按「无更新」处理，不会把面板刷红。升级方式就是重新导入新的 tgz，和第一次装一样。

输入框旁的「回退一次」和「回退上一轮」跟官方 DSH `session.fork({ atSeq })`：撤回已进行的那一轮，新会话接上之前的上下文，旧会话归档，那句回到输入框，再发送会重新注入。聊天里 `/rewind` 同样可用。

**极简 / PTC 与标准不一致时**：同一任务在标准模式能跑、在极简或 PTC 被拦，通常是 preset 里 `run_code` 或 plan 拦截句没洗净，或内置 minimal 缺少 `agent-instructions`。请升到 **1.1.61+**，**完全退出宿主 → 清洗里应用 → 自动重启 → 新开一轮对话** 再试；只换 preset 不重应用，旧进程里的补丁不会更新。

### 响应速度

DSH 会按顺序执行同一批中的 Bash 调用。旧版 dsh-purge 把默认前台等待从 60 秒提高到了 10 分钟，一条慢命令会让后续调用一起等待。补丁 #21 现在把带插件标记的旧值恢复为官方的 60 秒。无标记的等待时间和其他自定义值会保留；无标记的 10 分钟无法可靠地区分是插件旧值还是用户设置。

在 DSH Go 中，如需更快返回工具结果，可在 `$DSH_HOME/profiles/<profile>/cordis.patch.yml` 添加下面的条目 —— `<profile>` 就是 DSH Go 主目录 `profiles/` 下那一个目录名（没有 `DSH_HOME` 时退回 `~/.dsh/profiles/<profile>/cordis.patch.yml`）。已有相同 id 时修改原条目，不要重复添加。这个 profile 覆盖层在内置配置之后加载，后续应用插件会保留它。

```yaml
- id: bash-sandbox
  config:
    timeoutMs: 10000
```

使用标准 jobs 服务且 `promoteOnTimeout: true` 时，未完成的命令会在 10 秒后返回后台任务 id，并继续运行。用 `job_output` 读取结果、用 `job_kill` 停止。这个设置缩短前台等待，不会让命令本身跑得更快。没有 jobs 服务或关闭自动转后台时，超时会终止命令。单次调用传入的 `timeoutMs` 优先于这里的默认值；`run_in_background: true` 可立即返回任务 id。

日常任务还可以选择让新会话默认使用 Low 推理：

```yaml
- id: agent-default-model
  config:
    provider: deepseek-official
    model: deepseek-flash
    reasoningEffort: low
```

重启 DSH Go 后加载配置。模型和推理等级默认值只用于新建会话，已有会话请在输入框中选择 Low。插件不会自动修改这些模型偏好。需要深入推理的任务可保留 High；搜索文件时应限定目录，避免递归扫描所有应用目录。

### 目标范围

本社区构建不再按地区、行业或自有服务器名单限制红队目标。旧的「自己的服务器」设置和接口已移除。已有的 `net-scope-allow.txt` 文件保留原样，不再读取。

---

## 本地校验

```sh
node --check lib/index.js
node --check lib/core.js
node --check lib/rewind.js
node --check lib/skills.js
node --check client.js
```

---

## 工作原理

应用，启动时或手动点「应用」：

```mermaid
flowchart TD
  A["启动或点应用"] --> B{"补丁已经生效?"}
  B -->|是| C["跳过"]
  B -->|否| D["备份原件为 .dshpurge.bak"]
  D --> E["按补丁列表替换对应文件"]
  E --> F["覆盖 shim"]
  F --> G["注入插件加密默认（提示词框默认显示的那份）"]
```



每次会话的覆盖：

```mermaid
flowchart TD
  A["重启或新会话"] --> B["注入插件加密默认，不必点保存，不读宿主磁盘"]
```



每一轮的提示词注入与规则集决策。左边三个输入就是你在 dsh-purge 面板里控制的东西，虚线表示它们各自驱动哪一步判定：

```mermaid
flowchart TD
  L["规则库：启用某个规则集 → 写入 prompt-inject.md"]
  W["本地规则：勾选当前目录的 AGENTS.md / CLAUDE.md"]
  P["工作区策略：strict / fallback / always"]

  A["新一轮开始"] --> B{"prompt-inject.md 非空?"}
  B -->|是| C["注入 = prompt-inject.md (A)"]
  B -->|否| D{"当前目录有被勾选且非空的本地 md?"}
  D -->|是| E["注入 = 被勾选的 workspace md (B)"]
  D -->|否| F["注入 = 插件加密 slot 默认值 (D)"]
  C --> G{"Workspace baseline 策略 (C)"}
  E --> G
  F --> G
  G -->|strict| H["去掉 DSH workspace baseline 段"]
  G -->|fallback 默认| I{"上面有用户注入内容? (A 或 B)"}
  G -->|always| J["保留 DSH workspace baseline 段"]
  I -->|是| H
  I -->|否| J
  H --> K["最终系统提示词"]
  J --> K

  L -.-> B
  W -.-> D
  P -.-> G
```



Skill 不进注入段：

```mermaid
flowchart LR
  A["设置页导入或 /skills import"] --> B["写到官方 skills 目录"]
  B --> C["由 DSH 加载"]
  C --> D["卸载插件不删用户 Skill"]
```



---

## 还原

- 每个目标文件在应用前备份为 `<文件>.dshpurge.bak`。
- 「还原」或 `/purge revert` 用备份覆盖回去并删除备份；没有备份时去掉 shim 里由本插件写入的行。
- `prompt-inject.md` 是用户文件，还原时保留。
- 「卸载」会先还原（若已应用），再删除注入文件、规则库和插件本身。
- 重复应用是幂等的。

---

## 路径探测

本条线只有一个宿主面：**DSH Go**。桌面面（`web` / `desktop`）属于 [`dsh-purge-fork`](https://github.com/ssacko510-stack/dsh-purge-fork)。

查找顺序：

1. `$DSH_HOME`（显式覆盖，优先）
2. `$DSH_BASE`
3. DSH Go 主目录下的 `plugins/dsh-purge`
4. `~/.dsh`

确定根目录后，改 `node_modules/@deepseek-ai/*`（DSH Go 内置的引擎树）和 `redteam/` 下的覆盖文件与规则集。不碰非 `@deepseek-ai` 的第三方插件源仓库。密封的 `host-commands` / `runtime-commands` 只做清洗，不注入。

DSH Go 的安装包本体不动——不改 `app.asar`，不改签名。点「应用」成功后自动重启 DSH Go 一次，让新引擎文件生效。

找不到目标时提示设置 `DSH_HOME`，不改文件。

---

## 更新

每一版改了什么、安装包在 [Releases](https://github.com/ssacko510-stack/dsh-purge-go/releases)。发新版时把 `package.json` 的版本号改掉，中英文说明写进 `release-notes.md`，推到 `main` 就会自动打包。同一版本再推送不会重复发包。标签直接用 `v<版本号>`，例如 `v1.1.71-g17`。

## 说明

- 改动范围是本机 `@deepseek-ai/*` 包里的渲染文案、默认策略和执行逻辑，以及用户目录下的覆盖文件与规则集。
- 升级后原文对不上会显示跳过，这次应用仍算完成，不会乱改。
- 不改动非 `@deepseek-ai` 的第三方插件源仓库（启动时的 CMD 无感会**尽力**修补已装的 doctor / market / 梁神 / mnemon，属运行时补丁）。
- 安装本构建：把 `https://github.com/ssacko510-stack/dsh-purge-go/releases/download/v1.1.71-g17/dsh-purge-1.1.71-g17.tgz` 粘进 DSH Go 的「添加插件」框；或用 codeload 归档 `https://codeload.github.com/ssacko510-stack/dsh-purge-go/tar.gz/refs/heads/main`。`dsh plugin add --profile web` / `--profile desktop` 属于桌面线，不是这一条。

---

感谢 [LINUX DO](https://linux.do) 社区

## 命令行状态与体检

```sh
node bin/dsh-purge.js --status --json
node bin/dsh-purge.js --status --base /path/to/node_modules/@deepseek-ai
node bin/dsh-purge.js --doctor --json
node bin/dsh-purge.js --doctor --save-baseline
node bin/dsh-purge.js --doctor --repo /path/to/linked/checkout --json
```

状态会列出能解析到的各份安装，并报出引擎树里当前实际存在的标记，用来区分「全部应用」和「只应用了一部分」。`--surface` 参数仍然接受（兼容旧脚本），但这条线只有一个宿主面（DSH Go），真正决定装哪一份的是 `--base`。

doctor 全部检查通过时退出码为 0，否则为 1。只有健康状态可以保存基线，并记录宿主路径以避免混用不同安装的基线。`--repo` 用于链接到工作副本的开发安装；包缺失、链接失效或独立复制目录都不会通过该检查。

`--json` 仅支持状态和体检命令。与应用、还原、编辑或卸载操作组合时会报错，不执行该操作。


## 事务式更新器

**这条线按设计关掉了面板内自动更新。** `checkUpdate()` 挑 Release 资产时只认 `v?X.Y.Z` 形态的标签，而这里的版本号一律带 `-g<minor>` 后缀（`1.1.71-g17`），严格匹配永远过不了。与其让面板报错变红，这个分支直接返回「无更新」，并提示去拿 tgz。

所以升级是固定的手工动作：从 [Releases](https://github.com/ssacko510-stack/dsh-purge-go/releases) 下载新的 `dsh-purge-<版本>.tgz`，粘进「添加插件」，然后**彻底退出 DSH Go → 重新打开 → 清洗页点应用**。导入只是替换插件本体，引擎补丁会重新打一遍，不涉及回滚状态。

事务式更新器（`lib/update-transaction.js`、`lib/update-worker.js`、`lib/update-supervisor.js`）仍然随包发布，指向你自己控制的仓库时照样能用：先备份文件、带上 skills/scripts，新宿主验证生效后才提交版本状态。Git 本地有修改时停止更新。保留最近两份已验证的旧版备份，异常或带链接的备份保留并报告。启动失败按记录恢复文件，最多重启恢复一次。需要 Node >=22.13.0 及可用的 `node:sqlite`。
