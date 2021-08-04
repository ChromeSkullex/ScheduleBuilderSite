$(function(){
    console.log("Please just work")
    $(".subButton").click(function() {
        console.log("Hey ")
        checked = $("input[type=checkbox]:checked").length;

        if(!checked) {
            $("#validate").show();
            return false;
        }
    });

});

$(function(){
    $("#religionCheck").click(function(){
        if ($(this).is(":checked")){
            $("#mergeReligion").removeAttr("disabled")
            $("#contentDisabled").css("color", "black")
        }
        else{
            $("#mergeReligion").attr("disabled", true)
            $("#contentDisabled").css("color", "#9e9e9e")

        }
    });
});