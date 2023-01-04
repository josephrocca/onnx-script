# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: onnx.in.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


class Version(betterproto.Enum):
    """
    Versioning ONNX versioning is specified in docs/IR.md and elaborated on in
    docs/Versioning.md To be compatible with both proto2 and proto3, we will
    use a version number that is not defined by the default value but an
    explicit enum number.
    """

    # proto3 requires the first enum value to be zero. We add this just to
    # appease the compiler.
    _START_VERSION = 0
    # The version field is always serialized and we will use it to store the
    # version that the  graph is generated from. This helps us set up version
    # control. For the IR, we are using simple numbers starting with 0x00000001,
    # which was the version we published on Oct 10, 2017.
    IR_VERSION_2017_10_10 = 1
    # IR_VERSION 2 published on Oct 30, 2017 - Added type discriminator to
    # AttributeProto to support proto3 users
    IR_VERSION_2017_10_30 = 2
    # IR VERSION 3 published on Nov 3, 2017 - For operator versioning:    - Added
    # new message OperatorSetIdProto    - Added opset_import in ModelProto - For
    # vendor extensions, added domain in NodeProto
    IR_VERSION_2017_11_3 = 3
    # IR VERSION 4 published on Jan 22, 2019 - Relax constraint that initializers
    # should be a subset of graph inputs - Add type BFLOAT16
    IR_VERSION_2019_1_22 = 4
    # IR VERSION 5 published on March 18, 2019 - Add message TensorAnnotation. -
    # Add quantization annotation in GraphProto to map tensor with its scale and
    # zero point quantization parameters.
    IR_VERSION_2019_3_18 = 5
    # IR VERSION 6 published on Sep 19, 2019 - Add support for sparse tensor
    # constants stored in model.   - Add message SparseTensorProto   - Add sparse
    # initializers
    IR_VERSION_2019_9_19 = 6
    # IR VERSION 7 published on May 8, 2020 - Add support to allow function body
    # graph to rely on multiple external opreator sets. - Add a list to promote
    # inference graph's initializers to global and   mutable variables. Global
    # variables are visible in all graphs of the   stored models. - Add message
    # TrainingInfoProto to store initialization   method and training algorithm.
    # The execution of TrainingInfoProto   can modify the values of mutable
    # variables. - Implicitly add inference graph into each TrainingInfoProto's
    # algorithm.
    IR_VERSION_2020_5_8 = 7
    # IR VERSION 8 published on <TBD> Introduce TypeProto.SparseTensor Introduce
    # TypeProto.Optional Added a list of FunctionProtos local to the model
    # Deprecated since_version and operator status from FunctionProto
    IR_VERSION = 8


class OperatorStatus(betterproto.Enum):
    """Operator/function status."""

    EXPERIMENTAL = 0
    STABLE = 1


class AttributeProtoAttributeType(betterproto.Enum):
    UNDEFINED = 0
    FLOAT = 1
    INT = 2
    STRING = 3
    TENSOR = 4
    GRAPH = 5
    SPARSE_TENSOR = 11
    TYPE_PROTO = 13
    FLOATS = 6
    INTS = 7
    STRINGS = 8
    TENSORS = 9
    GRAPHS = 10
    SPARSE_TENSORS = 12
    TYPE_PROTOS = 14


class TensorProtoDataType(betterproto.Enum):
    UNDEFINED = 0
    FLOAT = 1
    UINT8 = 2
    INT8 = 3
    UINT16 = 4
    INT16 = 5
    INT32 = 6
    INT64 = 7
    STRING = 8
    BOOL = 9
    FLOAT16 = 10
    DOUBLE = 11
    UINT32 = 12
    UINT64 = 13
    COMPLEX64 = 14
    COMPLEX128 = 15
    BFLOAT16 = 16


class TensorProtoDataLocation(betterproto.Enum):
    DEFAULT = 0
    EXTERNAL = 1


