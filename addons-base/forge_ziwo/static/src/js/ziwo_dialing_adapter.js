/** @odoo-module **/

import { ComponentAdapter } from "web.OwlCompatibility";
import core from "web.core";
import { useBus } from "@web/core/utils/hooks";

const { Component } = owl;

export class ZiwoDialingAdapter extends ComponentAdapter {
    setup() {
        super.setup();
        this.env = Component.env;

        const ziwoBus = this.props.bus;

        useBus(ziwoBus, "ZIWO_TOGGLE_DIALING_PANEL", () => {
            core.bus.trigger('forge_ziwo_onToggleDisplay');
        });
    }
}