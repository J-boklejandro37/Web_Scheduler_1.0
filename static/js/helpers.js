$(document).ready(function() {

    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    /*
    [ IMPORTANT ]
     There're two ways of changing a webpage.
     1. "href" in the tag: Redirect to another url, will reload the page
     2. "event" happening: Redirect to another url, won't reload the page, only change partial content
     Both pass the parameter in the url if there's a need.

    [ jQuery Selector ]
     1. $('#id_value'): Get element by id
     2. $('.class_name'): Get element by class
     3. $(element): Get the element, typically $(this), can also use $('div'), it will get the first <div></div>
     4. $(element).attr('attr_name'): Get attribute value by attribute name, ex: class, id, data-id
     5. $(element).data('name'): Get attribute value whose name is with "data-" prefix

    [ AJAX URL rule ]
     1. url: '/scheduler/daily/daily_reset/' -> use root
     2. url: 'daily_reset/' -> relative to current url, result's the same
    */

    // daily checkbox toggle
    // Only trigger when clicking inside the <div class="class"></div>, within <div id="checkboxList"></div> area
    $('#checkboxList').on('click', '.card', function() {
        var dataId = $(this).data('id'); // Get data-id value of this element
        var context = {
            // dataId is passed in as parameter to def check(request, id=None) in views.py
            url: dataId + '/checked/',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            type: 'post',
            success: function() {
                var item = $('#dailyCheckbox[data-id="' + dataId + '"]');
                item.toggleClass('checked');
            },
        }

        $.ajax(context);
    });

    /*
    [IMPORTANT]: If there's no need to change the database, use without AJAX

    $('#checkboxList').on('click', '.card', function() {
        var dataId = $(this).data('id');
        var item = $('#dailyCheckbox[data-id="' + dataId + '"]');
        item.toggleClass('checked');
    });
    */

    $('#reset').click(function() {
        var context = {
            url: 'daily_reset/',
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            type: 'post',
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
            url: 'change_birthday/',
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
    $('#add_task_form').submit(function(event) {
        event.preventDefault(); // Stop the default form submission
        
        var form_data = $(this).serialize();
        var context = {
            url: 'add_task/',
            data: form_data,
            type: 'post',
            success: function(response) {
                var task = response["task"];
                $('#settingCheckboxList').append('<div class="setting-card" id="settingCheckbox" data-id="' + task.id +'"><div class="setting-card-body">' + task.task +'</div><button type="button" class="btn-close" data-id="' + task.id +'"></button></div>');      
            }
        };
    
        $.ajax(context);
        this.reset(); // Clear the form
        
        return false; // Extra insurance against form submission
    });

    // delete task
    $('#settingCheckboxList').on('click', 'button.btn-close', function(event) {
        event.stopPropagation();
        var dataId = $(this).data('id');
        console.log(dataId);
        var context = {
            url: 'delete_task/'+ dataId + '/',
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
            url: 'add_calendar/',
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
            url: 'open_dialog/',
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