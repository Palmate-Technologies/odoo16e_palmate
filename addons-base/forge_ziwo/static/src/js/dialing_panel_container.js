/** @odoo-module **/
import DialingPanel from "forge_ziwo.DialingPanel";
import { ZiwoDialingAdapter } from "./ziwo_dialing_adapter";

const { Component, xml } = owl;

export class DialingPanelContainer extends Component {
    setup() {
        this.DialingPanel = DialingPanel;
        // console.log('Panel Container Setup');
    }
}
DialingPanelContainer.template = xml`
    <div class="o_voip_dialing_panel_container">
        <ZiwoDialingAdapter Component="DialingPanel" bus="props.bus" />
    </div>`;
DialingPanelContainer.components = { ZiwoDialingAdapter };