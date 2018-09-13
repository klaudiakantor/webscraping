function isEmptyTable(data){

var table = document.getElementsByName('my_table');
if (data.length=0)
    table.style.display = 'none';
}


function set_dates() {


    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }

    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("datefield").setAttribute("min", today);
    document.getElementById("datefield").setAttribute("max", today + 14);
}