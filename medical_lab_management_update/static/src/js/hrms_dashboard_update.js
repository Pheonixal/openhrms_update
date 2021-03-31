odoo.define('hrms_dashboard.update', function (require) {
"use strict";
    var DashboardUpdate = require('hrms_dashboard.HrDashboard');
    var _t = core._t;
    var QWeb = core.qweb;

    DashboardUpdate.extend({
        render_department_employee:function(){
        var self = this;
        var w = 200;
        var h = 200;
        var r = h/2;
        var elem = this.$('.emp_graph');
        console.log("almas")
//        var colors = ['#ff8762', '#5ebade', '#b298e1', '#70cac1', '#cf2030'];
        var colors = ['#70cac1', '#659d4e', '#208cc2', '#4d6cb1', '#584999', '#8e559e', '#cf3650', '#f65337', '#fe7139',
        '#ffa433', '#ffc25b', '#f8e54b'];
        var color = d3.scale.ordinal().range(colors);
        rpc.query({
            model: "base.hr.employee",
            method: "get_dept_employee",
        }).then(function (data) {
            console.log(data)


            var legend = d3.select(elem[0]).append("table").attr('class','legend').attr('style', 'margin-top: 20px');

            // create one row per segment.
            var tr = legend.append("tbody").selectAll("tr").data(data).enter().append("tr");

            // create the first column for each segment.

            // create the second column for each segment.
            tr.append("td").attr('style', 'padding-left: 10px; font-size: 15px;').text(function(d){ return d.label;});

            // create the third column for each segment.
            tr.append("td").attr('style', 'padding-left: 50px; padding-right: 10px; font-size: 15px;')
                .text(function(d){ return d.value;});



        });

    },


    })

});
