# Good Learning

本仓库是 B 站 Good Learning 项目的个人优化与版本归档，基于 [yoli-mi/good-learning-skill](https://github.com/yoli-mi/good-learning-skill) 修改；这里的优化不是上游作者的官方发布。感谢原项目作者，原始 Git 历史与 MIT 许可证均予以保留。

一个用于 AI agent 的学习与备考 skill：根据考纲、教材、真题和可用时间建立知识清单、备考计划与每日课程，再依据真实作答整理错题并调整后续安排

## 能做什么

- 分别制作知识清单和备考计划，保留知识点编号、验收标准及来源
- 按零基础或复习模式生成自成体系的每日课程，包括完整原题例题、跨来源挑战练习、就地展示的答案与模型总结
- 根据用户的实际作答制作错题本；演示错误会标为模拟，不计入真实掌握状态
- 为当日复盘绘制 SVG 思维导图，可选生成 PNG 预览
- 通过 XeLaTeX 或 LuaLaTeX 编译课程、清单、计划和错题本 PDF；科目目录存放知识清单和备考计划 PDF，每日课程按日期独立成夹；各文件夹顶层只放最终 PDF，Markdown、`.tex` 和其他源文件放在对应的 `源文件` 子目录

## 输出目录

```text
科目或比赛/
├── 知识清单.pdf
├── 备考计划.pdf
├── 源文件/
└── 每日学习/
    └── D001-YYYY-MM-DD/
        ├── D001-紧凑排版型.pdf
        ├── D001-宽松排版型.pdf
        └── 源文件/  课程文本、LaTeX、配置与当日学习记录
```

后续课程按真实学习进度逐日建立，用户提交作答或错题后更新对应日期的记录，并调整尚未完成的学习任务

## 安装

以codex为示例：把仓库克隆或复制为 Codex skills 目录下的 `good-learning` 文件夹，重启 Codex 或重新加载 skills 后即可使用

```text
~/.codex/skills/good-learning/SKILL.md
```

示例请求：

```text
我准备参加一项数学竞赛，每天能学三小时，请帮我制定知识清单和备考计划
我是零基础，开始今天的学习
这里是我的作答，请核对并制作错题本
根据今天的知识和错题绘制总结思维导图
```

## 运行环境

- Python 3.10 或更新版本
- PDF：XeLaTeX 或 LuaLaTeX，以及 `ctex`、`amsmath`、`tikz` 等常用 LaTeX 宏包
- 总结图 PNG：Pillow，使用 `pip install -r requirements.txt` 安装
- 总结图 SVG：只需 Python 标准库
- 生成 PNG 时需提供中文字体；脚本可自动查找常见字体，也可用 `--font` 和 `--bold-font` 指定

## 脚本

```text
scripts/render_study_pdf.py      常用 Markdown → LaTeX
scripts/compile_study_pdf.py     LaTeX → PDF
scripts/render_summary_map.py    JSON → SVG，可选 PNG
```

总结图输入为 JSON，包含 `eyebrow`、`title`、`subtitle`、`status`、`description`、`core_label`、`core_title`、`core_subtitle`、`core_foot`、`workload`、`error_count`、`legend`、`note_legend`、`footer`，以及 4—6 个 `branches`；每个分支填写 `side`、`category`、`title`、`rule`、`detail`，如有错题再填写 `error.number`、`error.label`、`error.mistake`、`error.fix`；无错题时填写 `check` 与 `check_fix`

```text
python scripts/render_summary_map.py examples/summary-map.json summary.svg --png summary.png
```

具体工作流程见 [SKILL.md](SKILL.md)，设计与资料检索规则见 [references](references)

## 内容边界

本归档包含 skill 指令、生成脚本、修改报告和验证示例，不包含教材、历年试卷、用户作答或真实个人学习文件；使用资料时请核对来源与授权。

## 许可证

[MIT](LICENSE)

## 本机定制版本与报告

本归档保留上游原始历史及本机定制版本；详见 [版本导航与修改报告](reports/版本导航.md)。

## 本机定制：教学配图

2026-10-28 版本增加按内容主动生成专业图的规则，复用 TikZ/PGF 绘制控制框图、信号流图和数据结构状态图。参见 [教学配图规则](references/technical-diagrams.md) 和 [可编译示例](examples/technical-diagrams.md)。

课程源稿中的 `tikz` 围栏将渲染为图，普通代码围栏保留为代码。独立图示文档可用 `render_study_pdf.py 输入.md 输出.tex --kind diagram`，随后用原有编译器生成 PDF；每日课程继续使用 compact/loose 两种排版。源图及公式需要语义核对，PDF 需要实际渲染检查。验证渲染器可运行 `python -m unittest discover -s tests -v`。

## 例题解答优化（2026-11-01）

例题就地提供推理所需的图示与关键关系，明确图号，展开关键因果与计算量的选择，直接完成各问。内部边界检查不全部搬进正文，省略重复限制与无关例外；交付前逐例检查能否独立读懂。详见[本次更新说明](reports/worked-examples-2026-11-01/更新说明.md)和[版本导航](reports/版本导航.md)。

## 原题挑战与答案优先（2026-11-16）

仅选用户提供或明确指定的原题，取消新编、改写及公开高校／开放教材补题；知识匹配优先，混合课件与课本、练习册来源，主动安排挑战。整题逻辑完整，解释课件结论并总结模型，不附加易错提醒；答案紧接原题，取消错题复做。详见[更新说明](reports/original-question-challenges-2026-11-16/更新说明.md)。

## 讲义讲解原则精简（2026-11-16）

讲义讲解只保留七条原则，删除其展开细则及时间不足时的固定取舍、教学完整性验收清单；保留原题核对、答案正确性和 PDF 排版检查。历史版本说明不作为现行要求。详见[更新说明](reports/teaching-principles-2026-11-16/更新说明.md)。
