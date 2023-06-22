import {imageReset} from './utils.js'
import {samInit, mouseEvents} from './sam.js'
import {menuComponent} from "./component.js";

mouseEvents()
imageReset()
samInit()
customElements.get(`menu-component`) || customElements.define(`menu-component`, menuComponent)