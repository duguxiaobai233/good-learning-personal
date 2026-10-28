# Good Learning 本机环境

- 项目来源：<https://github.com/yoli-mi/good-learning-skill>
- 安装提交：`1255c4d7f0b602901100d29d85235ad2537eec31`
- 技能目录：`C:\Users\sora\.codex\skills\good-learning`
- 仓库副本：`C:\Users\sora\Documents\Codex\2026-10-25\github-https-github-com-yoli-mi\good-learning-skill`
- 本机运行环境：`C:\Users\sora\Documents\Codex\tools\good-learning`

技能不需要 API 密钥，也没有需要单独启动的服务。安装后可在后续对话中用 `$good-learning` 调用；若未显示，可重新加载技能或重启 Codex。

## 自动保存与续学

默认学习记录目录：`C:\Users\sora\Documents\Codex\学习记录`。根目录中的 `学习索引.md` 记录各科目位置和最近活动科目；科目内的 `源文件/学习进度.md` 及每日 `源文件/学习记录.md` 保存实际进度。

每次使用本技能时主动读取已有记录；“继续学习”默认接续最近活动科目。生成计划、课程或收到学习反馈后自动保存并更新索引，无需重复提供路径或提醒保存。尚未收到作答或完成反馈时保持待验证。用户明确另选目录时以其选择为准。

## 依赖

Python 使用上述运行环境内的独立虚拟环境 `venv`，基于 Codex 自带 Python 3.12.14，并继承已有的 Pillow 12.3.0。它不修改系统 Python 环境。

PDF 编译使用本机专用的 MiKTeX 26.5 Portable 目录：`C:\Users\sora\Documents\Codex\tools\good-learning\miktex`。已安装 ctex、xeCJK、geometry、booktabs、needspace、enumitem、fancyhdr、microtype 及编译中所需的其他依赖；amsmath、amsfonts、TikZ 等由基础环境提供。

2026-10-25 验证通过：已用安装后的脚本生成 SVG 和 PNG，并用 XeLaTeX 两遍编译含中文、公式、表格、圈号和六节点导图的 5 页 PDF，完成逐页目视检查；在默认受限执行环境下再次编译也通过。原有三个 Python 脚本与仓库内容一致。

MiKTeX 已设置中国科学技术大学 CTAN 镜像并允许自动补齐缺少的宏包；后续首次使用其他宏包时可能仍需联网。启动入口仅为当前运行临时添加环境路径，不修改系统 PATH。虚拟环境继承 Codex 自带 Python 的库；若未来该运行时被移除，应重新创建虚拟环境。

PNG 使用 Windows 中文字体：

- 常规：`C:\Windows\Fonts\msyh.ttc`
- 粗体：`C:\Windows\Fonts\msyhbd.ttc`

## 运行脚本

用技能目录的 `scripts\run-local.ps1` 运行脚本，由它选择本机 Python 和 LaTeX 路径。例如在 PowerShell 中：

```powershell
$runner = 'C:\Users\sora\.codex\skills\good-learning\scripts\run-local.ps1'
& $runner --check
& $runner render_summary_map.py 'C:\Users\sora\.codex\skills\good-learning\examples\summary-map.json' '.\summary.svg' --png '.\summary.png' --font 'C:\Windows\Fonts\msyh.ttc' --bold-font 'C:\Windows\Fonts\msyhbd.ttc'
& $runner compile_study_pdf.py '.\课程.tex' '.\课程.pdf'
```

运行时将示例输入、输出路径替换为自己的文件路径。课程 Markdown 转换为 LaTeX 可使用同一入口调用 `render_study_pdf.py`，具体参数见仓库 README 和 `references\latex-export.md`。

若 PowerShell 的脚本策略阻止运行，可用 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File` 调用该入口；这只影响当前进程，不修改系统策略。

## 教学配图更新（2026-10-28）

复用已安装的 TikZ/PGF，没有新增 Python 包或在线服务。课程转换器支持 `tikz` 围栏、普通代码围栏和无封面的 `--kind diagram`；常用 TikZ 库由现有 PGF 提供。示例位于 `examples/technical-diagrams.md`，按 `references/technical-diagrams.md` 生成并检查技术图。现有学习记录和两种课程 PDF 排版继续沿用。
