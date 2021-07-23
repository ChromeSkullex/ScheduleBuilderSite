var instrName; // Full Name of Professor
var instrPhone; // Phone Number of Professor, make it valid
var instrEmail; // Valid Email only
var courseDesc; // Paragraph Text of course desc
var checkBoxM = document.getElementById("monday");


var syllabusJSON = '{"instructorInfo":{' +
    '"insName"}}'

function testFunction(){
    courseDesc = document.getElementById("cDescript").value;
    console.log(courseDesc);
}

function assignInput(pageNum){
    if (pageNum === 0){
        writeJSON();
    }
    if (pageNum === 1){
        writeJSONSche()
    }
}

function writeJSON() {
    const dictTest = {instructorInfo: {insName: "", insPhone: "", insEmail: ""}, courseInfo: {courseDesc: ""}};
    dictTest.instructorInfo.insName = document.getElementById("instructorName").value;
    dictTest.instructorInfo.insPhone = document.getElementById("instructorPhone").value;
    dictTest.instructorInfo.insEmail = document.getElementById("instructorEmail").value;
    dictTest.courseInfo.courseDesc = document.getElementById("cDescript").value;
    console.log(dictTest);
    downloadJSON(dictTest);
}

function writeJSONSche(){


}


function downloadJSON(dictData) {
    const dataJSON = JSON.stringify(dictData);
    const a = document.createElement('a');
    const file = new Blob([dataJSON],{type: 'application/json'})
    a.href = URL.createObjectURL(file);
    a.download = "SyllabusBuilder";
    console.log(a.download);
    a.click();

}

function addTime(checkDay){
    /*
    var test = document.getElementById(checkDay+"_time");

    if (document.getElementById(checkDay).checked){
        console.log(checkDay);

        test.style.display = "block"
    }

    else{
        console.log("uncheck")
        test.style.display = "none"

    }*/
}