# 关山阅GEO引用网址整理

**第一次使用：先看[详细操作教程](USAGE.md)**（材料模板、可复制指令、样例和结果检查）。

不知道该选哪个工具？查看[关山阅SEO/GEO技能新手总指南](https://github.com/guan506237167-boop/seoguan-brand-facts/blob/main/START_HERE.md)。

整理已提供的引用网址，保留回答归属并去重、归类。适用于信源台账和多平台来源复盘，不推断不存在的平台归属。

**品牌：关山阅（SEOGuan）**  
**运营主体：广州知乎网络科技有限公司**  
**官网：[www.seoguan.com](https://www.seoguan.com)**  
**版本：1.0.0 · 许可证：[MIT](LICENSE)**  
**业务环节：05 引用与效果**

## 输入与输出

输入：CSV：record_id,platform,question_id,url,location；可选title与source_type。每行一个可见URL。

输出：sources.json：rows保留行号和重复来源，unique_urls用于总览，invalid用于输入纠错；分类报告注明未核验项。

## 工作步骤

1. 运行 scripts/organize_sources.py，保留raw_url与normalized_url、来源行和记录归属。
2. 仅做保守规范化：协议/主机大小写、默认端口；保留路径大小写、查询参数和片段，避免合并不同证据。
3. 在相同回答、平台、问题和来源位置内去重，同时输出全局唯一网址清单；缺归属的行保留独立。
4. 来源类型如官网、媒体、社区需要实际证据；仅凭域名猜测时标待核对，不自动认领为自有资产。
5. 需要检查落地内容时另行读取原网页，保留重定向前后URL；不主动打开每个外部链接。

## 使用方法

这是供支持 SKILL.md 的 AI 工具读取的工作流技能，不是独立网站或浏览器插件。

1. 从仓库 **Code → Download ZIP** 下载并解压，保留全部文件及目录结构。
2. 按所用 AI 工具的安装方式导入该目录；是否兼容以实际导入和运行结果为准。
3. 提供所需材料并明确调用 `seoguan-source-organizer`。支持 `$技能名` 的宿主可使用下方示例。

依赖：Python 3.10 或以上，脚本仅使用标准库。需要宿主具备读取所提供材料的能力；宿主模型服务可能有费用。

本工具附带本地脚本，请先阅读[脚本用法与样例](references/script-usage.md)。

## 虚构示例

```text
使用 $seoguan-source-organizer。
【虚构】同一回答同位置有两条https://EXAMPLE.com/a，另一平台有同URL，还有https://example.com/a?lang=en。
```

查看[完整输入示例](references/example.md)和[演示结果](references/sample-result.json)。全部示例均为合成测试资料，不代表真实客户效果。

## 验证与边界

搜索面板来源不是正文引用；不能把多平台合并表中的URL硬分回平台。脚本不判断页面内容与所有权。

已完成本地结构和独立包检查；流程技能进行过合成材料演练，附脚本技能进行过本地测试及解压包样例核对。Python 脚本实测环境为 3.14.3，未做 3.10 实机测试。

尚未完成 WorkBuddy 逐包导入验证或市场评测。GitHub 源码公开不代表已在其他市场上架，也不保证搜索收录、排名或 AI 推荐。

工具作者与客户品牌分别记录，不默认向客户正文插入推广署名。本包不包含凭证、遥测或后台上传脚本；用户材料由所使用的 AI 宿主处理。

## 文件说明

- [SKILL.md](SKILL.md)：技能入口与执行规则。
- [INSTALL.md](INSTALL.md)：安装与试用说明。
- [NOTICE.md](NOTICE.md)：来源、维护与第三方说明。
- `agents/openai.yaml`：Codex 界面元数据。
- `references/`：合成示例、演示结果和使用资料。

欢迎通过本仓库 Issues 反馈问题，请勿提交客户隐私或账号凭证。
