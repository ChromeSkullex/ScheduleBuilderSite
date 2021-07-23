/*
* jq -> Jquery cause I am indesisive
*
* */
/*
$(document).ready(function() {
    var formArr = $("form").serializeArray();
   $('form') .on('submit', function(event){
       console.log("wo")
       $.ajax({
          data : {
              meetings : $('#meetings').val()
          },
           type: 'POST',
           url : '/process'
       })
       .done(function (data) {
            if (data.error){
                console.log("Something")
                $('#error_sub').text(data.error).show();
            }
       });
       event.preventDefault();
   });
});*/



$('.AddNew').click(function(){
    var row = $(this).closest('baseTime');
    console.log("Cool")


});

//Credit to https://jsfiddle.net/vPatQ/
/*
*   WIP: This creates a new column when people want to add their class time
* Some may have different classes on the same day.
 */
$(document).on('click', '.AddNew', function(){
    // Changing ids after clone
    // Change tr, row_1 to row_2 (and increment)
    /* If needed
    var $tr = $('tr[id^="row_"]:last');
    var num = parseInt($tr.prop("id").match(/\d+/g), 10) + 1;

    console.log(num);
    */
   const row = $(this).closest('tr').clone();
   row.find('input').val('');
   $(this).closest('tr').after(row);
   $('input[type="button"]', row).removeClass('AddNew').addClass('RemoveRow').val('-');
});

/*
* WIP: This removes a row created by addNew
 */
$(document).on('click', '.RemoveRow', function(){
   $(this).closest('tr').remove();
});

/*
* SUBMIT
* Notes:
*   May need to turn this into an AJAX call for more efficiency but for now it will
*   submit a json
 */

$(document).ready(function(){
    $("#buildButton").click(function () {
        var arrayArgs = grabInformation();
        console.log(arrayArgs);
        createJSON(arrayArgs);
        //downloadJSON(arrayArgs);
        event.preventDefault();
    });
});

/*
*   grabInformation()
*   PARAMS: NONE
*   DESCRIPTION: Creates a serialized Array from form using 'name = ' and 'value = ' as its data
* returns a json
 */
function grabInformation(){
    // takes the form tag and creates an array automatically
    var formArr = $("form").serializeArray(), // an array
        dataObj = {}; // dataObj is the dict/json of all the data

    // Pushing formArr the data in the dataObj
    $(formArr).each(function(i,field){
        if (dataObj[field.name]){
            dataObj[field.name]  +=(" " + field.value); // Same name will be spaced

        }
        else {
            dataObj[field.name]  = field.value;  // Creates a new field and value

        }
    });
    // Meetings, numCols, landscape, turned into integer numbers
    if (dataObj["meetings"]){
        dataObj["meetings"] = dataObj["meetings"].split(" ");
        $(dataObj["meetings"]).each(function (j){
            dataObj["meetings"][j] = parseInt(dataObj["meetings"][j])
        });
    }
    dataObj["numCols"] = parseInt(dataObj["numCols"]);
    dataObj["landscape"] = parseInt(dataObj["landscape"]);


    /*
    $(formArr).each(function (index){
       console.log(index + ": " + $(this)[index].name)
    });*/
    return dataObj;
}
/*
*   createJSON()
*   PARAMS: serArr = serialized Array
*   DESCRIPTION: Creates a compatible json for the Syllabus Backend
* returns a json
 */
function createJSON(serArr){

}
/*
function downloadJSON(jsonData){

    const dataJSON = JSON.stringify(jsonData);
    const a = document.createElement('a');
    const file = new Blob([dataJSON],{type: 'application/json'})
    a.href = URL.createObjectURL(file);
    a.download = "Please Just Change";
    console.log(a.download);
    a.click();
}*/