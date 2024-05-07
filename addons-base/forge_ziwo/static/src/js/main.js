/** @odoo-module **/

import { ziwoService } from "./ziwo_service";
import { registry } from "@web/core/registry";

// console.log('ZIWO main is loaded successfully');

registry.category('services').add("forge_ziwo", ziwoService);