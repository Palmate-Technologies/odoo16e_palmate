odoo.define('forge_ziwo.FormViewWithoutControlPanel', function (require) {
    "use strict";
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var FormViewWithoutControlPanel = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            withControlPanel: false,
        }),
    });
    view_registry.add('form_without_control_panel', FormViewWithoutControlPanel);
    return FormViewWithoutControlPanel;
});
