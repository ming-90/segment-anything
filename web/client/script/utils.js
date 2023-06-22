let imgShape
let distanceWidth = 320
let distanceHeight = 150

$("img").on("load", function() { resizeImage() })

export const imageReset = () => {
    let today = new Date();
    $("#img").attr("src", "/client/image/default.png?ver=" + today.getSeconds())
}

export const distanceSize = () => {
    return [distanceHeight, distanceWidth]
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

    console.log($("#img").css("width").replace("px", ""))
    console.log($("#img").css("height").replace("px", ""))
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

export const drawCircle = (info) => {
    let tagString =
        `<circle
            name='${info.name}'
            id='${info.id}'
            cx='${info.x}'
            cy='${info.y}'
            fill='${info.fill}'
            r='${info.r}'
        />`
    document.getElementById('objectSvg').appendChild(parseSVG(tagString));
}

const parseSVG = (s) => {
    let div= document.createElementNS('http://www.w3.org/1999/xhtml', 'div');
    div.innerHTML= '<svg xmlns="http://www.w3.org/2000/svg">'+s+'</svg>';
    let frag= document.createDocumentFragment();
    while (div.firstChild.firstChild)
        frag.appendChild(div.firstChild.firstChild);
    return frag;
}

window.addEventListener(`resize`, resizeImage);