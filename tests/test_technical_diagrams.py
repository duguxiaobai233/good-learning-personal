"""Regression checks for diagram-bearing lessons; no TeX install required."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_study_pdf.py"
SPEC = importlib.util.spec_from_file_location("render_study_pdf", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)

PICTURE = r"""\begin{tikzpicture}
\node[draw] (g) {$\frac{1}{s+1}$};
\draw[-{Stealth}] (-2,0) -- (g.west);
\end{tikzpicture}"""
FENCED = "```tikz\n" + PICTURE + "\n```"


class TechnicalDiagramTests(unittest.TestCase):
    def test_existing_text_math_and_table(self):
        result = renderer.body_tex(
            "# 标题\n\n文字 **重点** 和 $G(s)$。\n\n"
            "| 变量 | 含义 |\n| --- | --- |\n| $r$ | 输入 |\n\n"
            "- 一个要点\n", "errors", "compact")
        self.assertIn(r"\chaptertitle{标题}", result)
        self.assertIn(r"文字 \textbf{重点} 和 $G(s)$。", result)
        self.assertIn(r"$r$ & 输入", result)
        self.assertIn(r"\item 一个要点", result)

    def test_tikz_is_vector_source_at_its_text_position(self):
        result = renderer.body_tex("图前\n\n" + FENCED + "\n\n图后", "diagram", "compact")
        self.assertIn(PICTURE, result)
        self.assertNotIn(r"\begin{verbatim}", result)
        self.assertNotIn(r"\begin{figure}", result)
        self.assertLess(result.index("图前"), result.index(PICTURE))
        self.assertLess(result.index(PICTURE), result.index("图后"))

    def test_code_contents_not_parsed_as_markdown(self):
        code = '# not a heading\n    $variable = 2\n|a|b|\n**A1.** literal'
        result = renderer.body_tex("```python\n" + code + "\n```", "day", "loose")
        self.assertIn("\\begin{verbatim}\n" + code + "\n\\end{verbatim}", result)
        self.assertNotIn(r"\chaptertitle", result)
        self.assertNotIn(r"\QuestionSpace", result)

    def test_long_and_tilde_fences(self):
        source = "~~~~text\n```\n~~~~~\n\n````tikz\n" + PICTURE + "\n`````"
        result = renderer.body_tex(source, "diagram", "compact")
        self.assertIn("\\begin{verbatim}\n```\n\\end{verbatim}", result)
        self.assertIn(PICTURE, result)

    def test_loose_question_space_follows_all_conditions_and_figure(self):
        source = ("## 独立练习\n\n**A1.** 求输出。\n\n" + FENCED
                  + "\n\n补充条件：零初始状态。\n\n"
                  "**A2.** 判断稳定性。\n\n## 答案\n\n答案文本。")
        result = renderer.body_tex(source, "day", "loose")
        positions = [result.index(fragment) for fragment in (
            r"\CompactQuestion{A1}", PICTURE, "补充条件", r"\QuestionSpace{23}",
            r"\CompactQuestion{A2}", r"\QuestionSpace{26}", r"\section{答案}",
        )]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(result.count(r"\QuestionSpace{"), 2)

    def test_compact_questions_keep_figures_without_answer_spaces(self):
        source = "## 独立练习\n\n**A1.** 看图作答。\n\n" + FENCED
        result = renderer.body_tex(source, "day", "compact")
        self.assertIn(PICTURE, result)
        self.assertNotIn(r"\QuestionSpace", result)

    def test_last_question_is_closed_at_end_of_file(self):
        result = renderer.body_tex(
            "## 错题 1\n\n### 再做一题\n\n**R1.** 作答。\n\n最后条件。",
            "errors", "loose")
        self.assertIn(r"\CompactQuestionColon{R1}", result)
        self.assertTrue(result.endswith(r"\QuestionSpace{42}"))
        self.assertLess(result.index("最后条件"), result.index(r"\QuestionSpace"))

    def test_unclosed_fence_reports_location(self):
        with self.assertRaisesRegex(ValueError, "Unclosed code fence at line 3"):
            renderer.body_tex("# 标题\n\n```tikz\n" + PICTURE, "diagram", "compact")

    def test_malformed_picture_is_not_silently_typeset_as_code(self):
        for content in ("", r"\draw (0,0) -- (1,0);", PICTURE + "\n" + PICTURE,
                        PICTURE.replace(r"\end{tikzpicture}", "")):
            with self.subTest(content=content):
                with self.assertRaisesRegex(ValueError, "TikZ fence at line 1"):
                    renderer.body_tex("```tikz\n" + content + "\n```", "diagram", "compact")

    def test_diagram_document_does_not_require_cover_config(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "lesson.md"
            output = Path(directory) / "lesson.tex"
            source.write_text("# 技术图\n\n" + FENCED, encoding="utf-8")
            renderer.render(source, output, "diagram", "compact", {})
            tex = output.read_text(encoding="utf-8")
            self.assertIn(PICTURE, tex)
            self.assertIn(r"\usetikzlibrary{arrows.meta,positioning,calc,shapes.geometric,fit}", tex)
            self.assertNotIn("学习导图", tex)
            self.assertTrue(tex.endswith("\\end{document}\n"))


if __name__ == "__main__":
    unittest.main()
