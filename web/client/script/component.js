import {hoverChange} from './sam.js'

let componentSeq = 0

export class menuComponent extends HTMLElement{
    connectedCallback(){
        $(this).on("click", function(){
            let children = $(this).children()
            if(children.hasClass("select-hover")){
                children.addClass("hover")
                children.removeClass("select-hover")
                hoverChange(false)
            }else{
                children.addClass("select-hover")
                children.removeClass("hover")
                hoverChange(true)
            }
        })
        this.innerHTML = `
        <div class="box button-group hover" name="menu_button">
            <div class="flex menu-title">
                <div>
                    <img class="menu-icon" src="/client/icon/mouse.png">
                </div>
                <div>
                    <div><p class="menu-inner">${this.attributes.title.value}</p></div>
                </div>
            </div>
            <div>
                <p class="info-text">${this.attributes.description.value}</p>
            </div>
            <div class=parameters> </div>
        </div>
        `
    }
}