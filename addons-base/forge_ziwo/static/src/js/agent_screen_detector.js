odoo.define('forge_ziwo.agent_screen_detector', function (require) {
    "use strict";

    const core = require('web.core');
    const formView = require('web.FormView');
    var _triggered = false;

    formView.include({
        init: function() {
            this._super.apply(this, arguments);
            core.bus.on('DOM_updated', null, () => {
                var model_name = this.loadParams.modelName;
                if (model_name && (model_name === 'agent.screen')) {
                    if (!_triggered) {
                        _triggered = true;
                        core.bus.trigger('forge_ziwo_onAgentScreen');
                        setTimeout(() => { _triggered = false; }, 1000);
                    }
                }
            });
        },
        on_attach_callback: function () {
            this._super.apply(this, arguments);
            this.on('on_change', this, () => {
                var model_name = this.loadParams.modelName;
                if (model_name && (model_name === 'agent.screen')) {
                    if (!_triggered) {
                        _triggered = true;
                        core.bus.trigger('forge_ziwo_onAgentScreen');
                        setTimeout(() => { _triggered = false; }, 1000);
                    }
                }
            });
        },

    });
});
