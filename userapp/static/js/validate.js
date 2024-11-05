$("#id_payment").on('change', function(){
    var val = $("#id_payment").val();

    if (val.length === 0) {
        console.log("Array is empty!")
        //        make two bank can open
        $("#id_issuing_bank option:selected").prop("selected", false);
        $("#id_issuing_bank").multiselect('refresh');
        $("#id_receiving_bank option:selected").prop("selected", false);
        $("#id_receiving_bank").multiselect('refresh');
        $("#id_tt_bank option:selected").prop("selected", false);
        $("#id_tt_bank").multiselect('refresh');
        document.getElementById("id_credit_amount").value = null;
        document.getElementById("id_credit_period").value = null;

        $("#id_issuing_bank").multiselect('disable');
        $("#id_receiving_bank").multiselect('disable');
        $("#id_tt_bank").multiselect('disable');
        document.getElementById("id_credit_amount").disabled = true;
        document.getElementById("id_credit_period").disabled = true;
        return
    }

    if (val.includes('1')) {
        $("#id_issuing_bank").multiselect('enable');
        $("#id_receiving_bank").multiselect('enable');
    }
    else {
        $("#id_issuing_bank option:selected").prop("selected", false);
        $("#id_issuing_bank").multiselect('refresh');
        $("#id_receiving_bank option:selected").prop("selected", false);
        $("#id_receiving_bank").multiselect('refresh');

        $("#id_issuing_bank").multiselect('disable');
        $("#id_receiving_bank").multiselect('disable');
    }

    if (val.includes('2') || val.includes('3')) {
        $("#id_tt_bank").multiselect('enable');
        document.getElementById("id_credit_amount").disabled = false;
        document.getElementById("id_credit_period").disabled = false;
    }
    else {
        $("#id_tt_bank option:selected").prop("selected", false);
        $("#id_tt_bank").multiselect('refresh');
        document.getElementById("id_credit_amount").value = null;
        document.getElementById("id_credit_period").value = null;

        $("#id_tt_bank").multiselect('disable');
        document.getElementById("id_credit_amount").disabled = true;
        document.getElementById("id_credit_period").disabled = true;
    }

    console.log(val);
});