@dataclass
class AttributeProto(betterproto.Message):
    """
    Attributes A named attribute containing either singular float, integer,
    string, graph, and tensor values, or repeated float, integer, string,
    graph, and tensor values. An AttributeProto MUST contain the name field,
    and *only one* of the following content fields, effectively enforcing a
    C/C++ union equivalent.
    """

    # The name field MUST be present for this version of the IR.
    name: str = betterproto.string_field(1)
    # if ref_attr_name is not empty, ref_attr_name is the attribute name in
    # parent function. In this case, this AttributeProto does not contain data,
    # and it's a reference of attribute in parent scope. NOTE: This should ONLY
    # be used in function (sub-graph). It's invalid to be used in main graph.
    ref_attr_name: str = betterproto.string_field(21)
    # A human-readable documentation for this attribute. Markdown is allowed.
    doc_string: str = betterproto.string_field(13)
    # The type field MUST be present for this version of the IR. For 0.0.1
    # versions of the IR, this field was not defined, and implementations needed
    # to use has_field heuristics to determine which value field was in use.  For
    # IR_VERSION 0.0.2 or later, this field MUST be set and match the f|i|s|t|...
    # field in use.  This change was made to accommodate proto3 implementations.
    type: "AttributeProtoAttributeType" = betterproto.enum_field(20)
    # Exactly ONE of the following fields must be present for this version of the
    # IR
    f: float = betterproto.float_field(2)
    i: int = betterproto.int64_field(3)
    s: bytes = betterproto.bytes_field(4)
    t: "TensorProto" = betterproto.message_field(5)
    g: "GraphProto" = betterproto.message_field(6)
    sparse_tensor: "SparseTensorProto" = betterproto.message_field(22)
    # Do not use field below, it's deprecated. optional ValueProto v = 12;
    # // value - subsumes everything but graph
    tp: "TypeProto" = betterproto.message_field(14)
    floats: List[float] = betterproto.float_field(7)
    ints: List[int] = betterproto.int64_field(8)
    strings: List[bytes] = betterproto.bytes_field(9)
    tensors: List["TensorProto"] = betterproto.message_field(10)
    graphs: List["GraphProto"] = betterproto.message_field(11)
    sparse_tensors: List["SparseTensorProto"] = betterproto.message_field(23)
    type_protos: List["TypeProto"] = betterproto.message_field(15)


@dataclass
class ValueInfoProto(betterproto.Message):
    """
    Defines information on value, including the name, the type, and the shape
    of the value.
    """

    # This field MUST be present in this version of the IR.
    name: str = betterproto.string_field(1)
    # This field MUST be present in this version of the IR for inputs and outputs
    # of the top-level graph.
    type: "TypeProto" = betterproto.message_field(2)
    # A human-readable documentation for this value. Markdown is allowed.
    doc_string: str = betterproto.string_field(3)


@dataclass
class NodeProto(betterproto.Message):
    """
    Nodes Computation graphs are made up of a DAG of nodes, which represent
    what is commonly called a "layer" or "pipeline stage" in machine learning
    frameworks. For example, it can be a node of type "Conv" that takes in an
    image, a filter tensor and a bias tensor, and produces the convolved
    output.
    """

    input: List[str] = betterproto.string_field(1)
    output: List[str] = betterproto.string_field(2)
    # An optional identifier for this node in a graph. This field MAY be absent
    # in ths version of the IR.
    name: str = betterproto.string_field(3)
    # The symbolic identifier of the Operator to execute.
    op_type: str = betterproto.string_field(4)
    # The domain of the OperatorSet that specifies the operator named by op_type.
    domain: str = betterproto.string_field(7)
    # Additional named attributes.
    attribute: List["AttributeProto"] = betterproto.message_field(5)
    # A human-readable documentation for this node. Markdown is allowed.
    doc_string: str = betterproto.string_field(6)


