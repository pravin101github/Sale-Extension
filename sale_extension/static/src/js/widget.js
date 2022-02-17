odoo.define('sale_customization.widget', function (require) {
"use strict";

var field_registry = require('web.field_registry');
var basicFields = require('web.basic_fields');
var FieldText = basicFields.FieldText;
var InputField = basicFields.InputField;

var Symbol = InputField.extend({
    className: 'o_field_integer o_field_number',
    tagName: 'span',
    supportedFieldTypes: ['float', 'integer'],
    resetOnAnyFieldChange: true,
    /**
     * Using Symbol widget have an additional currency_field
     * parameter which defines the name of the field from which set sign before it
     * should be read.
     *
     * @override
     */

    isSet: function () {
        return this.value === 0 || this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * While field in edit mode we remove widget and readonly
     *set it again
     * @override
     * @private
     */
    _render: function () {

        this._super.apply(this, arguments);
        var self = this
        var $Sign = $('<span>', {text: '₹'});
        self.$el.prepend($Sign);
    },



    _renderReadonly: function () {
        this.$el.html(this._formatValue(this.value));
    },
    /**
     * Re-gets the currency as its value may have changed.
     * @see FieldMonetary.resetOnAnyFieldChange
     *
     * @override
     * @private
     */

});

field_registry.add('Symbol', Symbol)

return {
    Symbol: Symbol,
};

});
