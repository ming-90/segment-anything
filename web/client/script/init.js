import {imageReset} from './utils.js'
import {samInit, mouseEvents, changeImage} from './sam.js'
import {menuComponent} from "./component.js";

mouseEvents()
imageReset()
samInit()
$("#fileUploader").change(changeImage)
$("#fileButton").on("click", function(e){ $("#fileUploader").click() })
customElements.get(`menu-component`) || customElements.define(`menu-component`, menuComponent)