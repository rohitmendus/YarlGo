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

function profile_change_img(e) {
    let filePath = URL.createObjectURL(event.target.files[0]); 
    document.getElementById("profile-pic-img").src = filePath;
}

$(document).ready(function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })

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
        if (elem.style.color==="red"){
            $('#edit-user-btn').attr('disabled', true);
        } else {
            $('#edit-user-btn').attr('disabled', false);
        }
    });

    $(document).on('submit', '#create-user-form', function(e){
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
        const url = ed$(this).attr('href');
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
        let topic_questions = parseInt($(this).closest('tr').children('.topic-questions').html())
        if (topic_questions !== 0) {
            let elem = $('#edit-topic-fail span')
            elem.empty();
            elem.html("You can't delete this topic without deleting all the questions in this topic. Click 'Delete All Questions' to delete all the questions.");
            $('#edit-topic-fail').removeClass('d-none');
        } else {
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
        }
    });

    $(document).on('click', '.dlt-questions-topic', function(e){
        const url = $(this).attr('href');
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        e.preventDefault()
        b_modal = $('#message-modal1')
        b_modal.modal('show');
        $('#confirm-dlt1').click(function(){
            $.ajax({
                url: url,
                data: {'csrfmiddlewaretoken': csrf_token},
                type: 'post',
                success: function(response){
                    b_modal.modal('hide');
                    refresh_table(response, $('#topic-table'), "topic-list-table")
                    // refresh_topic_table(response, $('#topic-table'));
                    $('#dlt-questions-topic-success').removeClass('d-none');
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
        b_modal = $('#message-modalqn');
        b_modal.modal('show');
        $('#confirm-dltqn').click(function(){
            $.ajax({
                url: url,
                data: {'csrfmiddlewaretoken': csrf_token},
                type: 'post',
                success: function(response){
                    b_modal.modal('hide');
                    refresh_table(response, $('#question-table'), "question-list-table")
                    // refresh_topic_table(response, $('#topic-table'));
                    $('#dlt-question-success').removeClass('d-none');
                }
            });
        })
    });
    $(document).on('click', '.edit-question', function(e){
        const url = $(this).attr('href');
        e.preventDefault()
        $.get(url, function(response){
            $('#question-heading').text('Edit Question')
            $('#create-question').html(response);
        })
    });
    $(document).on('submit', '#edit-question-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                if (response.success) {
                    refresh_table(response.table_response, $('#question-table'), 'question-list-table');
                    $('#question-heading').text('Add Question')
                    $('#create-question').html(response.form_response);
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


    $(document).on('click', '#add-topic-distribution button', function(e){
        let topicDistForm = document.querySelectorAll(".topic-distribution")
        let container = document.querySelector("#topic-distribution-container")
        let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
        let formNum = parseInt($('#id_form-TOTAL_FORMS').val());


        let newForm = topicDistForm[0].cloneNode(true) //Clone the bird form
        let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

        formNum++ //Increment the form number
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum-1}-`) //Update the new form to have the correct form number
        btn = $(newForm).find('.topic-close');
        btn.removeClass('d-none');
        container.append(newForm) //Insert the new form at the end of the list of forms

        totalForms.setAttribute('value', `${formNum}`)
    });

    $(document).on('click', '.topic-close', function(e){
        let form = $(this).parent()
        let total = parseInt($('#id_form-TOTAL_FORMS').val());
        let formRegex = RegExp(`form-(\\d){1}-`,'g')
        if (total > 1){
            form.remove();
            var forms = $('.topic-distribution');
            $('#id_form-TOTAL_FORMS').val(forms.length);
            forms.each(function(index){
                let topic = $(this).find('.inputTestTopic1').val()
                let no_of_questions = $(this).find('.inputTestTopic2').val()
                $(this).html(
                    $(this).html().replace(formRegex, `form-${index}-`)
                );
                $(this).find('.inputTestTopic1').val(topic)
                $(this).find('.inputTestTopic2').val(no_of_questions)
            });
        }
    });

    $(document).on('submit', '#create-test-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                let submit_response = $('#create-test')
                submit_response.empty();
                submit_response.append(response.response1);
                refresh_table(response.response2, $('#test-table'), "test-list-table")
            }
        });
    });

    $(document).on('input', '.closing_date', function(){
        let val1 = $(this).closest('.row').find('.opening_date').val();
        let obj1 = moment(val1, "DD-MM-YYYY");
        let opening_date = obj1.toDate();
        let val2 = $(this).val();
        let obj2 = moment(val2, "DD-MM-YYYY");
        let closing_date = obj2.toDate();
        let btn = $(this).closest('form').find('input[type="submit"], button[type="submit"]')
        let help_text = $(this).closest('.row').find('.dateHelp')
        if (closing_date.getTime() <= opening_date.getTime()){
            help_text.show();
            btn.attr('disabled','disabled');
        } else {
            help_text.hide()
            btn.removeAttr('disabled');
        }
    });

    $(document).on('input', '.opening_date', function(){
        let val1 = $(this).closest('.row').find('.closing_date').val();
        let obj1 = moment(val1, "DD-MM-YYYY");
        let closing_date = obj1.toDate();
        let val2 = $(this).val();
        let obj2 = moment(val2, "DD-MM-YYYY");
        let opening_date = obj2.toDate();
        let btn = $(this).closest('form').find('input[type="submit"], button[type="submit"]')
        let help_text = $(this).closest('.row').find('.dateHelp')
        if (closing_date.getTime() <= opening_date.getTime()){
            help_text.show();
            btn.attr('disabled','disabled');
        } else {
            help_text.hide();
            btn.removeAttr('disabled');
        }
    });

    $(document).on('input', '.opening_time', function(){
        let val1 = $(this).closest('.row').find('.closing_time').val();
        let obj1 = moment(val1, "hh:mm a");
        let closing_time = obj1.toDate();
        let val2 = $(this).val();
        let obj2 = moment(val2, "hh:mm a");
        let opening_time = obj2.toDate();
        let btn = $(this).closest('form').find('input[type="submit"], button[type="submit"]')
        let help_text = $(this).closest('.row').find('.timeHelp')
        if (closing_time.getTime() <= opening_time.getTime()){
            help_text.show();
            btn.attr('disabled','disabled');
        } else {
            help_text.hide();
            btn.removeAttr('disabled');
        }
    });
    $(document).on('input', '.closing_time', function(){
        let val1 = $(this).closest('.row').find('.opening_time').val();
        let obj1 = moment(val1, "hh:mm a");
        let opening_time = obj1.toDate();
        let val2 = $(this).val();
        let obj2 = moment(val2, "hh:mm a");
        let closing_time = obj2.toDate();
        let btn = $(this).closest('form').find('input[type="submit"], button[type="submit"]')
        let help_text = $(this).closest('.row').find('.timeHelp')
        if (closing_time.getTime() <= opening_time.getTime()){
            help_text.show();
            btn.attr('disabled','disabled');
        } else {
            help_text.hide();
            btn.removeAttr('disabled');
        }
    });

    $(document).on('input', '.search-students', function(){
        let search_query = $(this).val().toLowerCase();
        let val;
        $('.add-students .list-group-item').each(function(index) {
            val = $(this).find('label').text().toLowerCase();
            if (val.indexOf(search_query) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });

    $(document).on('click', '.dlt-test', function(e){
        const url = $(this).attr('href');
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        e.preventDefault()
        b_modal = $('#message-modal2');
        b_modal.modal('show');
        $('#confirm-dlt2').click(function(){
            $.ajax({
                url: url,
                data: {'csrfmiddlewaretoken': csrf_token},
                type: 'post',
                success: function(response){
                    b_modal.modal('hide');
                    refresh_table(response, $('#test-table'), "test-list-table");
                    $('#dlt-test-success').removeClass('d-none');
                }
            });
        })
    });

    $(document).on('submit', '#edit-test-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                if (response.success) {
                    $('#test-container').html(response.template);
                    let table = $('#test-table')
                    const datatablesSimple = document.getElementById('test-list-table');
                    if (datatablesSimple) {
                        table = new simpleDatatables.DataTable(datatablesSimple);
                    }
                    htmx.process(document)
                    $('#edit-test-success').removeClass('d-none');
                    $('#edit-test-success').show();
                } else {
                    let elem = $('#edit-test-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#edit-test-fail').removeClass('d-none');
                    $('#edit-test-fail').show();
                }
            }
        });
    });

    let current_url = window.location.href
    if (current_url.includes('take_test')) {
        var sec;
        var timer;
        var ele = document.getElementById('test-timer');

        (function (){
            let result;
            test_started_on = moment(test_started_on, "MM/DD/YYYY, HH:mm:ss");
            let now = moment();
            seconds = moment.duration(now.diff(test_started_on)).asSeconds();
            if (seconds) {
                sec = seconds
            } else {
                sec = 0;
            }
            timer = setInterval(()=>{
                result = new Date(sec * 1000).toISOString().slice(11, 19);
                ele.innerHTML = result;
                sec ++;
            }, 1000)
        })()

        window.onbeforeunload = function(event) {
            let next_url = document.activeElement.href;
            // window.localStorage.setItem('timer', sec);
            if (next_url.includes('take_test')) {
                if (next_url.includes('submit')) {
                    // window.localStorage.removeItem("timer");
                }
                return
            }
            else {
                // window.localStorage.removeItem("timer");
                var s = "You have unsaved changes. Really leave?";

                event = event || window.event;

                // This is for all other browsers
                return s;
            }
        }

        // window.onunload = function(event) {
        //     $('#test-submit').submit();
        // }

        $(document).on('input', '.test-option', function(){
            let option = $(this).val();
            let question_id = $(this).data('question-id');
            let question_no = $(this).data('question-no');
            const data = {'option_choosen': option, 'question_id': question_id, 'question_no': question_no}
            $.post('/take_test/select_answer/', data);
        });
        $(document).on('click', '.clear-answer', function(){
            let question_id = $(this).data('question-id');
            let question_no = $(this).data('question-no');
            const data = {'question_id': question_id, 'question_no': question_no}
            $.post('/take_test/clear_answer/', data, function(response){
                $('.test-option').each(function(){
                    this.checked = false;  
                });
            });
        });

        $(document).on('click', '.question-marker', function(){
            let question_id = $(this).data('question-id');
            let question_no = $(this).data('question-no');
            if ($(this).data('marked') === false) {
                let data = {'question_id': question_id, 'question_no': question_no, 'mark': true}
                $.post('/take_test/mark_question/', data, function(response){
                    $('.question-marker').attr('data-bs-original-title', "Unmark").tooltip('show');
                    $('.question-marker').data('marked', true)
                    $('.unmark').hide();
                    $('.mark').show();
                });
            } else {
                let data = {'question_id': question_id, 'question_no': question_no, 'mark': false}
                $.post('/take_test/mark_question/', data, function(response){
                    $('.question-marker').attr('data-bs-original-title', "Mark for later").tooltip('show');
                    $('.question-marker').data('marked', false);
                    $('.mark').hide();
                    $('.unmark').show();
                });
            }
        });
        $(document).on('click', '#end-test-btn', function(){
            $.get('/take_test/get_info/', {}, function(response){
                $('#test-submit-info').html(response);
                $('#test-submit-modal').modal('show');
            });
        })
    }


    var today = new Date();
    today.setDate(today.getDate() - 6);
    var date = (today.getMonth()+1)+'/'+today.getDate()+'/'+today.getFullYear();
    $(function () {
        $('#datetimepickerfilter').datetimepicker({
            format: 'L',
            maxDate: date
        });
    });

    $(document).on('change.datetimepicker', '#datetimepickerfilter', function(){
        let date = $('#day-fiter').val();
        $.get('/faculty/get_question_date_graph/', {'from_date': date}, function(response){
            barGraph2.data.labels = response.labels
            barGraph2.data.datasets[0].data = response.data
            barGraph2.update();
        });
    });

    $(document).on('change', '#select-subject-bank', function(){
        let total = $("option:selected", this).data('total');
        let filled = $("option:selected", this).data('filled');
        let text = `${filled}/${total}`
        $('#bank-status').text(text);
    });
    $(document).on('change', '#select-subject-questions', function(){
        let num = $("option:selected", this).data('questions');
        $('#question-num').text(num);
    });

    $(document).on('submit', '#edit-profile-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = new FormData(this);
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            cache: false,
            contentType: false,
            processData: false,
            success: function(response){
                if (response.success) {
                    $('#profile-success').removeClass('d-none');
                } else {
                    let elem = $('#profile-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#profile-fail').removeClass('d-none');
                }
            }
        });
    });

    $(document).on('submit', '#change-password-form', function(e){
        e.preventDefault();
        const url = $(this).attr('action');
        const data = $(this).serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function(response){
                if (response.success) {
                    $('#change-pwd-success').removeClass('d-none');
                    $('#change-password-form').trigger("reset");
                } else {
                    let elem = $('#change-pwd-fail span')
                    elem.empty();
                    for (let error of response.errors) {
                        elem.append(error)
                    }
                    $('#change-pwd-fail').removeClass('d-none');
                }
            }
        });
    });
}); 
