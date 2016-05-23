Ext.define('X.view.LoginWindow', {
    extend: 'Ext.window.Window',

    requires: ['Ext.form.Panel', 'Ext.form.FieldSet', 'Ext.form.field.Text',
        'Ext.button.Button'],

    height: 220,
    width: 400,
    title: '登陆窗口',

    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.cfg = cfg;
        me.callParent();
    },

    initComponent: function () {
        var me = this;

        var do_reset = function (btn) {
            if (enable_email(btn)) {
                return
            }
            tools.getCmp(me, {
                xtype: "form"
            }).getForm().reset();
        };

        var wait_interval = function (btn, text, sleep_time) {
            if (sleep_time <= 0) {
                btn.setText(text);
                btn.enable();
            }
            else {
                btn.setText(text + '(' + sleep_time + ')');
            }
        };

        var set_wait = function (btn, wait_time) {
            if (!btn) return false;
            btn.disable();
            var text = btn.text;
            var interval = setInterval(function () {
                wait_interval(btn, text, --wait_time);
            }, 1000);
            setTimeout(function () {
                window.clearInterval(interval);
            }, 1000 * (wait_time + 1));
        };

        var verify = function (btn, method) {
            tools.getCmp(me, {
                xtype: "form"
            }).getForm().submit({
                url: 'base/user-verify-' + method + '/',
                method: 'POST',
                waitTitle: '提示',
                waitMsg: '正在获取验证码',
                success: function (form, action) {
                    try {
                        var json = Ext.decode(action.response.responseText);
                        Ext.Msg.alert('成功', json.message);
                    } catch (e) {
                        Ext.Msg.alert('错误', action.response.responseText);
                    }
                },
                failure: function (form, action) {
                    try {
                        var json = Ext.decode(action.response.responseText);
                        Ext.Msg.alert('错误', json.message);
                    } catch (e) {
                        Ext.Msg.alert('错误', action.response.responseText);
                    }
                }
            });
            set_wait(btn, 10);
        };

        var email_click_times = 0;
        var enable_email = function (btn) {
            email_click_times++;
            if (email_click_times > 10) {
                verify(btn, 'email');
                return true;
            }
        };

        var do_post = function (btn) {
            tools.getCmp(me, {
                xtype: "form"
            }).getForm().submit({
                url: 'base/user-login/',
                method: 'POST',
                waitTitle: '提示',
                waitMsg: '正在登陆系统',
                success: function (form, action) {
                    Ext.Msg.alert('成功', '登陆成功！', function (button, text) {
                        me.cfg.success();
                        me.close();
                    });
                },
                failure: function (form, action) {
                    try {
                        var json = Ext.decode(action.response.responseText);
                        Ext.Msg.alert('错误', json.message);
                    } catch (e) {
                        Ext.Msg.alert('错误', action.response.responseText);
                    }
                }
            });
            set_wait(btn, 10);
        };

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'form',
                    bodyPadding: 10,
                    items: [
                        {
                            xtype: 'fieldset',
                            title: '请填写账号和密码',
                            items: [
                                {
                                    xtype: 'textfield',
                                    anchor: '100%',
                                    fieldLabel: '账号',
                                    name: 'object.code'
                                },
                                {
                                    xtype: 'textfield',
                                    anchor: '100%',
                                    fieldLabel: '密码',
                                    name: 'object.pwd',
                                    inputType: 'password'
                                }, {
                                    xtype: 'textfield',
                                    anchor: '100%',
                                    fieldLabel: '验证码',
                                    name: 'object.verify',
                                    listeners: {
                                        specialkey: function (f, e) {
                                            if (e.getKey() == e.ENTER) {
                                                do_post();
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    xtype: 'button',
                    margin: '0 5 0 10',
                    text: '获取验证码',
                    listeners: {
                        'click': function (btn) {
                            verify(btn, 'sms')
                        }
                    }
                },
                {
                    xtype: 'button',
                    margin: '0 5 0 10',
                    text: '登陆',
                    listeners: {
                        'click': do_post
                    }
                },
                {
                    xtype: 'button',
                    margin: '0 10 0 5',
                    text: '重置',
                    listeners: {
                        'click': do_reset
                    }
                }
            ]
        });

        me.callParent(arguments);
    }
});