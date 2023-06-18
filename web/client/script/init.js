import {imageReset, mouseEvents, samInit} from './utils.js'
import { menuComponent } from "./component.js";

imageReset()
mouseEvents()
samInit()
customElements.get(`menu-component`) || customElements.define(`menu-component`, menuComponent)
