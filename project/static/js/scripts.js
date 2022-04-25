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

function refresh_user_table(response){
    let table = $('#user-table');
    table.empty();
    table.append(response);
    const datatablesSimple = document.getElementById('user-list-table');
    if (datatablesSimple) {
        table = new simpleDatatables.DataTable(datatablesSimple);
    }
    $("#role-filter").on('change', function() {
        table.search(this.value);
    });  
}

$(document).ready(function(){
    $('#username-error').on('DOMSubtreeModified', function(){
        let elem = $(this).children('span')[0];
        if (elem.style.color==="red"){
            $('#create-user-btn').attr('disabled', true);
        } else {
            $('#create-user-btn').attr('disabled', false);
        }
    });

    $(document).on('DOMSubtreeModified', '#username-edit-error', function(){
        let elem = $(this).children('span')[0];
        console.log(elem)
        if (elem.style.color==="red"){
            $('#edit-user-btn').attr('disabled', true);
        } else {
            $('#edit-user-btn').attr('disabled', false);
        }
    });

    $('#create-user-form').on('submit', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-user')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_user_table(response.response2)
                htmx.process(document)
            }
        });
    });

    $(document).on('click', '.dlt-user', function(e){
        const url = $(this).attr('href');
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        e.preventDefault()
        b_modal = $('#message-modal')
        b_modal.modal('show');
        $('#confirm-dlt').click(function(){
            $.ajax({
                url: url,
                data: {'csrfmiddlewaretoken': csrf_token},
                type: 'post',
                success: function(response){
                    b_modal.modal('hide');
                    refresh_user_table(response);
                    $('#dlt-user-success').removeClass('d-none');
                }
            });
        })
    });

    $('.close-alert').click(function(){
        $(this).parent().addClass('d-none');
    });

    $(document).on('submit', '#edit-user-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-user-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_user_table(response.table_response)
                    $('#edit-user-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-user-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-user-fail').removeClass('d-none');
                }
                htmx.process(document)
            }
        });
    });
});
