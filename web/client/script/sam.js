import {distanceSize, drawCircle} from "./utils.js"
import {onnxMaskToImage, clearMask} from "./maskUtils.js"
let isHover = false
let model
let imgShape
let tensor
let [distanceHeight, distanceWidth] = distanceSize()
let lefts = []
let rights = []

export const samInit = async () => {
    const MODEL_DIR = "/decoder/sam_onnx_quantized.onnx";
    model = await ort.InferenceSession.create(MODEL_DIR).then(console.log("model loaded"));

    const IMAGE_EMBEDDING = "/model/embedding.npy";
    NumpyLoader.ajax(IMAGE_EMBEDDING, function (e) {
        tensor = new ort.Tensor("float32", e.data, e.shape);
        console.log("image embedding loaded")
    })
}

export const mouseEvents =  () => {
    $("body").on("mouseup", async function(e){
        let X = e.pageX - distanceWidth
        let Y = e.pageY - distanceHeight
        mouseClick(e, [X, Y])
    })

    $("body").on("mousemove", function(e){
        if(!isHover) return
        let X = e.pageX - distanceWidth
        let Y = e.pageY - distanceHeight
        hoverMouseMove([X, Y])
    })
}

export const hoverChange = (hover) => {
    isHover = hover
    if(!hover) clearMask()
}

const mouseClick = async (e, coor) => {
    let fill = "#0000ff"
    if((e.button == 0)) {
        fill = "#ff0000"
        lefts.push({
            x: coor[0],
            y: coor[1],
            clickType: 1
        })
    }else{
        fill = "#0000ff"
        rights.push({
            x: coor[0],
            y: coor[1],
            clickType: 0
        })
    }
    let clicks = lefts.concat(rights)
    await run(clicks)

    let info = {
        name:"dot",
        id:"dot",
        x: coor[0],
        y: coor[1],
        fill:fill,
        r:"4"
    }
    drawCircle(info)
    isHover = false
}

const hoverMouseMove = async (coor) => {
    if (!isHover) return
    let click = {
        x: coor[0],
        y: coor[1],
        clickType: 1
    }
    let clicks = [click]
    await run(clicks)
}

const run = async (clicks) => {
    const { height, width, samScale } = handleImageScale();
    let modelScale = {
        samScale: samScale,
        height: height,
        width: width
    }
    const feeds = modelData({
        clicks,
        tensor,
        modelScale,
    });
    if (feeds === undefined) return
    const results = await model.run(feeds)
    const output = results[model.outputNames[0]]
    onnxMaskToImage(output.data, output.dims[2], output.dims[3])
}

const handleImageScale = () => {
    // Input images to SAM must be resized so the longest side is 1024
    const LONG_SIDE_LENGTH = 1024
    let w = $("#img").width()
    let h = $("#img").height()
    const samScale = LONG_SIDE_LENGTH / Math.max(h, w)

    return { height: h, width: w, samScale }
}

const modelData = ({ clicks, tensor, modelScale }) => {
    const imageEmbedding = tensor;
    let pointCoords;
    let pointLabels;
    let pointCoordsTensor;
    let pointLabelsTensor;

    // Check there are input click prompts
    if (clicks) {
        let n = clicks.length;

        // If there is no box input, a single padding point with
        // label -1 and coordinates (0.0, 0.0) should be concatenated
        // so initialize the array to support (n + 1) points.
        pointCoords = new Float32Array(2 * (n + 1));
        pointLabels = new Float32Array(n + 1);

        // Add clicks and scale to what SAM expects
        for (let i = 0; i < n; i++) {
            pointCoords[2 * i] = clicks[i].x * modelScale.samScale;
            pointCoords[2 * i + 1] = clicks[i].y * modelScale.samScale;
            pointLabels[i] = clicks[i].clickType;
        }

        // Add in the extra point/label when only clicks and no box
        // The extra point is at (0, 0) with label -1
        pointCoords[2 * n] = 0.0;
        pointCoords[2 * n + 1] = 0.0;
        pointLabels[n] = -1.0;

        // Create the tensor
        pointCoordsTensor = new ort.Tensor("float32", pointCoords, [1, n + 1, 2]);
        pointLabelsTensor = new ort.Tensor("float32", pointLabels, [1, n + 1]);
    }
    const imageSizeTensor = new ort.Tensor("float32", [
        modelScale.height,
        modelScale.width,
    ]);

    if (pointCoordsTensor === undefined || pointLabelsTensor === undefined)
        return;

    // There is no previous mask, so default to an empty tensor
    const maskInput = new ort.Tensor(
        "float32",
        new Float32Array(256 * 256),
        [1, 1, 256, 256]
    );
    // There is no previous mask, so default to 0
    const hasMaskInput = new ort.Tensor("float32", [0]);

    return {
        image_embeddings: imageEmbedding,
        point_coords: pointCoordsTensor,
        point_labels: pointLabelsTensor,
        mask_input: maskInput,
        has_mask_input: hasMaskInput,
        orig_im_size: imageSizeTensor,
    };
};