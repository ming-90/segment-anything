export let imgShape

export const imageReset = () => {
    let today = new Date();
    $("#img").attr("src", "/client/image/default.png?ver=" + today.getSeconds() )
    resizeImage()
}

const resizeImage = () => {
    // $("#maskImg").css("display", "none")
    const image_frame_width = window.innerWidth - 300
    const image_frame_height = window.innerHeight - 150
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

window.addEventListener(`resize`, resizeImage);