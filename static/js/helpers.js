$(document).ready(function() {

    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();


    // daily checkbox toggle
    $('#checkboxList').on('click', '.card', function() {
        var dataId = $(this).data('id');
        var context = {
            url: '/' + dataId + '/checked/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataId,
            },
            type: 'post',
            success: function() {
                var item = $('#dailyCheckbox[data-id="' + dataId + '"]');
                item.toggleClass('checked');
            },
        }

        $.ajax(context);
    });


    $('#reset').click(function() {
        var context = {
            url: '/daily_reset/',
            success: function(response) {
                var list = response.checkbox_list;
                for (item in list) {
                    $('#dailyCheckbox[data-id="' + list[item].id + '"]').removeClass('checked');
                }              
            }
        }

        $.ajax(context);
    });



    // change birthday
    $('#change_birthday_btn').click(function(event) {
        event.preventDefault();
        var form_data = $('#change_birthday_form').serialize();
        var context = {
            url: '/settings/change_birthday/',
            data: form_data,
            type: 'post',
            success: function(response) {
                document.getElementById('change_birthday_response').innerHTML = response["response"];                          
            }
        }
        
        $.ajax(context);
    });



    // daily checkbox management
    // add task
    $('#add_task').click(function(event) {
        event.preventDefault();
        var form_data = $('#add_task_form').serialize();
        var context = {
            url: '/settings/add_task/',
            data: form_data,
            type: 'post',
            success: function(response) {
                var task = response["task"]; 
                $('#settingCheckboxList').append('<div class="setting-card" id="settingCheckbox" data-id="' + task.id +'"><div class="setting-card-body">' + task.task +'</div><button type="button" class="btn-close" data-id="' + task.id +'"></button></div>');      
            }
        }

        $.ajax(context);

        $('#add_task_form')[0].reset();
    });

    // delete task
    $('#settingCheckboxList').on('click', 'button.btn-close', function(event) {
        event.stopPropagation();
        var dataId = $(this).data('id');
        console.log(dataId);
        var context = {
            url: '/settings/delete_task/'+ dataId + '/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataId,
            },
            type: 'post',
            success: function(response) {
                $('#settingCheckbox[data-id="' + dataId + '"]').hide();                             
            }
        }

        $.ajax(context);
    });
    


    // calendar items management
    $('#add_calendar_btn').click(function(event) {
        event.preventDefault();
        var form_data = $('#add_calendar_form').serialize();
        var context = {
            url: '/settings/add_calendar/',
            data: form_data,
            type: 'post',
            success: function(response) {
                document.getElementById('add_calendar_response').innerHTML = response["response"];     
            }
        }

        $.ajax(context);

        $('#add_calendar_form')[0].reset();
    });


    // open dialog
    $('.calendar-item').click(function() {
        var dataId = $(this).data('id');
        var context = {
            url: '/calendar/open_dialog/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                date: dataId,
            },
            type: 'post',
            success: function(response) {
                document.getElementById('date_title').innerHTML = dataId;
                var morning = document.getElementById('morning_task');
                var afternoon = document.getElementById('afternoon_task');
                var evening = document.getElementById('evening_task');
                if (response["morning_task"]) {
                    var x = response["morning_task"];
                    morning.innerHTML = '<div class="detail-title">' + x.task_title + '</div><div class="detail-content">' + x.task_content + '</div>';
                }
                else { morning.innerHTML = "" }
                if (response["afternoon_task"]) {
                    var x = response["afternoon_task"];
                    afternoon.innerHTML = '<div class="detail-title">' + x.task_title + '</div><div class="detail-content">' + x.task_content + '</div>';
                }
                else { afternoon.innerHTML = "" }
                if (response["evening_task"]) {
                    var x = response["evening_task"];
                    evening.innerHTML = '<div class="detail-title">' + x.task_title + '</div><div class="detail-content">' + x.task_content + '</div>';
                }
                else { evening.innerHTML = "" }
            }
        }

        $.ajax(context);
        $('.dialog').show();
        
    });

    //close dialog
    $('.dialog').on('click', '.btn-close', function(event) {
        event.stopPropagation();
        $('.dialog').hide();
    });

});