@dataclass
class TrainingInfoProto(betterproto.Message):
    """
    Training information TrainingInfoProto stores information for training a
    model. In particular, this defines two functionalities: an initialization-
    step and a training-algorithm-step. Initialization resets the model back to
    its original state as if no training has been performed. Training algorithm
    improves the model based on input data. The semantics of the
    initialization-step is that the initializers in ModelProto.graph and in
    TrainingInfoProto.algorithm are first initialized as specified by the
    initializers in the graph, and then updated by the "initialization_binding"
    in every instance in ModelProto.training_info. The field "algorithm"
    defines a computation graph which represents a training algorithm's step.
    After the execution of a TrainingInfoProto.algorithm, the initializers
    specified by "update_binding" may be immediately updated. If the targeted
    training algorithm contains consecutive update steps (such as block
    coordinate descent methods), the user needs to create a TrainingInfoProto
    for each step.
    """

    # This field describes a graph to compute the initial tensors upon starting
    # the training process. Initialization graph has no input and can have
    # multiple outputs. Usually, trainable tensors in neural networks are
    # randomly initialized. To achieve that, for each tensor, the user can put a
    # random number operator such as RandomNormal or RandomUniform in
    # TrainingInfoProto.initialization.node and assign its random output to the
    # specific tensor using "initialization_binding". This graph can also set the
    # initializers in "algorithm" in the same TrainingInfoProto; a use case is
    # resetting the number of training iteration to zero. By default, this field
    # is an empty graph and its evaluation does not produce any output. Thus, no
    # initializer would be changed by default.
    initialization: "GraphProto" = betterproto.message_field(1)
    # This field represents a training algorithm step. Given required inputs, it
    # computes outputs to update initializers in its own or inference graph's
    # initializer lists. In general, this field contains loss node, gradient
    # node, optimizer node, increment of iteration count. An execution of the
    # training algorithm step is performed by executing the graph obtained by
    # combining the inference graph (namely "ModelProto.graph") and the
    # "algorithm" graph. That is, the actual the actual
    # input/initializer/output/node/value_info/sparse_initializer list of the
    # training graph is the concatenation of "ModelProto.graph.input/initializer/
    # output/node/value_info/sparse_initializer" and
    # "algorithm.input/initializer/output/node/value_info/sparse_initializer" in
    # that order. This combined graph must satisfy the normal ONNX conditions.
    # Now, let's provide a visualization of graph combination for clarity. Let
    # the inference graph (i.e., "ModelProto.graph") be    tensor_a, tensor_b ->
    # MatMul -> tensor_c -> Sigmoid -> tensor_d and the "algorithm" graph be
    # tensor_d -> Add -> tensor_e The combination process results    tensor_a,
    # tensor_b -> MatMul -> tensor_c -> Sigmoid -> tensor_d -> Add -> tensor_e
    # Notice that an input of a node in the "algorithm" graph may reference the
    # output of a node in the inference graph (but not the other way round).
    # Also, inference node cannot reference inputs of "algorithm". With these
    # restrictions, inference graph can always be run independently without
    # training information. By default, this field is an empty graph and its
    # evaluation does not produce any output. Evaluating the default training
    # step never update any initializers.
    algorithm: "GraphProto" = betterproto.message_field(2)
    # This field specifies the bindings from the outputs of "initialization" to
    # some initializers in "ModelProto.graph.initializer" and the
    # "algorithm.initializer" in the same TrainingInfoProto. See "update_binding"
    # below for details. By default, this field is empty and no initializer would
    # be changed by the execution of "initialization".
    initialization_binding: List["StringStringEntryProto"] = betterproto.message_field(
        3
    )
    # Gradient-based training is usually an iterative procedure. In one gradient
    # descent iteration, we apply x = x - r * g where "x" is the optimized
    # tensor, "r" stands for learning rate, and "g" is gradient of "x" with
    # respect to a chosen loss. To avoid adding assignments into the training
    # graph, we split the update equation into y = x - r * g x = y The user needs
    # to save "y = x - r * g" into TrainingInfoProto.algorithm. To tell that "y"
    # should be assigned to "x", the field "update_binding" may contain a key-
    # value pair of strings, "x" (key of StringStringEntryProto) and "y" (value
    # of StringStringEntryProto). For a neural network with multiple trainable
    # (mutable) tensors, there can be multiple key-value pairs in
    # "update_binding". The initializers appears as keys in "update_binding" are
    # considered mutable variables. This implies some behaviors as described
    # below.  1. We have only unique keys in all "update_binding"s so that two
    # variables may not have the same name. This ensures that one     variable is
    # assigned up to once.  2. The keys must appear in names of
    # "ModelProto.graph.initializer" or
    # "TrainingInfoProto.algorithm.initializer".  3. The values must be output
    # names of "algorithm" or "ModelProto.graph.output".  4. Mutable variables
    # are initialized to the value specified by the     corresponding
    # initializer, and then potentially updated by     "initializer_binding"s and
    # "update_binding"s in "TrainingInfoProto"s. This field usually contains
    # names of trainable tensors (in ModelProto.graph), optimizer states such as
    # momentums in advanced stochastic gradient methods (in
    # TrainingInfoProto.graph), and number of training iterations (in
    # TrainingInfoProto.graph). By default, this field is empty and no
    # initializer would be changed by the execution of "algorithm".
    update_binding: List["StringStringEntryProto"] = betterproto.message_field(4)


