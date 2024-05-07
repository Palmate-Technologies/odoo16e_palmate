odoo.define('forge_ziwo.DialingPanel', function (require) {
    "use strict";
    
    const core = require('web.core');
    const config = require('web.config');
    const Widget = require('web.Widget');
    
    const { _t, _lt } = core;

    /**
     * @class
     * @extends {Widget}
     */
    const DialingPanel = Widget.extend({
        template: 'forge_ziwo.ZiwoDialingPanel',

        events: {
            'click .ziwo_dial_fold': '_onClickFold',
            'click .ziwo_dial_window_close': '_onClickWindowClose',
        },

        /**
         * @constructor
         */
        init() {
            this._super(...arguments);
            this.win = false;
            this._isFolded = false;
            this._isShow = false;
            this.title = this._getTitle();
            this.callRecord = false;
            this.model = false;
            this.record = false;
            this.record_status = false;
            this.session = false;
        },

        /**
         * @override
         */
        async willStart() {
            this._messaging = await owl.Component.env.services.messaging.get();
        },

        /**
         * @override
         */
        async start() {
            this.$el.hide();

            $(document).ready(() => {
                $('#ziwoFrame').on('load', () => {
                    this._updateWindow()
                    // console.log(this.win);
                });
            });

            core.bus.on('forge_ziwo_onToggleDisplay', this, () => {
                this._onToggleDisplay();
            });

            core.bus.on('forge_ziwo_onAgentScreen', this, (model_name) => {
                this._agentScreenDetected();
            });
            
            this.call('bus_service', 'addEventListener', 'notification', this._onBusNotification.bind(this));
        },

        /**
         * @override
         */
        destroy() {
            if (this.win !== false) {
                bus.off('notification', this);
                this.win.removeEventListener('ziwo-call-all', this._onZiwoEvent)
                this.win.removeEventListener('ziwo-call-active', this._onZiwoEvent)
            };
        },

        /**
         * @private
         */
        _updateWindow() {
            if (this.win === false && document.getElementById('ziwoFrame') !== null) {
                this.win = document.getElementById('ziwoFrame').contentWindow;
                this.win.addEventListener('ziwo-call-all', this._onZiwoEvent.bind(this));
                this.win.addEventListener('ziwo-call-active', this._onZiwoEvent.bind(this));
            }
            if (!this.session) {
                this.session = JSON.parse(localStorage.getItem('ZIWO_SESSION_DETAILS'));
            }
        },

        /**
         * @private
         */
        _fold() {
            this._isFolded ? this.$el.addClass('folded') : this.$el.removeClass('folded');
        },
        /**
         * @private
         * @returns {string}
         */
        _getTitle() {
            return _t("Ziwo");
        },

        /**
         * @private
         * @return {Promise}
         */
        async _showWidget() {
            if (!this._isShow) {
                this.$el.show();
                this._isShow = true;
                if (this._isFolded) {
                    await this._toggleFold();
                }
                this._isFolded = false;
            } else {
                if (this._isFolded) {
                    await this._toggleFold();
                }
                this._isFolded = false;
            }
        },

        /**
         * @private
         * @return {Promise}
         */
        async _showWidgetFolded() {
            if (!this._isShow) {
                this.$el.show();
                this._isShow = true;
                this._isFolded = true;
                this._fold(false);
            }
        },
        /**
         * @private
         * @return {Promise}
         */
        async _toggleDisplay() {
            if (this._isShow) {
                if (!this._isFolded) {
                    this.$el.hide();
                    this._isShow = false;
                } else {
                    return this._toggleFold({ isFolded: false });
                }
            } else {
                this.$el.show();
                this._isShow = true;
                if (this._isFolded) {
                    await this._toggleFold();
                }
                this._isFolded = false;
            }
        },
        /**
         * @private
         * @param {Object} [param0={}]
         * @param {boolean} [param0.isFolded]
         * @return {Promise}
         */
        async _toggleFold({ isFolded } = {}) {
            this._isFolded = _.isBoolean(isFolded) ? isFolded : !this._isFolded;
            this._fold();
        },

        // Handlers:

        /**
         * @private
         * @override
         */
        _onBackButton(ev) {
            this._onClickWindowClose(ev);
        },

        /**
         * @private
         * @return {Promise}
         */
        async _onClickFold() {
            return this._toggleFold();
        },

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClickWindowClose(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            this.$el.hide();
            this._isShow = false;
        },

        /**
         * @private
         * @param {CustomEvent} ev
         * @param {Object[]} [ev.detail] notifications coming from the bus.
         * @param {string} [ev.detail[i].type]
         */
        async _onBusNotification({ detail: notifications }) {
            await this._updateWindow()
            for (const notification of notifications) {
                // console.log('_onBusNotification: ', notification.type);
                if (notification.type === 'ziwo/bus') {
                    if (notification.payload.action === 'call') {
                        this._showWidget();
                        this.model = notification.payload.model;
                        this.record = notification.payload.record;
                        this.win.ZIWO.calls.startCall(notification.payload.mobile)
                            .catch((error) => {
                                console.error('Error while starting call:', error);
                            });
                    }
                    if (notification.payload.action === 'update') {
                        this.model = notification.payload.model;
                        this.record = notification.payload.record;
                        this._updateCallModel()
                            .catch((error) => {
                                console.error('Error while updating model:', error);
                            });
                    }
                    if (notification.payload.action === 'get') {
                        this._updateCallRecording(notification.payload.record)
                            .catch((error) => {
                                console.error('Error while updating call recording:', error);
                            });
                    }
                }
                
            }
        },

        /**
         * @private
         */
        async _onZiwoEvent({ detail: event }) {
            await this._updateWindow();
            const isInternal = event.call && event.call.participants[0].isInternal;
            // console.log('_onZiwoEvent', event);
            // console.log('isInternal', isInternal)
            if (!isInternal) {
                switch (event.type) {
                    case 'ringing':
                    case 'early':
                        var mobile = event.call.participants[0].number;
                        var call_type = event.call.direction;
                        var call_id = event.call.callId;
                        var call_time = event.call.startedAt;
                        var is_transfer = event.call.isTransfer;
                        var verto_call_id = event.call.vertoPrimaryCallId;

                        await this._showWidget();

                        if (!is_transfer && verto_call_id){
                            if (call_type === 'inbound') {
                                await this._createCallRecord(mobile, call_type, verto_call_id, call_time);
                            } else {
                                await this._transferCallRecord(verto_call_id,'blind');
                            }
                        
                        } else if (is_transfer) {
                            var parentCallId = event.call.userVariables.verto_h_transfer_origin_call_id;
                            await this._transferCallRecord(parentCallId,'attend');
                        
                        }  else if (this.callRecord === false){
                            await this._createCallRecord(mobile, call_type, call_id, call_time);

                        } else {
                            await this._updateCallID(call_id, call_time);

                        }
                        break;
                    case 'answering':
                        this.record_status = 'answered';
                        await this._updateCallStatus(this.record_status);
                        break;
                    case 'hangup':
                        var call_states = event.call.states;
                        var call_type = event.call.direction;
                        var cause = event.cause;
                        if (!this.record_status && !call_states.find(s => s.state === 3)) {
                            if (call_type === "outbound"){
                                if (!cause || cause === "NORMAL_CLEARING" || cause === "NO_USER_RESPONSE") {
                                    this.record_status = 'rejected';
                                } else {
                                    this.record_status = 'missed';
                                }
                            } else {
                                this.record_status = 'missed';
                            }
                            await this._updateCallStatus(this.record_status);
                        }
                        break;
                    case 'destroy':
                        await this._endCallProcedure();
                        break;
                }
            } else {
                await this._showWidget();
            }
        },

        /**
         * @private
         */
        async _endCallProcedure() {
            await this._updateWindow();
            await this._updateCallModel(!this.model);
            await this._createCallRecording();
            await this._createCallMessage();
            await this._clearData();
        },

        /**
         * @private
         */
        async _clearData() {
            this.callRecord = false;
            this.model = false;
            this.record = false;
            this.record_status = false;
        },

        /**
         * @private
         */
        async _createCallRecord(mobile, call_type, call_id, call_time) {
            const c2c_override = await this._rpc({
                model: 'forge.sudo.override',
                method: 'get_param_navigate_outbound_calls_c2c',
                args: [],
            });
            await this._rpc({
                model: 'ziwo.history',
                method: 'create_call_record',
                args: [mobile,call_type,call_id,call_time, this.model, this.record],
            }).then((result) => {
                this.callRecord = result.record_id;
                const override = this.model && c2c_override;
                if (result.action && !override) {
                    this._performWindowAction(result.action)
                }
            });
        },

        /**
         * @private
         */
        async _transferCallRecord(parent_call_id, transfer_type) {
            await this._rpc({
                model: 'ziwo.history',
                method: 'transfer_call_record',
                args: [parent_call_id, transfer_type],
            }).then((result) => {
                this.callRecord = result.record_id;
            });
        },

        async _updateCallRecording(record_id) {
            await this._updateWindow();
            await this._rpc({
                model: 'ziwo.history',
                method: 'create_call_recording',
                args: [record_id,this.session],
            }).then((result) => {
                if (result.action) {
                    this._performClientAction(result.action);
                }
            });
        },

        async _createCallRecording() {
            await this._rpc({
                model: 'ziwo.history',
                method: 'create_call_recording',
                args: [this.callRecord,this.session],
            });
        },

        async _updateCallID(call_id, call_time) {
            await this._rpc({
                model: 'ziwo.history',
                method: 'update_call_id',
                args: [this.callRecord, call_id, call_time],
            });
        },

        /**
         * @private
         */
        async _updateCallStatus(call_status) {
            await this._rpc({
                model: 'ziwo.history',
                method: 'update_call_status',
                args: [this.callRecord,call_status],
            });
        },

        /**
         * @private
         */
        async _createCallMessage() {
            await this._rpc({
                model: 'ziwo.history',
                method: 'create_call_message',
                args: [this.callRecord],
            });
        },

        /**
         * @private
         * @param {boolean} [context=false] - Optional parameter with a default value of false
         */
        async _updateCallModel(context=false) {
            const args = [this.callRecord, this.model, this.record];
            if (context) {
                const model_regex = /#id=(\d+).*model=([a-z\.]+)/;
                const model_data = this.$el[0].baseURI.match(model_regex);
                args.push(context);
                if (model_data){
                    args.push(model_data[2]);
                    args.push(model_data[1]);
                }
            }
            await this._rpc({
                model: 'ziwo.history',
                method: 'update_call_model',
                args: args,
            }).then((result) => {
                if (result.action) {
                    this._performWindowAction(result.action);
                }
            });
        },

        /**
         * @private
         */
        async _performWindowAction(result_action) {
            const action = await this._rpc({
                model: 'forge.sudo.override',
                method: 'create_act_window',
                args: [result_action],
            });
            this.do_action(action);
        },

        /**
         * @private
         */
        async _performClientAction(result_action) {
            const action = await this._rpc({
                model: 'forge.sudo.override',
                method: 'create_client_notification',
                args: [result_action],
            });
            this.do_action(action);
        },

        /**
         * @private
         */
        async _onToggleDisplay() {
            await this._toggleDisplay();
        },

        /**
         * @private
         */
        async _agentScreenDetected() {
            var model_regex = /model=([a-z\.]+)/;
            var model_data = this.$el[0].baseURI.match(model_regex);
            var model_agent_screen = false;
            if (model_data){
                model_agent_screen = model_data[1];
            }
            if (this.callRecord && (model_agent_screen !== 'agent.screen')){
                var result = await this._rpc({
                    model: 'ziwo.history',
                    method: 'set_agent_screen',
                    args: [this.callRecord],
                });
                this._performWindowAction(result);
            }
        },
    });
    
    return DialingPanel;
});