odoo.define('documentation.data', function (require) {
"use strict";


var page=require('web.UserMenu');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
var usepage=page.include({
    _onMenuPassport: function () {
        var self = this;
        var session = this.getSession();
        var args = ['', {
            'uid' : session.uid,
        }];
        rpc.query({
            'model': 'hr.employee',
            'method': 'open_current_user_employee_passport',
            'args': args,
            })
            .then(function (result) {
                self.do_action(result);
            });
    },
    })

});