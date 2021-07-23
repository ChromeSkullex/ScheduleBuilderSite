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