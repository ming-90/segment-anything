
export let imgShape
export let tensor
export let model
export let isHover = false
let distanceWidth = 320
let distanceHeight = 150

export const imageReset = () => {
    let today = new Date();
    $("#img").attr("src", "/client/image/default.png?ver=" + today.getSeconds() )
    resizeImage()
}

const resizeImage = () => {
    // $("#maskImg").css("display", "none")
    const image_frame_width = window.innerWidth - distanceWidth
    const image_frame_height = window.innerHeight - distanceHeight
    const img_width = $("#img").css("width").replace("px", "") * 1
    const img_height = $("#img").css("height").replace("px", "") * 1

    imgShape = {
        width: img_width, height: img_height
    }

    const less_width = image_frame_width - img_width
    const less_height = image_frame_height - img_height

    if (less_width < less_height) {
        $("#img").css("width", image_frame_width - 100)
        $("#img").css("height", "")
        $("#objectSvg").css("width", $("#img").css("width").replace("px", ""))
        $("#objectSvg").css("height", $("#img").css("height").replace("px", ""))
    }else{
        $("#img").css("height", image_frame_height - 100)
        $("#img").css("width", "")
        $("#objectSvg").css("width", $("#img").css("width").replace("px", ""))
        $("#objectSvg").css("height", $("#img").css("height").replace("px", ""))
    }
}

export const mouseEvents = () => {
    $("body").on("mouseup", function(e){
        let X = e.pageX - distanceHeight
        let Y = e.pageY - distanceWidth
        console.log("mouse up")
    })

    $("body").on("mousemove", function(e){
        let X = e.pageX - distanceHeight
        let Y = e.pageY - distanceWidth
        if(!isHover) return
        console.log("mouse move")
        hoverMouseMove()
    })
}

export const samInit = async () => {
    const MODEL_DIR = "/model/sam_decoder_uint8.onnx";
    model = await ort.InferenceSession.create(MODEL_DIR).then(console.log("model loaded"));

    // const imageUrl = "frontend/image/default.png";
    // const response = await fetch(imageUrl);
    // const data = await response.blob();
    // imageFile = new File([data], "default.png", { type: 'image/png' });

    const IMAGE_EMBEDDING = "/model/embedding.npy";
    NumpyLoader.ajax(IMAGE_EMBEDDING, function (e) {
        tensor = new ort.Tensor("float32", e.data, e.shape);
        console.log("image embedding loaded")
    })
}

const hoverMouseMove = async (coor) => {
    if (!isHover) return
    const { height, width, samScale } = handleImageScale();
    let modelScale = {
        samScale: samScale,
        height: height,
        width: width
    }
    let click = {
        x: coor[0],
        y: coor[1],
        clickType: 1
    }
    let clicks = [click]

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

window.addEventListener(`resize`, resizeImage);