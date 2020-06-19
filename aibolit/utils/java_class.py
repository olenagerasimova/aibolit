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


from functools import cached_property

from typing import Dict, Set, TYPE_CHECKING
from networkx import DiGraph  # type: ignore

from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.java_class_method import JavaClassMethod
from aibolit.utils.java_class_field import JavaClassField

if TYPE_CHECKING:
    from aibolit.utils.java_package import JavaPackage


class JavaClass(AST):
    def __init__(self, tree: DiGraph, root: int, java_package: 'JavaPackage'):
        self.tree = tree
        self.root = root
        self._java_package = java_package

    @cached_property
    def name(self) -> str:
        try:
            class_name = next(self.children_with_type(self.root, ASTNodeType.STRING))
            return self.tree.nodes[class_name]['string']
        except StopIteration:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def package(self) -> 'JavaPackage':
        return self._java_package

    @cached_property
    def methods(self) -> Dict[str, Set[JavaClassMethod]]:
        methods: Dict[str, Set[JavaClassMethod]] = {}
        for nodes in self.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION):
            method = JavaClassMethod(self.tree.subgraph(nodes), nodes[0], self)
            if method.name in methods:
                methods[method.name].add(method)
            else:
                methods[method.name] = {method}
        return methods

    @cached_property
    def fields(self) -> Dict[str, JavaClassField]:
        fields: Dict[str, JavaClassField] = {}
        for nodes in self.subtrees_with_root_type(ASTNodeType.FIELD_DECLARATION):
            field = JavaClassField(self.tree.subgraph(nodes), nodes[0], self)
            fields[field.name] = field
        return fields
