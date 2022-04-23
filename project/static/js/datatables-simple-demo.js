// window.addEventListener('DOMContentLoaded', event => {
//     // Simple-DataTables
//     // https://github.com/fiduswriter/Simple-DataTables/wiki

//     const datatablesSimple = document.getElementById('datatablesSimple');
//     if (datatablesSimple) {
//         new simpleDatatables.DataTable(datatablesSimple);
//     }
// });
// $(document).on('DOMContentLoaded', event => {
//     // Simple-DataTables
//     // https://github.com/fiduswriter/Simple-DataTables/wiki

    
// });

$(document).ready(function(){
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        var table = new simpleDatatables.DataTable(datatablesSimple);
    }
    $("#role-filter").on('change', function() {
        table.search(this.value);
    }); 
});
