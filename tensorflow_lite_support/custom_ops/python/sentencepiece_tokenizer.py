# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Lint as: python3
"""Python class that implements Sentencepiece tokenizer.

It follows TF.text designers design.

"""
import tensorflow.compat.v2 as tf  # pylint: disable=g-direct-tensorflow-import
from third_party.tensorflow.python.ops.ragged import ragged_tensor  # pylint: disable=g-direct-tensorflow-import
from tensorflow_lite_support.custom_ops.kernel.sentencepiece import gen_sentencepiece_tokenizer_op
from tensorflow_lite_support.custom_ops.kernel.sentencepiece.py import model_converter


class SentencepieceTokenizer:
  """Sentencepiece tokenizer with tf.text interface."""

  def __init__(self, model, reverse=False, add_bos=False, add_eos=False):
    converted_model = model_converter.convert_sentencepiece_model(model)
    # Use uint8 tensor as a buffer for the model to avoid any possible changes,
    # for example truncation by '\0'.
    self._converted_model = tf.constant(list(converted_model), dtype=tf.uint8)
    self._vocab_size = model_converter.get_vocabulary_size(converted_model)
    self._reverse = reverse
    self._add_bos = add_bos
    self._add_eos = add_eos

  def tokenize(self, inputs):
    """The main tokenization function."""
    input_tensor = ragged_tensor.convert_to_tensor_or_ragged_tensor(inputs)
    if input_tensor.shape.ndims is None:
      raise ValueError("Rank of input_tensor must be statically known.")
    if ragged_tensor.is_ragged(input_tensor):
      # Ensure that input has row_split_dtype is int32
      input_tensor = input_tensor.with_row_splits_dtype(tf.int32)
      # Recursively process the values of the ragged tensor.
      tokens = self.tokenize(input_tensor.flat_values)
      return input_tensor.with_flat_values(tokens)
    else:
      if input_tensor.shape.ndims > 1:
        # Convert the input tensor to ragged and process it.
        return self.tokenize(
            tf.RaggedTensor.from_tensor(
                input_tensor, row_splits_dtype=tf.int32))
      elif input_tensor.shape.ndims == 0:
        tokens = self.tokenize(tf.stack([input_tensor]))
        return tokens.values
      else:
        # Our rank 1 tensor is the correct shape, so we can process it as
        # normal.
        (output_values, row_splits) = (
            gen_sentencepiece_tokenizer_op.tf_sentencepiece_tokenize_op(
                self._converted_model, input_tensor, 0, 0, self._add_bos,
                self._add_eos, self._reverse))
        tokens = tf.RaggedTensor.from_nested_row_splits(
            flat_values=output_values,
            nested_row_splits=[row_splits],
            validate=False)
        return tokens

  def vocab_size(self):
    """Returns size of the vocabulary in Sentencepiece model."""
    return self._vocab_size
