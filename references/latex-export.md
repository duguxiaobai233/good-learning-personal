# LaTeX 导出

本 skill 产出的**每一份 PDF**，不论学科或是否有公式，均须先生成 `.tex`，再用 XeLaTeX 或 LuaLaTeX 实际编译。知识清单、备考计划等主文件的最终 PDF 放在科目或比赛文件夹顶层；每日课程 PDF 放在各自的 `每日学习/D001-YYYY-MM-DD` 文件夹。对应 `.tex` 放在同级 `源文件` 子目录，保持同名以便重编译。公式直接保留 LaTeX 数学模式；不得使用网页打印、Word 导出、ReportLab 等其他方式替代编译。若编译器不可用，先排查或安装，仍不可用时明确告知 PDF 尚未完成，不输出来源不明的 PDF。

工作区的 [`scripts/render_study_pdf.py`](../scripts/render_study_pdf.py) 可把本 skill 常用的 Markdown（标题、段落、列表、表格、粗体、链接和 `$...$`／`$$...$$` 公式）转成黑白 XeLaTeX 文档。它从一个 JSON 文件读取导图信息：顶层分别以 `knowledge`、`plan`、`day` 为键，每项有 `title`、`center` 和六个 `nodes`；每个节点有 `title` 与 `lines`。如果材料含脚本未支持的 Markdown，先扩展转换逻辑或直接编写 `.tex`，不得丢失正文。

```text
python scripts/render_study_pdf.py 科目/每日学习/D001-YYYY-MM-DD/源文件/今日课程.md 科目/每日学习/D001-YYYY-MM-DD/源文件/今日课程-紧凑.tex --kind day --layout compact --map-config 科目/每日学习/D001-YYYY-MM-DD/源文件/导图.json
python scripts/render_study_pdf.py 科目/每日学习/D001-YYYY-MM-DD/源文件/今日课程.md 科目/每日学习/D001-YYYY-MM-DD/源文件/今日课程-宽松.tex --kind day --layout loose --map-config 科目/每日学习/D001-YYYY-MM-DD/源文件/导图.json
python scripts/compile_study_pdf.py 科目/每日学习/D001-YYYY-MM-DD/源文件/今日课程-紧凑.tex 科目/每日学习/D001-YYYY-MM-DD/今日课程-紧凑.pdf
python scripts/compile_study_pdf.py 科目/每日学习/D001-YYYY-MM-DD/源文件/今日课程-宽松.tex 科目/每日学习/D001-YYYY-MM-DD/今日课程-宽松.pdf
```

对知识清单和备考计划分别使用 `--kind knowledge`、`--kind plan`。每日课程按知识关系用 `## 单元 N...` 组织，单元中先给完整知识讲解，再给相应例题和练习；脚本使单元另起一页。从允许材料选取的挑战原题可放在 `### 举一反三` 下，集中或混合练习放在 `## 独立练习` 下，使用 `**A1.**` 一类题号。这些标题只是排版入口，不要求生成填步题或每例固定配题；原题选择遵循 [每日学习与调整](daily-study.md)。脚本只给独立题留作答空白，例题不留白；按实际解答量调整空白高度。题目所需图表、程序、情境和数据必须与题干完整保留，不能用前面例题或原课件页码代替；来源短注与题目正文分开。若转换脚本不能正确保留必要格式，调整结构或直接编写 TeX。每题依次排完整原题、简明答案、详细解析和题型与模型总结，不将答案统一移到文末。可使用 `### 简明答案`、`### 详细解析`、`### 题型与模型总结`，每道后续练习用 `## 独立练习 N` 恢复题目排版。宽松版的作答区置于本题答案与解析之后，保证简明答案紧接原题；若自动留白位置不符合此顺序，直接调整 TeX 的 `\QuestionSpace` 位置。例题不留作答区。

错题本用 --kind errors 渲染，不需要导图 JSON；不制作思维导图、独立封面或其他非正题内容，首页直接进入第一条错题。每条错题采用“错题 N”二级标题，第二条起另起一页。只保留原题、实际作答、错因、完整订正与掌握状态，不添加复做题、日期或勾选表。正文排版采用黑白、宽页边距、较舒展的行距和段距；表格优先不用竖线，留足行高。核心例题和错题记录都不要在同页堆叠，题干与步骤保持在一起，避免标题落在页尾。紧凑版也保留阅读所需空白；两个版本只在独立题的作答区有差异。编译器源文件应能在本机重新编译成同一内容的 PDF。

编译脚本实际调用 XeLaTeX 两遍，用临时 ASCII 文件名避开 Windows 上中文日志文件名写入失败；若要使用 LuaLaTeX，可传 --compiler lualatex。源文件应为自包含的 LaTeX 文档。检查日志中的缺字与越界警告，渲染 PDF 的每一页检查中文、公式、导图、表格和作答空白。紧凑版和宽松版必须出自同一份课程文本，核对题目及答案完整一致。

## 课程内的技术图

涉及控制框图、信号流图或数据结构状态等教学内容时，按 [教学配图](technical-diagrams.md) 生成实际图。转换脚本已支持 `tikz` 代码围栏：围栏内容是一个完整的 `\begin{tikzpicture}...\end{tikzpicture}`，输出原位矢量图；普通代码围栏仍作为代码排版。预加载 `arrows.meta, positioning, calc, shapes.geometric, fit`。图不能依赖临时编译目录之外的文件。示例见 [配图示例](../examples/technical-diagrams.md)。

日常课程仍使用 `--kind day --layout compact/loose`。独立的教学图说明或安装验证可用 `--kind diagram`，无需 `--map-config`，不生成导图封面。图仅在超出行宽时缩小；过密或过高的图需要重排或拆图，不以过小字体勉强放下。图题置于紧邻图的正文，宽松版练习题的作答空白放在该题答案、解析与模型总结之后，简明答案紧接完整题干与附图。Markdown 查看器不一定绘制 TikZ，交付须提供实际编译的 PDF 或渲染后的 PNG。
