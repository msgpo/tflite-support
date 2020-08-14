/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef THIRD_PARTY_TENSORFLOW_LITE_SUPPORT_CUSTOM_OPS_KERNEL_SENTENCEPIECE_MODEL_CONVERTER_H_
#define THIRD_PARTY_TENSORFLOW_LITE_SUPPORT_CUSTOM_OPS_KERNEL_SENTENCEPIECE_MODEL_CONVERTER_H_
#include <string>

#include "absl/status/status.h"

namespace tflite {
namespace support {
namespace ops {
// Converts Sentencepiece configuration to flatbuffer format.
// encoding_offset is used by some encoders that combine different encodings.
std::pair<absl::Status, std::string> ConvertSentencepieceModelToFlatBuffer(
    const std::string& model_config_str, int encoding_offset = 0);

// The functions that are provided for the Python wrapper.
std::string ConvertSentencepieceModel(const std::string& model_string);

// Returns size of a vocabulary from Sentencepiece configuration in flatbuffer
// format.
int GetVocabularySize(const std::string& model_string);
}  // namespace ops
}  // namespace support
}  // namespace tflite

#endif  // THIRD_PARTY_TENSORFLOW_LITE_SUPPORT_CUSTOM_OPS_KERNEL_SENTENCEPIECE_MODEL_CONVERTER_H_
