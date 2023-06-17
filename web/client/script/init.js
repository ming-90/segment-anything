import {imageReset} from './utils.js'
import { menuComponent } from "./component.js";

imageReset()
customElements.get(`menu-component`) || customElements.define(`menu-component`, menuComponent)