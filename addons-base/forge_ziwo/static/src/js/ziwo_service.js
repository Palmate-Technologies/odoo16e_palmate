/** @odoo-module **/

import { registry } from "@web/core/registry";

import { ZiwoSystrayItem } from "./ziwo_systray_item";
import { DialingPanelContainer } from "./dialing_panel_container";

const { EventBus } = owl;

const systrayRegistry = registry.category("systray");
const mainComponentRegistry = registry.category("main_components");

export const ziwoService = {
    dependencies: ["user", "notification"],
    async start(env, { user, notification }) {
        const isEmployee = await user.hasGroup('base.group_user');
        let bus;
        // console.log(isEmployee);
        if (isEmployee) {
            bus = new EventBus();
            systrayRegistry.add('forge_ziwo', { Component: ZiwoSystrayItem, props: { bus } });
            mainComponentRegistry.add('forge_ziwo.DialingPanelContainer', {
                Component: DialingPanelContainer,
                props: { bus },
            });
        }
    },
};
