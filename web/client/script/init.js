import { menuComponent } from "./component.js";

customElements.get(`menu-component`) || customElements.define(`menu-component`, menuComponent)