@dataclass
class ModelProto(betterproto.Message):
    """
    Models ModelProto is a top-level file/container format for bundling a ML
    model and associating its computation graph with metadata. The semantics of
    the model are described by the associated GraphProto's.
    """

    # The version of the IR this model targets. See Version enum above. This
    # field MUST be present.
    ir_version: int = betterproto.int64_field(1)
    # The OperatorSets this model relies on. All ModelProtos MUST have at least
    # one entry that specifies which version of the ONNX OperatorSet is being
    # imported. All nodes in the ModelProto's graph will bind against the
    # operator with the same-domain/same-op_type operator with the HIGHEST
    # version in the referenced operator sets.
    opset_import: List["OperatorSetIdProto"] = betterproto.message_field(8)
    # The name of the framework or tool used to generate this model. This field
    # SHOULD be present to indicate which implementation/tool/framework emitted
    # the model.
    producer_name: str = betterproto.string_field(2)
    # The version of the framework or tool used to generate this model. This
    # field SHOULD be present to indicate which implementation/tool/framework
    # emitted the model.
    producer_version: str = betterproto.string_field(3)
    # Domain name of the model. We use reverse domain names as name space
    # indicators. For example: `com.facebook.fair` or
    # `com.microsoft.cognitiveservices` Together with `model_version` and
    # GraphProto.name, this forms the unique identity of the graph.
    domain: str = betterproto.string_field(4)
    # The version of the graph encoded. See Version enum below.
    model_version: int = betterproto.int64_field(5)
    # A human-readable documentation for this model. Markdown is allowed.
    doc_string: str = betterproto.string_field(6)
    # The parameterized graph that is evaluated to execute the model.
    graph: "GraphProto" = betterproto.message_field(7)
    # Named metadata values; keys should be distinct.
    metadata_props: List["StringStringEntryProto"] = betterproto.message_field(14)
    # Training-specific information. Sequentially executing all stored
    # `TrainingInfoProto.algorithm`s and assigning their outputs following the
    # corresponding `TrainingInfoProto.update_binding`s is one training
    # iteration. Similarly, to initialize the model (as if training hasn't
    # happened), the user should sequentially execute all stored
    # `TrainingInfoProto.initialization`s and assigns their outputs using
    # `TrainingInfoProto.initialization_binding`s. If this field is empty, the
    # training behavior of the model is undefined.
    training_info: List["TrainingInfoProto"] = betterproto.message_field(20)
    # A list of function protos local to the model. Name of the function
    # "FunctionProto.name" should be unique within the domain
    # "FunctionProto.domain". In case of any conflicts the behavior (whether the
    # model local functions are given higher priority, or standard opserator sets
    # are given higher priotity or this is treated as error) is defined by the
    # runtimes. The operator sets imported by FunctionProto should be compatible
    # with the ones imported by ModelProto and other model local FunctionProtos.
    # Example, if same operator set say 'A' is imported by a FunctionProto and
    # ModelProto or by 2 FunctionProtos then versions for the operator set may be
    # different but, the operator schema returned for op_type, domain, version
    # combination for both the versions should be same for every node in the
    # function body. One FunctionProto can reference other FunctionProto in the
    # model, however, recursive reference is not allowed.
    functions: List["FunctionProto"] = betterproto.message_field(25)


@dataclass
class StringStringEntryProto(betterproto.Message):
    """
    StringStringEntryProto follows the pattern for cross-proto-version maps.
    See https://developers.google.com/protocol-buffers/docs/proto3#maps
    """

    key: str = betterproto.string_field(1)
    value: str = betterproto.string_field(2)


@dataclass
class TensorAnnotation(betterproto.Message):
    tensor_name: str = betterproto.string_field(1)
    # <key, value> pairs to annotate tensor specified by <tensor_name> above. The
    # keys used in the mapping below must be pre-defined in ONNX spec. For
    # example, for 8-bit linear quantization case, 'SCALE_TENSOR',
    # 'ZERO_POINT_TENSOR' will be pre-defined as quantization parameter keys.
    quant_parameter_tensor_names: List[
        "StringStringEntryProto"
    ] = betterproto.message_field(2)


