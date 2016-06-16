Ext.Ajax.timeout = 10000;
var re_phone = /^[0-9]{11}$/;
var re_email = /^(\w)+(\.\w+)*@(\w)+((\.\w{2,20}){1,3})$/;
var re_code = /^[a-zA-Z0-9_]{4,}$/;
var re_ip = /^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$/;
var re_port = /^(([1-9][0-9]{0,3})|([1-5][0-9]{4})|(6[0-4][0-9]{3})|(65[0-4][0-9]{2})|(655[0-2][0-9])|(6553[0-5]))|[0]$/;
var re_sp_id = /^[0-9]{6}$/;
var re_sp_pwd = /^.+$/;
var re_src_id = /^[0-9]{5,20}$/;
var re_ser_id = /^[a-zA-Z0-9_]{1,10}$/;
var re_version = /^[0-9]$/;
var re_speed = /^[0-9]{1,3}$/;
var re_suffix = /^[0-9]{1,4}$/;
var re_digital = /^\d+$/;
var re_percent = /^\d+%$/;
var re_share = /^\d+:\d+$/;
var re_number = /^\d+\.?\d*$/;

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

if (!String.prototype.startsWith) {
    String.prototype.startsWith = function (str) {
        if (str == null || str == "" || this.length == 0 || str.length > this.length)
            return false;
        if (this.substr(0, str.length) == str)
            return true;
        else
            return false;
        return true;
    }
}

if (!String.prototype.endsWith) {
    String.prototype.endsWith = function (str) {
        if (str == null || str == "" || this.length == 0 || str.length > this.length)
            return false;
        if (this.substring(this.length - str.length) == str)
            return true;
        else
            return false;
        return true;
    }
}

if (!Date.prototype.format) {
    Date.prototype.format = function (fmt) { //author: meizz
        var o = {
            "M+": this.getMonth() + 1, //月份
            "d+": this.getDate(), //日
            "h+": this.getHours(), //小时
            "m+": this.getMinutes(), //分
            "s+": this.getSeconds(), //秒
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度
            "S": this.getMilliseconds() //毫秒
        };
        if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }
}