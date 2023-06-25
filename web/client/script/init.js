import {imageReset} from './utils.js'
import {samInit, mouseEvents, changeImage} from './sam.js'
import {menuComponent} from "./component.js";

mouseEvents()
imageReset()
samInit()
$("#reset").on("click", () => {
    imageReset()
    samInit()
    $("circle").remove()
    $("polygon").remove()
    $("#maskImg").attr("width", 0)
    $("#maskImg").attr("height", 0)
    $(".select-hover").addClass("hover")
    $(".select-hover").removeClass("select-hover")
})
$("#fileUploader").change(changeImage)
$("#fileButton").on("click", function(e){ $("#fileUploader").click() })
customElements.get(`menu-component`) || customElements.define(`menu-component`, menuComponent)