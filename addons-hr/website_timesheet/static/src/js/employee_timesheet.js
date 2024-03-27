
'use strict';
$(document).ready(function () {
    $('#project_id').on('change', function () {
        var project_id = $(this).val();
        $.ajax({
            url: "/get_task_options",
            type: "POST",
            dataType: "json",
            data: { project_id: project_id },
            success: function (options) {
                $('#task_id').empty();
                options.forEach(function (option) {
                    $('#task_id').append($('<option>', {
                        value: option.id,
                        text: option.name
                    }));
                });
            },
            error: function (xhr, status, error) {
                console.error("Error fetching task options:", error);
            }
        });
    });
});
