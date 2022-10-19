
import unittest

import numpy as np

from onnxscript import script, graph
from onnxscript.onnx_opset import opset17 as op
from onnxscript.onnx_types import FLOAT
from onnxscript.ort_evaluator import ort_evaluator


class EvaluatorTest(unittest.TestCase):
    def test_mixed_evaluator(self):
        @script()
        def seq_map (x : FLOAT['N']):
            seq1 = op.SequenceConstruct(x, x+1, x+2)
            @graph()
            def square(y : FLOAT['N']) -> FLOAT['N']:
                return op.Mul(y, y)
            seq2 = op.SequenceMap(seq1, body=square)
            return seq2
        
        x = np.array([0.0, 1.0], dtype=np.float32)
        output = seq_map[ort_evaluator](input)
        expected = [t*t for t in [x, x+1, x+2]]
        np.testing.assert_equal(output, expected)

if __name__ == "__main__":
    unittest.main()