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
    htmx.process(document)
}
function refresh_table(response, table, table_id){
    table.empty();
    table.append(response);
    const datatablesSimple = document.getElementById( table_id );
    console.log(table_id);
    console.log(datatablesSimple)
    if (datatablesSimple) {
        table = new simpleDatatables.DataTable(datatablesSimple);
    }
    $("#topic-filter").on('change', function() {
        table.search(this.value);
    });
    htmx.process(document)
}
function refresh_batch_timing_table(response, table) {
    table.empty();
    table.append(response);
    const datatablesSimple = document.getElementById('batch-timing-list-table');
    if (datatablesSimple) {
        table = new simpleDatatables.DataTable(datatablesSimple);
    }
    $("#batch-filter").on('change', function() {
        table.search(this.value);
    });
    htmx.process(document)
}


$(document).ready(function(){
    $('.pwd-eye').click(function(){
        $(this).hide();
        $(this).siblings().show();
        if ($(this).data('state') == 1) {
            $('#inputLoginPassword').attr('type', 'text');
        } else {
            $('#inputLoginPassword').attr('type', 'password');
        }
    });

    $(document).on('DOMSubtreeModified', '#username-error', function(){
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
                // htmx.process($('#create-user'))
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
                // htmx.process(document)
            }
        });
    });

    $(document).on('submit', '#create-exam-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-exam')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#exam-table'), "exam-list-table")
                // refresh_exam_table(response.response2, $('#exam-table'))
                // htmx.process($('#create-user'))
            }
        });
    });

    $(document).on('click', '.dlt-exam', function(e){
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
                    refresh_table(response, $('#exam-table'), "exam-list-table")
                    // refresh_exam_table(response, $('#exam-table'));
                    $('#dlt-exam-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-exam-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-exam-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_table(response.table_response, $('#exam-table'), "exam-list-table")
                    // refresh_exam_table(response.table_response, $('#exam-table'))
                    $('#edit-exam-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-exam-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-exam-fail').removeClass('d-none');
                }
                // htmx.process(document)
            }
        });
    });

    $(document).on('submit', '#create-exam-cat-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-exam-cat')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#exam-cat-table'), "exam-list-table");
            }
        });
    });

    $(document).on('click', '.dlt-exam-cat', function(e){
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
                    refresh_table(response, $('#exam-cat-table'), "exam-list-table")
                    // refresh_exam_table(response, $('#exam-cat-table'));
                    $('#dlt-exam-cat-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-exam-cat-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-exam-cat-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_table(response.table_response, $('#exam-cat-table'), "exam-list-table");
                    $('#edit-exam-cat-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-exam-cat-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-exam-cat-fail').removeClass('d-none');
                }
                // htmx.process(document)
            }
        });
    });

    $(document).on('submit', '#create-subject-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-subject')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#subject-table'), 'subject-list-table')
                // refresh_subject_table(response.response2, $('#subject-table'))
                // htmx.process($('#create-user'))
            }
        });
    });

    $(document).on('click', '.dlt-subject', function(e){
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
                    refresh_table(response, $('#subject-table'), 'subject-list-table')
                    // refresh_subject_table(response, $('#subject-table'));
                    $('#dlt-subject-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-subject-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-subject-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_table(response.table_response, $('#subject-table'), 'subject-list-table')
                    // refresh_subject_table(response.table_response, $('#subject-table'))
                    $('#edit-subject-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-subject-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-subject-fail').removeClass('d-none');
                }
            }
        });
    });

    $(document).on('submit', '#create-batch-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-batch')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#batch-table'), 'batch-list-table')
                // refresh_admin_batch_table(response.response2, $('#batch-table'));
            }
        });
    });

    $(document).on('click', '.dlt-batch', function(e){
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
                    refresh_table(response, $('#batch-table'), 'batch-list-table')
                    // refresh_admin_batch_table(response, $('#batch-table'));
                    $('#dlt-batch-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-batch-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-batch-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_table(response.table_response, $('#batch-table'), 'batch-list-table')
                    // refresh_admin_batch_table(response.table_response, $('#batch-table'))
                    $('#edit-batch-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-batch-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-batch-fail').removeClass('d-none');
                }
            }
        });
    });

    $(document).on('submit', '#create-batch-timing-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-batch-timing')
                submit_response.empty();
                submit_response.append(response.response1);
                // refresh_table(response.response2, $('#batch-timing-table'), 'batch-timing-list-table');
                refresh_batch_timing_table(response.response2, $('#batch-timing-table'));
            }
        });
    });

    $(document).on('click', '.dlt-batch-timing', function(e){
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
                    // refresh_table(response, $('#batch-timing-table'), 'batch-timing-list-table');
                    refresh_batch_timing_table(response, $('#batch-timing-table'));
                    $('#dlt-batch-timing-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-batch-timing-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-batch-timing-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    // refresh_table(response.table_response, $('#batch-timing-table'), 'batch-timing-list-table');
                    refresh_batch_timing_table(response.table_response, $('#batch-timing-table'))
                    $('#edit-batch-timing-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-batch-timing-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-batch-timing-fail').removeClass('d-none');
                }
            }
        });
    });

    $('#faculty-nav a').on('click', function (e) {
        $(this).tab('show')
    })
    var url = window.location.href;
    var activeTab = url.substring(url.indexOf("#") + 1);
    $('#faculty-nav a[href="#'+ activeTab +'"]').tab('show');
    
    $('.subject-operate-btn').click(function(e){
        e.preventDefault();
        const subject_id = $(this).data('subject');
        const url = $(this).attr('href');
        $.ajax({
            url: '/subjects/store_subject/',
            data: {'subject_id': subject_id},
            type: 'get',
            success: function(){
                window.location.replace(url);
            }
        });
    });

    $(document).on('submit', '#create-topic-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-topic')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#topic-table'), "topic-list-table")
                // refresh_topic_table(response.response2, $('#topic-table'));
            }
        });
    });

    $(document).on('click', '.dlt-topic', function(e){
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
                    refresh_table(response, $('#topic-table'), "topic-list-table")
                    // refresh_topic_table(response, $('#topic-table'));
                    $('#dlt-topic-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-topic-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-topic-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_table(response.table_response, $('#topic-table'), 'topic-list-table');
                    $('#edit-topic-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-topic-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-topic-fail').removeClass('d-none');
                }
            }
        });
    });

    $(document).on('submit', '#create-question-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-question')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#question-table'), "question-list-table")
            }
        });
    });

    $(document).on('click', '.dlt-question', function(e){
        const url = $(this).attr('href');
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        e.preventDefault()
        console.log("log 1")
        b_modal = $('#message-modal1');
        b_modal.modal('show');
        console.log(b_modal)
        $('#confirm-dlt1').click(function(){
            $.ajax({
                url: url,
                data: {'csrfmiddlewaretoken': csrf_token},
                type: 'post',
                success: function(response){
                    console.log("log 3")
                    b_modal.modal('hide');
                    refresh_table(response, $('#question-table'), "question-list-table")
                    // refresh_topic_table(response, $('#topic-table'));
                    $('#dlt-question-success').removeClass('d-none');
                }
            });
        })
    });
    $(document).on('submit', '#edit-question-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        const edit_modal = $('#edit-question-modal')
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                edit_modal.modal('hide');
                if (response.success) {
                    refresh_table(response.table_response, $('#question-table'), 'question-list-table');
                    $('#edit-question-success').removeClass('d-none');
                } else {
                    let elem = $('#edit-question-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-question-fail').removeClass('d-none');
                }
            }
        });
    });
}); 
