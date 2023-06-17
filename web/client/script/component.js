

class menuComponent extends HTMLElement{
    connectedCallback(){
        this.innerHTML = `
        <div class="box button-group hover" name="menu_button" id="dot">
            <div class="flex menu-title">
                <div>
                    <img class="menu-icon" src="/client/icon/mouse.png">
                </div>
                <div>
                    <div><p class="menu-inner">${this.attributes.title.value}</p></div>
                </div>
            </div>
            <div>
                <p class="info-text">
                    ${this.attributes.description.value}
                </p>
            </div>
            <div class=parameters> </div>
        </div>
        `
    }
}

export {menuComponent}