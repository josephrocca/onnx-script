"""Test op correctness by comparing with PyTorch results."""
from __future__ import annotations

import copy
import dataclasses
import unittest
from typing import Any, Callable, Collection, Iterable, Optional, Sequence, TypeVar

import numpy as np
import onnx
import onnxruntime.capi.onnxruntime_pybind11_state
import torch
from torch.testing._internal import common_device_type, common_methods_invocations
from torch.testing._internal.opinfo import core as opinfo_core

import onnxscript
from onnxscript.function_libs.torch_aten.ops import core as core_ops
from onnxscript.function_libs.torch_aten.ops import nn as nn_ops

T = TypeVar("T")

# Test only float32 inputs. All dtypes will be tested on the generated symbolic functions.
TESTED_DTYPES = (torch.float32,)

# Convenience tuples for creating dtype lists when skipping or xfailing tests

BOOL_TYPES = (torch.bool,)

INT_TYPES = (
    torch.int8,
    torch.int16,
    torch.int32,
    torch.int64,
    torch.uint8,
)

FLOAT_TYPES = (
    torch.float16,
    torch.float32,
    torch.float64,
)


def dtypes_except(*dtypes: torch.dtype) -> Sequence[torch.dtype]:
    """Returns all dtypes except the ones specified."""
    return tuple(dtype for dtype in TESTED_DTYPES if dtype not in dtypes)


@dataclasses.dataclass
class DecorateMeta:
    """A dataclass for storing information about a test case to skip or xfail.

    Adapted from functorch: functorch/test/common_utils.py
    """

    op_name: str
    variant_name: str
    decorator: Callable[..., Any]
    dtypes: Optional[Collection[torch.dtype]]
    reason: str
    matcher: Optional[Callable[[Any], bool]] = None


def xfail(
    op_name: str,
    variant_name: str = "",
    *,
    reason: str,
    dtypes: Optional[Collection[torch.dtype]] = None,
) -> DecorateMeta:
    """Expects an OpInfo test to fail.

    Args:
        op_name: The name of the operator.
        variant_name: Optional OpInfo variant_test_name.
        dtypes: The dtypes to expect the failure.
        reason: The reason for the failure.
    """
    return DecorateMeta(
        op_name=op_name,
        variant_name=variant_name,
        decorator=unittest.expectedFailure,
        dtypes=dtypes,
        reason=reason,
    )


def skip(
    op_name: str,
    variant_name: str = "",
    *,
    reason: str,
    dtypes: Optional[Collection[torch.dtype]] = None,
    matcher: Optional[Callable[[Any], Any]] = None,
) -> DecorateMeta:
    """Skips an OpInfo test.

    Args:
        op_name: The name of the operator.
        variant_name: Optional OpInfo variant_test_name.
        dtypes: The dtypes to skip.
        reason: The reason for skipping.
        matcher: A function that matches the test sample input. It is used only when
            xfail is in the SKIP_SUBTESTS list.
    """
    return DecorateMeta(
        op_name=op_name,
        variant_name=variant_name,
        decorator=unittest.skip(f"Skip: {reason}"),
        dtypes=dtypes,
        reason=reason,
        matcher=matcher,
    )


def add_decorate_info(
    all_opinfos: Sequence[opinfo_core.OpInfo],
    test_class_name: str,
    base_test_name: str,
    skip_or_xfails: Iterable[DecorateMeta],
) -> Callable[[T], T]:
    """Decorates OpInfo tests with decorators based on the skip_or_xfails list."""
    ops_mapping = {(info.name, info.variant_test_name): info for info in all_opinfos}
    for decorate_meta in skip_or_xfails:
        opinfo = ops_mapping.get((decorate_meta.op_name, decorate_meta.variant_name))
        assert (
            opinfo is not None
        ), f"Couldn't find OpInfo for {decorate_meta}. Did you need to specify variant_name?"
        decorators = list(opinfo.decorators)
        new_decorator = opinfo_core.DecorateInfo(
            decorate_meta.decorator,
            test_class_name,
            base_test_name,
            dtypes=decorate_meta.dtypes,
        )
        decorators.append(new_decorator)
        opinfo.decorators = tuple(decorators)

    # This decorator doesn't modify fn in any way
    def wrapped(fn):
        return fn

    return wrapped


# Modify this section ##########################################################

