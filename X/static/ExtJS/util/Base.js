Ext.Ajax.timeout = 10000;
var re_phone = /^[0-9]{11}$/;
var re_email = /^(\w)+(\.\w+)*@(\w)+((\.\w{2,20}){1,3})$/;
var re_code = /^[a-zA-Z0-9_]{4,}$/;
var re_ip = /^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$/;
var re_port = /^(([1-9][0-9]{0,3})|([1-5][0-9]{4})|(6[0-4][0-9]{3})|(65[0-4][0-9]{2})|(655[0-2][0-9])|(6553[0-5]))|[0]$/;
var re_sp_id = /^[0-9]{6}$/;
var re_sp_pwd = /^[0-9]{6}$/;
var re_src_id = /^[0-9]{5,20}$/;
var re_ser_id = /^[a-zA-Z0-9_]{1,10}$/;
var re_version = /^[0-9]$/;
var re_speed = /^[0-9]{1,3}$/;
var re_suffix = /^[0-9]{1,4}$/;

var re_phones = /(^(([0-9]{11}|[0-9]{13}),)*([0-9]{11}|[0-9]{13})$)|(^$)/;

var qtpp_url = 'http://218.207.87.21:8080/dnmms/services/GetSIMMS?wsdl';
if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}
if (!String.prototype.getWidth) {
    String.prototype.getWidth = function (fontSize) {
        var span = document.getElementById("__getwidth");
        if (span == null) {
            span = document.createElement("span");
            span.id = "__getwidth";
            document.body.appendChild(span);
            span.style.visibility = "hidden";
            span.style.whiteSpace = "nowrap";
        }
        span.innerText = this;
        span.style.fontSize = fontSize + "px";
        span.style.fontWeight = "bold";
        span.style.fontFamily = "helvetica, arial, verdana, sans-serif";

        return span.offsetWidth;
    }
}