odoo.define('documentation.data', function (require) {
"use strict";


var page=require('web.UserMenu');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
var usepage=page.include({
    _onMenuManual: function () {
        var base_url = window.location.origin;
        window.open(base_url + '/user_manual/', '_blank');
    },
    })

});