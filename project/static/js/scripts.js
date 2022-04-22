window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

$(document).ready(function(){
    $('#username-error').on('DOMSubtreeModified', function(){
        let elem = $(this).children('span')[0];
        if (elem.style.color==="red"){
            $('#create-user-btn').attr('disabled', true);
        } else {
            $('#create-user-btn').attr('disabled', false);
        }
    });
});