@dataclass
class GraphProto(betterproto.Message):
    """
    Graphs A graph defines the computational logic of a model and is comprised
    of a parameterized list of nodes that form a directed acyclic graph based
    on their inputs and outputs. This is the equivalent of the "network" or
    "graph" in many deep learning frameworks.
    """

    # The nodes in the graph, sorted topologically.
    node: List["NodeProto"] = betterproto.message_field(1)
    # The name of the graph.
    name: str = betterproto.string_field(2)
    # A list of named tensor values, used to specify constant inputs of the
    # graph. Each initializer (both TensorProto as well SparseTensorProto) MUST
    # have a name. The name MUST be unique across both initializer and
    # sparse_initializer, but the name MAY also appear in the input list.
    initializer: List["TensorProto"] = betterproto.message_field(5)
    # Initializers (see above) stored in sparse format.
    sparse_initializer: List["SparseTensorProto"] = betterproto.message_field(15)
    # A human-readable documentation for this graph. Markdown is allowed.
    doc_string: str = betterproto.string_field(10)
    # The inputs and outputs of the graph.
    input: List["ValueInfoProto"] = betterproto.message_field(11)
    output: List["ValueInfoProto"] = betterproto.message_field(12)
    # Information for the values in the graph. The ValueInfoProto.name's must be
    # distinct. It is optional for a value to appear in value_info list.
    value_info: List["ValueInfoProto"] = betterproto.message_field(13)
    # This field carries information to indicate the mapping among a tensor and
    # its quantization parameter tensors. For example: For tensor 'a', it may
    # have {'SCALE_TENSOR', 'a_scale'} and {'ZERO_POINT_TENSOR', 'a_zero_point'}
    # annotated, which means, tensor 'a_scale' and tensor 'a_zero_point' are
    # scale and zero point of tensor 'a' in the model.
    quantization_annotation: List["TensorAnnotation"] = betterproto.message_field(14)


@dataclass
class TensorProto(betterproto.Message):
    """Tensors A serialized tensor value."""

    # The shape of the tensor.
    dims: List[int] = betterproto.int64_field(1)
    # The data type of the tensor. This field MUST have a valid
    # TensorProto.DataType value
    data_type: int = betterproto.int32_field(2)
    segment: "TensorProtoSegment" = betterproto.message_field(3)
    # For float and complex64 values Complex64 tensors are encoded as a single
    # array of floats, with the real components appearing in odd numbered
    # positions, and the corresponding imaginary component appearing in the
    # subsequent even numbered position. (e.g., [1.0 + 2.0i, 3.0 + 4.0i] is
    # encoded as [1.0, 2.0 ,3.0 ,4.0] When this field is present, the data_type
    # field MUST be FLOAT or COMPLEX64.
    float_data: List[float] = betterproto.float_field(4)
    # For int32, uint8, int8, uint16, int16, bool, and float16 values float16
    # values must be bit-wise converted to an uint16_t prior to writing to the
    # buffer. When this field is present, the data_type field MUST be INT32,
    # INT16, INT8, UINT16, UINT8, BOOL, FLOAT16 or BFLOAT16
    int32_data: List[int] = betterproto.int32_field(5)
    # For strings. Each element of string_data is a UTF-8 encoded Unicode string.
    # No trailing null, no leading BOM. The protobuf "string" scalar type is not
    # used to match ML community conventions. When this field is present, the
    # data_type field MUST be STRING
    string_data: List[bytes] = betterproto.bytes_field(6)
    # For int64. When this field is present, the data_type field MUST be INT64
    int64_data: List[int] = betterproto.int64_field(7)
    # Optionally, a name for the tensor.
    name: str = betterproto.string_field(8)
    # A human-readable documentation for this tensor. Markdown is allowed.
    doc_string: str = betterproto.string_field(12)
    # Serializations can either use one of the fields above, or use this raw
    # bytes field. The only exception is the string case, where one is required
    # to store the content in the repeated bytes string_data field. When this
    # raw_data field is used to store tensor value, elements MUST be stored in as
    # fixed-width, little-endian order. Floating-point data types MUST be stored
    # in IEEE 754 format. Complex64 elements must be written as two consecutive
    # FLOAT values, real component first. Complex128 elements must be written as
    # two consecutive DOUBLE values, real component first. Boolean type MUST be
    # written one byte per tensor element (00000001 for true, 00000000 for
    # false). Note: the advantage of specific field rather than the raw_data
    # field is that in some cases (e.g. int data), protobuf does a better packing
    # via variable length storage, and may lead to smaller binary footprint. When
    # this field is present, the data_type field MUST NOT be STRING or UNDEFINED
    raw_data: bytes = betterproto.bytes_field(9)
    # Data can be stored inside the protobuf file using type-specific fields or
    # raw_data. Alternatively, raw bytes data can be stored in an external file,
    # using the external_data field. external_data stores key-value pairs
    # describing data location. Recognized keys are: - "location" (required) -
    # POSIX filesystem path relative to the directory where the ONNX
    # protobuf model was stored - "offset" (optional) - position of byte at which
    # stored data begins. Integer stored as string.
    # Offset values SHOULD be multiples 4096 (page size) to enable mmap support.
    # - "length" (optional) - number of bytes containing data. Integer stored as
    # string. - "checksum" (optional) - SHA1 digest of file specified in under
    # 'location' key.
    external_data: List["StringStringEntryProto"] = betterproto.message_field(13)
    # If value not set, data is stored in raw_data (if set) otherwise in type-
    # specified field.
    data_location: "TensorProtoDataLocation" = betterproto.enum_field(14)
    # For double Complex128 tensors are encoded as a single array of doubles,
    # with the real components appearing in odd numbered positions, and the
    # corresponding imaginary component appearing in the subsequent even numbered
    # position. (e.g., [1.0 + 2.0i, 3.0 + 4.0i] is encoded as [1.0, 2.0 ,3.0
    # ,4.0] When this field is present, the data_type field MUST be DOUBLE or
    # COMPLEX128
    double_data: List[float] = betterproto.double_field(10)
    # For uint64 and uint32 values When this field is present, the data_type
    # field MUST be UINT32 or UINT64
    uint64_data: List[int] = betterproto.uint64_field(11)