# Ops to be tested for numerical consistency between onnx and pytorch
# Find the names of the OpInfos in torch/testing/_internal/common_methods_invocations.py
OPINFO_FUNCTION_MAPPING: dict[str, onnxscript.OnnxFunction] = {
    "abs": core_ops.aten_abs,
    "acos": core_ops.aten_acos,
    "acosh": core_ops.aten_acosh,
    "add": core_ops.aten_add,
    "addmm": core_ops.aten_addmm,
    "asin": core_ops.aten_asin,
    "asinh": core_ops.aten_asinh,
    "atan": core_ops.aten_atan,
    "atanh": core_ops.aten_atanh,
    "bmm": core_ops.aten_bmm,
    "ceil": core_ops.aten_ceil,
    "clamp_max": core_ops.aten_clamp_max,
    "clamp_min": core_ops.aten_clamp_min,
    "clamp": core_ops.aten_clamp,
    "cos": core_ops.aten_cos,
    "cosh": core_ops.aten_cosh,
    "dot": core_ops.aten_dot,
    "erf": core_ops.aten_erf,
    "exp": core_ops.aten_exp,
    "exp2": core_ops.aten_exp2,
    "fmod": core_ops.aten_fmod,
    "gt": core_ops.aten_gt,
    "isinf": core_ops.aten_isinf,
    "lt": core_ops.aten_lt,
    "matmul": core_ops.aten_matmul,
    "mm": core_ops.aten_mm,
    "mul": core_ops.aten_mul,
    "ne": core_ops.aten_ne,
    "neg": core_ops.aten_neg,
    "nn.functional.elu": nn_ops.aten_elu,
    "nn.functional.leaky_relu": nn_ops.aten_leaky_relu,
    "nn.functional.linear": nn_ops.aten_linear,
    "nn.functional.relu": nn_ops.aten_relu,
    "nn.functional.relu6": nn_ops.aten_relu6,
    "nn.functional.selu": core_ops.aten_selu,
    "nonzero": core_ops.aten_nonzero,
    "ones_like": core_ops.aten_ones_like,
    "ones": core_ops.aten_ones,
    "reciprocal": core_ops.aten_reciprocal,
    "remainder": core_ops.aten_remainder,
    "repeat": core_ops.aten_repeat,
    "round": core_ops.aten_round,
    "rsqrt": core_ops.aten_rsqrt,
    "sigmoid": core_ops.aten_sigmoid,
    "sign": core_ops.aten_sign,
    "sin": core_ops.aten_sin,
    "sinh": core_ops.aten_sinh,
    "sqrt": core_ops.aten_sqrt,
    "sub": core_ops.aten_sub,
    "t": core_ops.aten_t,
    "tan": core_ops.aten_tan,
    "tanh": core_ops.aten_tanh,
    # "transpose": core_ops.aten_transpose,  # TODO(justinchuby): Enable when onnxscript errors are fixed,
    "unsqueeze": core_ops.aten_unsqueeze,
    "zeros": core_ops.aten_zeros,
    "zeros_like": core_ops.aten_zeros_like,
}

TESTED_OPS = frozenset(OPINFO_FUNCTION_MAPPING)

EXPECTED_SKIPS_OR_FAILS = (
    skip("clamp", reason="Enable when onnxscript errors are fixed"),
    xfail(
        "nn.functional.linear",
        reason="ONNX Runtime thinks the graph is invalid",
    ),
    xfail("round", variant_name="decimals_0", reason="The op does not support decimals"),
    xfail("round", variant_name="decimals_3", reason="The op does not support decimals"),
    xfail("round", variant_name="decimals_neg_3", reason="The op does not support decimals"),
    xfail("transpose", reason="Enable when onnxscript errors are fixed"),
)


SKIP_SUBTESTS: tuple[DecorateMeta, ...] = (
    skip(
        "nonzero",
        matcher=lambda sample: sample.kwargs.get("as_tuple") is True,
        reason="as_tuple=True is not supported",
    ),
)
OP_WITH_SKIPPED_SUBTESTS = frozenset(meta.op_name for meta in SKIP_SUBTESTS)

# END OF SECTION TO MODIFY #####################################################


OPS_DB = copy.deepcopy(common_methods_invocations.op_db)

ALL_OPS_IN_DB = frozenset(op_info.name for op_info in OPS_DB)
# Assert all ops in OPINFO_FUNCTION_MAPPING are in the OPS_DB
assert TESTED_OPS.issubset(ALL_OPS_IN_DB), f"{TESTED_OPS - ALL_OPS_IN_DB} not in OPS_DB"


TORCH_TYPE_TO_ONNX = {
    torch.bool: onnx.TensorProto.BOOL,
    torch.uint8: onnx.TensorProto.UINT8,
    torch.int8: onnx.TensorProto.INT8,
    torch.int16: onnx.TensorProto.INT16,
    torch.int32: onnx.TensorProto.INT32,
    torch.int64: onnx.TensorProto.INT64,
    torch.float16: onnx.TensorProto.FLOAT16,
    torch.float32: onnx.TensorProto.FLOAT,
    torch.float64: onnx.TensorProto.DOUBLE,
    torch.complex64: onnx.TensorProto.COMPLEX64,
    torch.complex128: onnx.TensorProto.COMPLEX128,
    torch.bfloat16: onnx.TensorProto.BFLOAT16,
}


