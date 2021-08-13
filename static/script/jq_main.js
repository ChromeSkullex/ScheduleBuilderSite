$(function(){
    console.log("Please just work")
    $(".subButton").click(function() {
        console.log("Hey ")
        console.log($('.meet:checkbox:checked').length)
        if($(this).find('.meet:checkbox:checked').length > 0){
            console.log("HEY HYE")
            $("#validate").show();
        }
        //checkedList = $("input[type=checkbox]:checked").length;
        /*
        console.log(checkedList)

        if(!checkedList) {
            console.log("Hey 2")
            $("#validate").show();
            return false;
        }*/
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