@dataclass
class TensorProtoSegment(betterproto.Message):
    """
    For very large tensors, we may want to store them in chunks, in which case
    the following fields will specify the segment that is stored in the current
    TensorProto.
    """

    begin: int = betterproto.int64_field(1)
    end: int = betterproto.int64_field(2)


@dataclass
class SparseTensorProto(betterproto.Message):
    """A serialized sparse-tensor value"""

    # The sequence of non-default values are encoded as a tensor of shape [NNZ].
    # The default-value is zero for numeric tensors, and empty-string for string
    # tensors. values must have a non-empty name present which serves as a name
    # for SparseTensorProto when used in sparse_initializer list.
    values: "TensorProto" = betterproto.message_field(1)
    # The indices of the non-default values, which may be stored in one of two
    # formats. (a) Indices can be a tensor of shape [NNZ, rank] with the [i,j]-th
    # value corresponding to the j-th index of the i-th value (in the values
    # tensor). (b) Indices can be a tensor of shape [NNZ], in which case the i-th
    # value must be the linearized-index of the i-th value (in the values
    # tensor). The linearized-index can be converted into an index tuple
    # (k_1,...,k_rank) using the shape provided below. The indices must appear in
    # ascending order without duplication. In the first format, the ordering is
    # lexicographic-ordering: e.g., index-value [1,4] must appear before [2,1]
    indices: "TensorProto" = betterproto.message_field(2)
    # The shape of the underlying dense-tensor: [dim_1, dim_2, ... dim_rank]
    dims: List[int] = betterproto.int64_field(3)


@dataclass
class TensorShapeProto(betterproto.Message):
    """
    Defines a tensor shape. A dimension can be either an integer value or a
    symbolic variable. A symbolic variable represents an unknown dimension.
    """

    dim: List["TensorShapeProtoDimension"] = betterproto.message_field(1)


@dataclass
class TensorShapeProtoDimension(betterproto.Message):
    dim_value: int = betterproto.int64_field(1, group="value")
    dim_param: str = betterproto.string_field(2, group="value")
    # Standard denotation can optionally be used to denote tensor dimensions with
    # standard semantic descriptions to ensure that operations are applied to the
    # correct axis of a tensor. Refer to https://github.com/onnx/onnx/blob/main/d
    # ocs/DimensionDenotation.md#denotation-definition for pre-defined dimension
    # denotations.
    denotation: str = betterproto.string_field(3)


