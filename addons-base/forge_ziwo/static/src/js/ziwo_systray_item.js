/** @odoo-module **/

const { Component } = owl;

export class ZiwoSystrayItem extends Component {
    onClick() {
        this.props.bus.trigger('ZIWO_TOGGLE_DIALING_PANEL');
    }
}
ZiwoSystrayItem.template = "forge_ziwo.ZiwoSystrayItem";