def _convert_tensor_to_numpy(input: Any) -> Any:
    if isinstance(input, torch.Tensor):
        return input.detach().cpu().numpy()
    if isinstance(input, (tuple, list)):
        if len(input) == 0:
            return np.array((), dtype=np.int64)
        if isinstance(input[0], torch.Tensor):
            return [_convert_tensor_to_numpy(x) for x in input]
        if isinstance(input[0], (int, float)):
            # Just a tuple of numbers
            return np.array(input)
        return input

    return input


def _convert_kwargs_for_onnx(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Converts kwargs to be compatible with ONNX Runtime.

    ONNX Runtime doesn't support torch.bool, so we convert them to torch.uint8.
    """
    new_kwargs = {}
    for key, value in kwargs.items():
        if key == "device":
            continue
        if key == "dtype":
            value = TORCH_TYPE_TO_ONNX[value]
        new_kwargs[key] = value
    return new_kwargs


def _should_skip_test_sample(op_name: str, sample) -> Optional[str]:
    """Returns a reason if a test sample should be skipped."""
    if op_name not in OP_WITH_SKIPPED_SUBTESTS:
        return None
    for decorator_meta in SKIP_SUBTESTS:
        # Linear search on SKIP_SUBTESTS. That's fine because the list is small.
        if decorator_meta.op_name == op_name:
            assert decorator_meta.matcher is not None, "Matcher must be defined"
            if decorator_meta.matcher(sample):
                return decorator_meta.reason
    return None


class TestOutputConsistency(unittest.TestCase):
    """Test output consistency between exported ONNX models and PyTorch eager mode.

    This is a parameterized test suite.
    """

    def setUp(self) -> None:
        torch.manual_seed(42)
        np.random.seed(42)

    @common_device_type.ops(  # type: ignore[misc]
        [info for info in OPS_DB if info.name in TESTED_OPS],
        allowed_dtypes=TESTED_DTYPES,
    )
    @add_decorate_info(
        OPS_DB,
        "TestOutputConsistency",
        "test_output_match",
        skip_or_xfails=EXPECTED_SKIPS_OR_FAILS,
    )
    def test_output_match(self, device: str, dtype: torch.dtype, op):
        """Base test method for testing each opset, used by instantiate_device_type_tests."""
        # device is provided by instantiate_device_type_tests, but we only want to run in cpu.
        assert device == "cpu"

        samples = op.sample_inputs(
            device,
            dtype,
            requires_grad=False,
        )

        onnx_function = OPINFO_FUNCTION_MAPPING[op.name]

        for (i, cpu_sample) in enumerate(samples):
            inputs = (cpu_sample.input, *cpu_sample.args)
            # Provide the repr to subtest because tensors are not serializable in parallel test runs
            with self.subTest(
                sample_num=i,
                inputs=repr(inputs),
                kwargs=repr(cpu_sample.kwargs),
            ):
                skip_reason = _should_skip_test_sample(op.name, cpu_sample)
                if skip_reason is not None:
                    self.skipTest(skip_reason)
                input_onnx = [_convert_tensor_to_numpy(x) for x in inputs]
                kwargs_onnx = _convert_kwargs_for_onnx(cpu_sample.kwargs)
                output_torch = op(*inputs, **cpu_sample.kwargs)
                try:
                    function_output = onnx_function(*input_onnx, **kwargs_onnx)
                # pylint: disable=c-extension-no-member
                except onnxruntime.capi.onnxruntime_pybind11_state.NotImplemented:
                    self.skipTest(
                        f"ONNX Runtime doesn't support running {op.name} with dtype {dtype}",
                    )
                # pylint: enable=c-extension-no-member

                if dtype == torch.float32:
                    # Relax atol and rtol for float32 based on empirical results
                    # The current most relaxed values are for aten::matmul
                    rtol = 3.7e-6
                    atol = 1.8e-5
                else:
                    rtol = None
                    atol = None

                # Use torch testing to ensure dtypes and shapes match
                torch.testing.assert_close(
                    torch.tensor(function_output),
                    output_torch,
                    rtol=rtol,
                    atol=atol,
                )


common_device_type.instantiate_device_type_tests(
    TestOutputConsistency, globals(), only_for="cpu"
)


if __name__ == "__main__":
    unittest.main()
