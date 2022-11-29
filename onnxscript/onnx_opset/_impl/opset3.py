# --------------------------------------------------------------------------
# ⚠️ WARNING - AUTO-GENERATED CODE - DO NOT EDIT ⚠️
# ⚙️ Generated by 'python -m opgen'
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
# flake8: noqa
# mypy: disable-error-code=override
# pylint: disable=W0221,W0222,W0237,W0246,R0901
# --------------------------------------------------------------------------

from typing import Callable, Optional, Sequence, Tuple, Union

from onnx.defs import get_schema

from onnxscript.onnx_opset._impl.opset2 import Opset2
from onnxscript.onnx_types import DOUBLE, FLOAT, FLOAT16, INT32
from onnxscript.values import Op, Opset


class Opset3(Opset2):
    def __new__(cls):
        return Opset.__new__(cls, "", 3)

    def __init__(self):
        super().__init__()

    def GRU(
        self,
        X: Union[DOUBLE, FLOAT, FLOAT16],
        W: Union[DOUBLE, FLOAT, FLOAT16],
        R: Union[DOUBLE, FLOAT, FLOAT16],
        B: Optional[Union[DOUBLE, FLOAT, FLOAT16]] = None,
        sequence_lens: Optional[INT32] = None,
        initial_h: Optional[Union[DOUBLE, FLOAT, FLOAT16]] = None,
        activation_alpha: Optional[Sequence[float]] = None,
        activation_beta: Optional[Sequence[float]] = None,
        activations: Optional[Sequence[str]] = None,
        clip: Optional[float] = None,
        direction: str = "forward",
        hidden_size: Optional[int] = None,
        linear_before_reset: int = 0,
        output_sequence: int = 0,
    ) -> Tuple[Union[DOUBLE, FLOAT, FLOAT16], Union[DOUBLE, FLOAT, FLOAT16]]:
        r"""[🌐 GRU(3)](https://onnx.ai/onnx/operators/onnx__GRU.html#gru-3 "Online Documentation")


        Computes an one-layer GRU. This operator is usually supported via some custom
        implementation such as CuDNN.

        Notations:

        `X` - input tensor

        `z` - update gate

        `r` - reset gate

        `h` - hidden gate

        `t` - time step (t-1 means previous time step)

        `W[zrh]` - W parameter weight matrix for update, reset, and hidden gates

        `R[zrh]` - R recurrence weight matrix for update, reset, and hidden gates

        `Wb[zrh]` - W bias vectors for update, reset, and hidden gates

        `Rb[zrh]` - R bias vectors for update, reset, and hidden gates

        `WB[zrh]` - W parameter weight matrix for backward update, reset, and hidden gates

        `RB[zrh]` - R recurrence weight matrix for backward update, reset, and hidden gates

        `WBb[zrh]` - W bias vectors for backward update, reset, and hidden gates

        `RBb[zrh]` - R bias vectors for backward update, reset, and hidden gates

        `H` - Hidden state

        `num_directions` - 2 if direction == bidirectional else 1

        Activation functions:

          Relu(x)                - max(0, x)

          Tanh(x)                - (1 - e^{-2x})/(1 + e^{-2x})

          Sigmoid(x)             - 1/(1 + e^{-x})

          (NOTE: Below are optional)

          Affine(x)              - alpha*x + beta

          LeakyRelu(x)           - x if x >= 0 else alpha * x

          ThresholdedRelu(x)     - x if x >= alpha else 0

          ScaledTanh(x)          - alpha*Tanh(beta*x)

          HardSigmoid(x)         - min(max(alpha*x + beta, 0), 1)

          Elu(x)                 - x if x >= 0 else alpha*(e^x - 1)

          Softsign(x)            - x/(1 + |x|)

          Softplus(x)            - log(1 + e^x)

        Equations (Default: f=Sigmoid, g=Tanh):

          - zt = f(Xt*(Wz^T) + Ht-1*Rz + Wbz + Rbz)

          - rt = f(Xt*(Wr^T) + Ht-1*Rr + Wbr + Rbr)

          - ht = g(Xt*(Wh^T) + (rt (.) Ht-1)*Rh + Rbh + Wbh) # default, when linear_before_reset = 0

          - ht = g(Xt*(Wh^T) + (rt (.) (Ht-1*Rh + Rbh) + Wbh) # when linear_before_reset != 0

          - Ht = (1 - zt) (.) ht + zt (.) Ht-1


        Args:
            X: The input sequences packed (and potentially padded) into one 3-D tensor
                with the shape of `[seq_length, batch_size, input_size]`.

            W: The weight tensor for the gates. Concatenation of `W[zrh]` and `WB[zrh]`
                (if bidirectional) along dimension 0. This tensor has shape
                `[num_directions, 3*hidden_size, input_size]`.

            R: The recurrence weight tensor. Concatenation of `R[zrh]` and `RB[zrh]` (if
                bidirectional) along dimension 0. This tensor has shape
                `[num_directions, 3*hidden_size, hidden_size]`.

            B: (optional) The bias tensor for the gates. Concatenation of `[Wb[zrh],
                Rb[zrh]]` and `[WBb[zrh], RBb[zrh]]` (if bidirectional) along dimension
                0. This tensor has shape `[num_directions, 6*hidden_size]`. Optional: If
                not specified - assumed to be 0

            sequence_lens: (optional) Optional tensor specifying lengths of the
                sequences in a batch. If not specified - assumed all sequences in the
                batch to have length `seq_length`. It has shape `[batch_size]`.

            initial_h: (optional) Optional initial value of the hidden. If not specified
                - assumed to be 0. It has shape `[num_directions, batch_size,
                hidden_size]`.

            activation_alpha: Optional scaling values used by some activation functions.
                The values are consumed in the order of activation functions, for
                example (f, g, h) in LSTM. Default values are the same as of
                corresponding ONNX operators.For example with LeakyRelu, the default
                alpha is 0.01.

            activation_beta: Optional scaling values used by some activation functions.
                The values are consumed in the order of activation functions, for
                example (f, g, h) in LSTM. Default values are the same as of
                corresponding ONNX operators.

            activations: A list of 2 (or 4 if bidirectional) activation functions for
                update, reset, and hidden gates. The activation functions must be one of
                the activation functions specified above. Optional: See the equations
                for default if not specified.

            clip: Cell clip threshold. Clipping bounds the elements of a tensor in the
                range of [-threshold, +threshold] and is applied to the input of
                activations. No clip if not specified.

            direction: Specify if the RNN is forward, reverse, or bidirectional. Must be
                one of forward (default), reverse, or bidirectional.

            hidden_size: Number of neurons in the hidden layer

            linear_before_reset: When computing the output of the hidden gate, apply the
                linear transformation before multiplying by the output of the reset
                gate.

            output_sequence: The sequence output for the hidden is optional if 0.
                Default 0.
        """

        schema = get_schema("GRU", 3, "")
        op: Callable[
            ..., Tuple[Union[DOUBLE, FLOAT, FLOAT16], Union[DOUBLE, FLOAT, FLOAT16]]
        ] = Op(self, "GRU", schema)
        return op(
            *self._prepare_inputs(schema, X, W, R, B, sequence_lens, initial_h),
            activation_alpha=activation_alpha,
            activation_beta=activation_beta,
            activations=activations,
            clip=clip,
            direction=direction,
            hidden_size=hidden_size,
            linear_before_reset=linear_before_reset,
            output_sequence=output_sequence,
        )
