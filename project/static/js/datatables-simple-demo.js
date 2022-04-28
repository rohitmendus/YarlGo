htmx.onLoad(function(elt){
    const datatables = htmx.findAll(elt, ".datatablesSimple")
    for (datatableSimple of datatables) {
        if (datatableSimple) {
            var table = new simpleDatatables.DataTable(datatableSimple);
            htmx.process(datatableSimple);
        }
        $("#role-filter").on('change', function() {
            table.search(this.value);
        });
        $("#batch-filter").on('change', function() {
            table.search(this.value);
        });
    }
});
// $(document).ready(function(){
//     const datatables = $(".datatablesSimple");
//     for (datatableSimple of datatables) {
//         if (datatableSimple) {
//             var table = new simpleDatatables.DataTable(datatableSimple);
//             htmx.process(datatableSimple);
//         }
//         $("#role-filter").on('change', function() {
//             table.search(this.value);
//         });
//     } 
// });

