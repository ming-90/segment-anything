// Copyright (c) Meta Platforms, Inc. and affiliates.
// All rights reserved.

// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.

// Convert the onnx model mask prediction to ImageData
const arrayToImageData = (input,  width, height) => {
  const [r, g, b, a] = [0, 114, 189, 255]; // the masks's blue color
  const arr = new Uint8ClampedArray(4 * width * height).fill(0);
  for (let i = 0; i < input.length; i++) {

    // Threshold the onnx model mask prediction at 0.0
    // This is equivalent to thresholding the mask using predictor.model.mask_threshold
    // in python
    if (input[i] > 0.0) {
      arr[4 * i + 0] = r;
      arr[4 * i + 1] = g;
      arr[4 * i + 2] = b;
      arr[4 * i + 3] = a;
    }
  }
  return new ImageData(arr, height, width);
}

// Use a Canvas element to produce an image from ImageData

// Canvas elements can be created from ImageData
const imageDataToCanvas = (imageData) => {
  const maskCanvas = document.getElementById("maskImg")
	const maskCtx = maskCanvas.getContext("2d")
  maskCanvas.width = imageData.width
  maskCanvas.height = imageData.height
  maskCtx.putImageData(imageData, 0, 0)

  $("#maskImg").css("display", "")
}

// Convert the onnx model mask output to an HTMLImageElement
export const onnxMaskToImage = (input, width, height) =>  {
  let start = new Date()
  let image =  imageDataToCanvas(arrayToImageData(input, width, height));
  console.log("mask to iamge :", (new Date() - start) / 1000)
  return image
}

export const clearMask = () => {
  const maskCanvas = document.getElementById("maskImg")
	const maskCtx = maskCanvas.getContext("2d")

  maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height)
}