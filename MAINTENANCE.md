# MAINTENANCE — 两条线怎么维护

这个项目在本机同时存在两份产物，**目标宿主不同、安装方式不同、代码也不是同一棵树**。改动前先确认自己在改哪一条。

| | **DSH Go 线**（本仓库） | **电脑桌面线** |
| --- | --- | --- |
| 仓库 | `ssacko510-stack/dsh-purge-go`（本仓库） | `ssacko510-stack/dsh-purge-fork` |
| 本地目录 | `D:/09_成果输出/DSH成果/05-DSH与AI工具链/dsh-purge-Go版` | `D:/09_成果输出/DSH成果/05-DSH与AI工具链/dsh-purge-个人维护版` |
| 目标宿主 | DSH Go 客户端（内置 dsh 0.2.2-rc.1） | `dsh web` / 官方桌面版（dsh 0.2.x，打 `app.asar`） |
| 版本号 | `1.1.71-g17` 这种 `-g<GoMinor>` 号段 | `1.1.71` 这种上游号段 |
| 交付物 | `dsh-purge-1.1.71-g17.tgz`（tarball 导入） | zip / 目录树 |
| 独有代码 | `lib/anchor.js`、`lib/identity.js` 的宿主回忆段放行、`lib/runtime-check.js`、`lib/subagent-control.js`、`lib/update-*.js`、`NOTICE` | `lib/net-scope.js`、`normalizeChatmlLayout` 等桌面壳逻辑 |
| 上游同步 | 从社区 `realMisakaMikoto/dsh-purge` 切；补丁表与桌面线共用 | 同源，但**不要**直接 merge 上游 1.6.x |

## Go 线版本号规则

`1.1.71-g17` = 上游补丁表基线 1.1.71 + 面向 DSH Go **1.1.0**。DSH Go 每升一次，就发一个 `-g<minor>`：

```sh
DSH Go 1.0.14 → 1.1.71-g14
DSH Go 1.0.15 → 1.1.71-g15
DSH Go 1.0.16 → 1.1.71-g16
DSH Go 1.1.0  → 1.1.71-g17   ← 当前
```

**不要**用 `1.1.71` 这个裸号段发 Go 线：面板的更新器会把它跟桌面线的版本号搞混。

## 适配新一版 DSH Go 的流程

1. **拿到新旧两棵树**。装好新版 DSH Go，定位它的 `@deepseek-ai` 引擎树；旧版从安装包或历史副本里解出来。
2. **算差异面**。新版先从上游 release 资产里把 `runtime/patches/` 的 `series` + `pins.json` 取下来，用 pins 里每个文件的 `before`/`after` sha256 重建出一棵精确的引擎树；再用整棵树逐文件 sha256 对比。1.0.16 → 1.1.0 是 **4 个文件**（1.0.15 → 1.0.16 那次是 22 个）。

```sh
python build110b.py   # 按 pins110 重建 eng110，逐文件校验 after sha256
python build15.py     # 全树 sha 对比，输出 changed*.json + delta*.diff
```

3. **取交集**。只留 purge 补丁表里 `file` 字段指向的那些包。1.1.0 的 4 个变动文件里，交集只有 **1 个**：
   - `dsh-llm-deepseek/lib/index.js` → 表里确有键，但 1.1.0 改的是 `isAttachmentError` 那两行，不在锚点上
   不在表里、无需处理的 3 个：`dsh-api-session-controller/lib/index.js`（改的是 `fork-default-effort` 的 reasoningEffort 两行，与 #85/#86 的 steer 块不重叠）、`dsh-config-editor/lib/index.js`、`@earendil-works/pi-ai/dist/utils/overflow.js`。
   历史留档：1.0.16 的交集是 3 个（session-controller #85/#86、client-ui-conversation #56/#77、anthropic-messages #47/#49）。
4. **逐 replacement 探针**。判据是「旧树命中 > 0 且新树命中 = 0」= DRIFT。

```sh
node an45.py          # 227 个 rep 全量跑一遍
```

   1.0.16 只有 1 条真漂移：#86 的 rep0。1.1.0 **零漂移**（227 个 replacement 全量跑过，无一从 "旧树命中>0" 变成 "新树命中=0"）。
5. **补锚点，不换锚点**。老 pattern 全留着，新形状**追加**在后面，旧宿主继续能打。
6. **双树实测**。两棵树各跑一次 `core.applyPatches`，比 status 计数：

```sh
node run5.js
# 期望：applied 65 / already 6 / skipped 2 / missing_file 6 / na 6，STATUS DIFFS 0
```

7. **数标记**。打完补丁后 `dsh-purge-\d+` 标记要存在，被替换掉的旧语句残留为 0。
8. **改版本号**：`package.json` 的 `version` 与 `description`。
9. **打包 + 上传**（见下节）。

### 坑

- **锚点整段 miss 但报告 applied**。一条补丁可以有多个 `file` 键、多个 replacement；只要有一个命中，状态就是 applied，其余静默失效。#86 在 1.0.16 上就是这样退化成 `agent.steer()` 的。**判断是否真生效，看替换后的文本和残留计数，不要只看状态**。
- **别用错路径键**。`targetFiles` 的 key 形如 `node_modules/@deepseek-ai/<pkg>/lib/x.js`，切段时丢了 `node_modules` 前缀就会全 MISS。
- **同一语句有多处**。`agent.steer(message);` 在 1.0.16 / 1.1.0 的 session-controller 里都有 2 处（队列分支 + 方法体），锚点要够长，别误伤。
- **更新器不认本线版本号**。`lib/update.js` 的 `completeRelease` 要求 tag 形如 `v?\d+\.\d+\.\d+`，`1.1.71-g17` 过不了。g16 起在 `checkUpdate` 里降级成「无更新 + 请重新导入 tgz」，面板照常渲染。

## 打包

tgz 必须是 npm 形态：所有条目在 `package/` 前缀下、只有文件条目、无目录条目、mode `0o666`。

本机没有 npm CLI，用 Python `tarfile` 手工复刻：

```sh
"C:/Users/Honor/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/python.exe" pack.py
```

产物落到 `dist/dsh-purge-1.1.71-g17.tgz`。打完必须**解包再跑一遍 applyPatches**，确认包里的东西跟源树一致（`scripts/verify-pack.js`）。

## 发布

1. 改 `package.json` 的版本与 `description`。
2. 在 `release-notes.md` **顶部**加一节，中文在前英文在后。
3. 提交，推 `main`。
4. 打 tag `v<version>`，推上去。
5. 建 Release，附 `dsh-purge-<version>.tgz` 与 `SHA256SUMS`。

发布后核对：README 里三个导入链接（Release 资产 / codeload 归档 / 本地目录）都得能打开。

## 不要做

- 不要在两个仓库之间互相 `merge`。补丁表可以比，宿主适配层不行。
- 不要把桌面线的 `app.asar` 补丁塞进 Go 线。
- 不要在 `release-notes.md` 里删旧版本条目 —— 面板会读版本历史。
