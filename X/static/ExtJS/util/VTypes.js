Ext.apply(Ext.form.VTypes, {
    passConfirm: function (val, field) {
        if (field.confirmTo) {
            var form = field.findParentByType("form");
            var pass = form.getForm().findField(field.confirmTo);
            return (val == pass.getValue());
        }
        return true;
    },
    uniqueCode: function (val, field) {
        if (!field.uniqueKey) {
            return true;
        }
        if (!field.idField) {
            return true;
        }
        var flag = false;

        var id;//检查是否有ID
        var form = field.findParentByType("form");
        var idField = form.getForm().findField(field.idField);
        if (idField && idField.getValue()) id = idField.getValue();
        return true;
        Ext.Ajax.request({
            url: 'unique',
            async: false,
            params: {'id': id, 'type': field.uniqueKey, 'value': val},
            method: 'POST',
            success: function (response, options) {
                var json = Ext.decode(response.responseText);//JSON.parse(response.responseText);
                flag = json.unique;
            },
            failure: function (response, options) {
                flag = false;
            }
        });
        return flag;
    },
    comboBox: function (val, field) {
        return !!field.getDisplayValue();
    }
});