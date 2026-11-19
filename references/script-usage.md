# 本地脚本使用

依赖：Python 3.10 或以上。除图片工具外只使用Python标准库。先将工作目录切到本Skill文件夹，或把命令中的相对路径替换为实际绝对路径。下述输出文件/目录必须尚不存在；重试时使用新路径，原输入和旧结果都保留。

```sh
python scripts/organize_sources.py references/sources.csv --output sources-result.json
```

## 输入与示例预期

CSV必须含record_id,platform,question_id,url,location。每行一个URL；location建议用body、source_panel、video_card。缺归属的字段可留空，脚本保留独立行。输出3个有效归属行、2个全局唯一URL、1个无效行。

## 能力边界

URL只规范主机和默认端口，不删查询参数和片段，不联网。原有title、source_type等列保留；分类依据由AI另行核查。

所有样例使用example.com及虚构资料，不能当客户实测。脚本不含遥测或付费API，不会发布内容。发现问题会写入报告，不代表执行异常；命令参数或输入格式错误返回退出码2。图片工具有文件处理失败时返回1并保留manifest；跳过动画会记录原因。
