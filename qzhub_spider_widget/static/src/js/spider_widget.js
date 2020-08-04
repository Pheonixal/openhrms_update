odoo.define('hr_employee_view.RadarWidget', function (require) {
    "use strict";

    let AbstractField = require('web.AbstractField');
    let core = require('web.core');
    let field_registry = require('web.field_registry');
    let utils = require('web.utils');

    let _t = core._t;


    let SpiderWidget = AbstractField.extend({
        className: "oe_radar_value  d-block",
        jsLibs: [
            '/hr_employee_updation/static/src/js/lib/Chart.js',
        ],

        //Render this chart in odoo front

        _renderReadonly: function () {
            var self = this;
            return this._rpc({
                model: 'hr.employee.skill',
                method: 'gotSkills',
                args: [self.record.data.id],
            }).then(response => {
                let spiderwidget = {
                    type: 'radar',
                    data: {
                        labels: response.map(val => val.label_id),
                        datasets: [{
                            label: 'Current',
                            data: response.map(val => val.level),
                            backgroundColor: 'rgba(233, 0, 6, 0.39)'
                        }, {
                            label: 'Required',
                            data: response.map(val => val.required_level),
                            backgroundColor: 'rgba(38,233,0,0.39)'
                        }]
                    },
                    options: {
                        responsive: true,
                        scale: {
                            angleLines: {
                                display: false
                            },
                            ticks: {
                                suggestedMin: 1,
                                suggestedMax: 5
                            }
                        }
                    }
                };
                //variables
                this.$canvas = $('<canvas/>');
                this.$el.empty();
                this.$el.append(this.$canvas);
                this.$el.attr('style', this.nodeOptions.style);
                this.$el.css({position: 'relative'});
                let context = this.$canvas[0].getContext('2d');
                context.canvas.style.maxWidth = '99%';
                context.canvas.style.minWidth = '90%';
                this.chart = new Chart(context, spiderwidget);
                let $value = $('<span class="oe_radar_widget_value">')
                $value.css({
                    'text-align': 'center',
                    position: 'absolute',
                    left: 0,
                    right: 0,
                    bottom: '6px',
                    'font-weight': 'bold'
                });

                this.$el.append($value);


            })

        },

        _render: function () {
            return this._renderReadonly();
        },

    });

    field_registry.add("spider", SpiderWidget);

    return SpiderWidget;

});
