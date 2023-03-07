from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import MC6809


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(MC6809,),
        )
