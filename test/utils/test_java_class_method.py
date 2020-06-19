# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from unittest import TestCase
from pathlib import Path

from aibolit.utils.java_package import JavaPackage


class JavaClassMethodTestCase(TestCase):
    def test_method_name(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'TwoClasses.java')
        java_class = java_package.java_classes['Second']
        self.assertEqual(java_class.methods.keys(), {'Decrement', 'Increment'})

    def test_used_methods(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'MethodUseOtherMethodExample.java')
        java_class = java_package.java_classes['MethodUseOtherMethod']
        for method_name, method in java_class.methods.items():
            with self.subTest(f'Method: {method_name}'):
                self.assertEqual(JavaClassMethodTestCase._used_methods_by_name[method.name],
                                 method.used_methods.keys())

    _used_methods_by_name = {
        'useOnlyMethods1': {'useOnlyMethods2'},
        'useOnlyMethods2': {'useOnlyMethods1'},
        'getField': {},
        'setField': {},
        'standAloneMethod': {},
    }
