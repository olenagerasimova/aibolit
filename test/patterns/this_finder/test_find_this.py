# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.hybrid_constructor.hybrid_constructor import HybridConstructor
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class HybridConstructorTestCase(TestCase):
    cur_dir = Path(__file__).absolute().parent

    def test_several(self):
        filepath = Path(self.cur_dir, "several.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [4, 10, 20])

    def test_simple2(self):
        filepath = Path(self.cur_dir, "init_block.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple22(self):
        filepath = Path(self.cur_dir, "init_static_block.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple3(self):
        filepath = Path(self.cur_dir, "autocloseable.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [4, 14, 31])

    def test_simple5(self):
        filepath = Path(self.cur_dir, "one_line_usage.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [12])

    def test_simple6(self):
        filepath = Path(self.cur_dir, "super.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [12])

    def test_simple7(self):
        filepath = Path(self.cur_dir, "holy_moly_constructor.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [47])

    def test_simple9(self):
        filepath = Path(self.cur_dir, "super_this.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15, 25, 51, 62, 76, 87, 101])

    def test_simple10(self):
        filepath = Path(self.cur_dir, "BookmarkEditCmd.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple11(self):
        filepath = Path(self.cur_dir, "ChainedBuffer.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple12(self):
        filepath = Path(self.cur_dir, "CliMethodExtraSections.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple13(self):
        filepath = Path(self.cur_dir, "LengthStringOrdinalSet.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple14(self):
        filepath = Path(self.cur_dir, "LoaderInfoHeader.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple15(self):
        filepath = Path(self.cur_dir, "OmfModuleEnd.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
