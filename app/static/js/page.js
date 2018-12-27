$(function() {


    $('.product').bind('change', function(){
        var row = $(this).closest("[data-toggle=fieldset-entry]");
        console.log( '###' );
        console.log( row );
        console.log( '###' );

        var id = $(this).val();
        // Cascading programming
        var _URL_ = '/api/v1.0/item/'+id;
        $.getJSON(
            _URL_,
            function(data) {
              _set_row( row, data );
            }
        );

    });

    var _set_row = function( row, data ){

        var transation_type = row.find('#transaction_type').val();
        if( transation_type == 'sale' ){
            row.find('.price').val(data.selling_price);
            row.find('.amount').val(data.selling_price);
        }
        else{
            row.find('.price').val(data.buying_price);
            row.find('.amount').val(data.buying_price);
        }

        row.find('.qty').val(1);

        calcProdSubTotal();
    };


    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);

        //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"));
            var oldrow = target.find("[data-toggle=fieldset-entry]:last");
            var row = oldrow.clone(true, true);
            console.log(row.find(":input")[0]);
            var elem_id = row.find(":input")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            row.attr('data-id', elem_num);

            row.find(":input").each(function() {
                console.log(this);
                if( $(this).attr('id') !== 'transaction_type'){
                    var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                    $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
                }
            });

            row.show();
            oldrow.after(row);
        }); //End add new entry



        //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
});



// UTILITY FUNCTIONS

function IsNumeric(n) {
    return !isNaN(n);
}

function CleanNumber(value) {

    // Assumes string input, removes all commas, dollar signs, and spaces
    newValue = value.toString().replace(",","");
    newValue = newValue.replace("$","");
    newValue = newValue.replace(/ /g,'');
    return newValue;

}

function CommaFormatted(amount) {

	var delimiter = ".";
	var i = parseInt(amount);

	if(isNaN(i)) { return ''; }

	i = Math.abs(i);

	var minus = '';
	if (i < 0) { minus = '-'; }

	var n = new String(i);
	var a = [];

	while(n.length > 3)
	{
		var nn = n.substr(n.length-3);
		a.unshift(nn);
		n = n.substr(0,n.length-3);
	}

	if (n.length > 0) { a.unshift(n); }

	n = a.join(delimiter);

	amount = minus + n;

	return amount;

}


// ORDER FORM UTILITY FUNCTIONS

function applyName(klass, numPallets) {

    var toAdd = $("td." + klass).text();

    var actualClass = $("td." + klass).attr("rel");

    $("input." + actualClass).attr("value", numPallets + " pallets");

}

function removeName(klass) {

    var actualClass = $("td." + klass).attr("rel");

    $("input." + actualClass).attr("value", "");

}

function calcTotalPallets() {

    var totalPallets = 0;

    $(".qty").each(function() {

        var thisValue = parseInt($(this).val());

        if ( (IsNumeric(thisValue)) &&  (thisValue != '') ) {
            totalPallets += parseInt(thisValue);
        };

    });

    $("#total-pallets-input").val(totalPallets);

}

function calcProdSubTotal() {

    var prodSubTotal = 0;

    $(".row-total-input").each(function() {

        var valString = $(this).val() || 0;

        prodSubTotal += parseInt(valString);

    });

    $(".total").val(prodSubTotal);

}

function calcShippingTotal() {

    var totalPallets = $("#total-pallets-input").val() || 0;
    var shippingRate = $("#shipping-rate").text() || 0;
    var shippingTotal = totalPallets * shippingRate;

    $("#shipping-subtotal").val(CommaFormatted(shippingTotal));

}

function calcOrderTotal() {

    var orderTotal = 0;

    var productSubtotal = $("#product-subtotal").val() || 0;
    var shippingSubtotal = $("#shipping-subtotal").val() || 0;
    var underTotal = $("#under-box").val() || 0;

    var orderTotal = parseInt(CleanNumber(productSubtotal)) + parseInt(CleanNumber(shippingSubtotal));

    $("#order-total").val(CommaFormatted(orderTotal));
    $("#total").text(CommaFormatted(orderTotal));

    $("#fc-price").attr("value", orderTotal);

}

// DOM READY
$(function() {

    var inc = 1;

    $(".product-title").each(function() {

        $(this).addClass("prod-" + inc).attr("rel", "prod-" + inc);

        var prodTitle = $(this).text();

        $("#foxycart-order-form").append("<input type='hidden' name='" + prodTitle + "' value='' class='prod-" + inc + "' />");

        inc++;

    });

    // Reset form on page load, optional
    $("#order-table input[type=text]:not('#product-subtotal')").val("");
    $("#product-subtotal").val("$0");
    $("#shipping-subtotal").val("$0");
    $("#fc-price").val("$0");
    $("#order-total").val("$0");
    $("#total-pallets-input").val("0");

    // "The Math" is performed pretty much whenever anything happens in the quanity inputs
    $('.qty').bind("focus blur change keyup", function(){

        //alert();

        // Caching the selector for efficiency
        var $el = $(this);

        // Grab the new quantity the user entered
        var numPallets = CleanNumber($el.val());

        // Find the pricing
        var multiplier = $el
            .parent().parent()
            .find("td.price input")
            .val();

        // If the quantity is empty, reset everything back to empty
        if ( (numPallets == '') || (numPallets == 0) ) {

            $el
                .removeClass("warning")
                .parent().parent()
                .find("td.row-total input")
                .val("");

            var titleClass = $el.parent().parent().find("td.product-title").attr("rel");

            removeName(titleClass);

        // If the quantity is valid, calculate the row total
        } else if ( (IsNumeric(numPallets)) && (numPallets != '') ) {

            var rowTotal = numPallets * multiplier;

            $el
                .removeClass("warning")
                .parent().parent()
                .find("td.row-total input")
                .val(rowTotal);

            var titleClass = $el.parent().parent().find("td.product-title").attr("rel");

            applyName(titleClass, numPallets);

        // If the quantity is invalid, let the user know with UI change
        } else {

            $el
                .addClass("warning")
                .parent().parent()
                .find("td.row-total input")
                .val("");

            var titleClass = $el.parent().parent().find("td.product-title").attr("rel");

            removeName(titleClass);

        };

        // Calcuate the overal totals
        calcProdSubTotal();
        calcTotalPallets();
        calcShippingTotal();
        calcOrderTotal();

    });

});
