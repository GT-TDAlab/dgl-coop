/*!
 *   Copyright (c) 2022, NVIDIA Corporation
 *   Copyright (c) 2022, GT-TDAlab (Muhammed Fatih Balin & Umit V. Catalyurek)  
 *   All rights reserved.
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * \file array/cuda/labor_sampling.cc
 * \brief labor sampling
 */
#include "./labor_pick.h"

namespace dgl {
namespace aten {
namespace impl {

/////////////////////////////// CSR ///////////////////////////////

template <DGLDeviceType XPU, typename IdxType, typename FloatType>
std::pair<COOMatrix, FloatArray> CSRLaborSampling(CSRMatrix mat, IdArray NIDs, IdArray rows,
                                  int64_t num_samples, FloatArray prob, IdArray random_seed, IdArray cnt, int importance_sampling) {
  return CSRLaborPick<IdxType, FloatType>(mat, NIDs, rows, num_samples, prob, random_seed, cnt, importance_sampling);
}

template std::pair<COOMatrix, FloatArray> CSRLaborSampling<kDGLCPU, int32_t, float>(
    CSRMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);
template std::pair<COOMatrix, FloatArray> CSRLaborSampling<kDGLCPU, int64_t, float>(
    CSRMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);
template std::pair<COOMatrix, FloatArray> CSRLaborSampling<kDGLCPU, int32_t, double>(
    CSRMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);
template std::pair<COOMatrix, FloatArray> CSRLaborSampling<kDGLCPU, int64_t, double>(
    CSRMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);

/////////////////////////////// COO ///////////////////////////////

template <DGLDeviceType XPU, typename IdxType, typename FloatType>
std::pair<COOMatrix, FloatArray> COOLaborSampling(COOMatrix mat, IdArray NIDs, IdArray rows,
                                    int64_t num_samples, FloatArray prob, IdArray random_seed, IdArray cnt, int importance_sampling) {
  return COOLaborPick<IdxType, FloatType>(mat, NIDs, rows, num_samples, prob, random_seed, cnt, importance_sampling);
}

template std::pair<COOMatrix, FloatArray> COOLaborSampling<kDGLCPU, int32_t, float>(
    COOMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);
template std::pair<COOMatrix, FloatArray> COOLaborSampling<kDGLCPU, int64_t, float>(
    COOMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);
template std::pair<COOMatrix, FloatArray> COOLaborSampling<kDGLCPU, int32_t, double>(
    COOMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);
template std::pair<COOMatrix, FloatArray> COOLaborSampling<kDGLCPU, int64_t, double>(
    COOMatrix, IdArray, IdArray, int64_t, FloatArray, IdArray, IdArray, int);

}  // namespace impl
}  // namespace aten
}  // namespace dgl