@dataclass
class TypeProto(betterproto.Message):
    """Types The standard ONNX data types."""

    # The type of a tensor.
    tensor_type: "TypeProtoTensor" = betterproto.message_field(1, group="value")
    # The type of a sequence.
    sequence_type: "TypeProtoSequence" = betterproto.message_field(4, group="value")
    # The type of a map.
    map_type: "TypeProtoMap" = betterproto.message_field(5, group="value")
    # The type of an optional.
    optional_type: "TypeProtoOptional" = betterproto.message_field(9, group="value")
    # Type of the sparse tensor
    sparse_tensor_type: "TypeProtoSparseTensor" = betterproto.message_field(
        8, group="value"
    )
    opaque_type: "TypeProtoOpaque" = betterproto.message_field(7, group="value")
    # An optional denotation can be used to denote the whole type with a standard
    # semantic description as to what is stored inside. Refer to
    # https://github.com/onnx/onnx/blob/main/docs/TypeDenotation.md#type-
    # denotation-definition for pre-defined type denotations.
    denotation: str = betterproto.string_field(6)


@dataclass
class TypeProtoTensor(betterproto.Message):
    # This field MUST NOT have the value of UNDEFINED This field MUST have a
    # valid TensorProto.DataType value This field MUST be present for this
    # version of the IR.
    elem_type: int = betterproto.int32_field(1)
    shape: "TensorShapeProto" = betterproto.message_field(2)


@dataclass
class TypeProtoSequence(betterproto.Message):
    """repeated T"""

    # The type and optional shape of each element of the sequence. This field
    # MUST be present for this version of the IR.
    elem_type: "TypeProto" = betterproto.message_field(1)


@dataclass
class TypeProtoMap(betterproto.Message):
    """map<K,V>"""

    # This field MUST have a valid TensorProto.DataType value This field MUST be
    # present for this version of the IR. This field MUST refer to an integral
    # type ([U]INT{8|16|32|64}) or STRING
    key_type: int = betterproto.int32_field(1)
    # This field MUST be present for this version of the IR.
    value_type: "TypeProto" = betterproto.message_field(2)


@dataclass
class TypeProtoOptional(betterproto.Message):
    """wrapper for Tensor, Sequence, or Map"""

    # The type and optional shape of the element wrapped. This field MUST be
    # present for this version of the IR. Possible values correspond to
    # OptionalProto.DataType enum
    elem_type: "TypeProto" = betterproto.message_field(1)


@dataclass
class TypeProtoSparseTensor(betterproto.Message):
    # This field MUST NOT have the value of UNDEFINED This field MUST have a
    # valid TensorProto.DataType value This field MUST be present for this
    # version of the IR.
    elem_type: int = betterproto.int32_field(1)
    shape: "TensorShapeProto" = betterproto.message_field(2)


@dataclass
class TypeProtoOpaque(betterproto.Message):
    # When missing, the domain is the same as the model's.
    domain: str = betterproto.string_field(1)
    # The name is optional but significant when provided.
    name: str = betterproto.string_field(2)


@dataclass
class OperatorSetIdProto(betterproto.Message):
    """
    Operator Sets OperatorSets are uniquely identified by a (domain,
    opset_version) pair.
    """

    # The domain of the operator set being identified. The empty string ("") or
    # absence of this field implies the operator set that is defined as part of
    # the ONNX specification. This field MUST be present in this version of the
    # IR when referring to any other operator set.
    domain: str = betterproto.string_field(1)
    # The version of the operator set being identified. This field MUST be
    # present in this version of the IR.
    version: int = betterproto.int64_field(2)


@dataclass
class FunctionProto(betterproto.Message):
    # The name of the function, similar usage of op_type in OperatorProto.
    # Combined with FunctionProto.domain, this forms the unique identity of the
    # FunctionProto.
    name: str = betterproto.string_field(1)
    # The inputs and outputs of the function.
    input: List[str] = betterproto.string_field(4)
    output: List[str] = betterproto.string_field(5)
    # The attributes of the function.
    attribute: List[str] = betterproto.string_field(6)
    # The nodes in the function.
    node: List["NodeProto"] = betterproto.message_field(7)
    # A human-readable documentation for this function. Markdown is allowed.
    doc_string: str = betterproto.string_field(8)
    opset_import: List["OperatorSetIdProto"] = betterproto.message_field(9)
    # The domain which this function belongs to. Combined with
    # FunctionProto.name, this forms the unique identity of the FunctionProto.
    domain: str = betterproto.string_field(10)
