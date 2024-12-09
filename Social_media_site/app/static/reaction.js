$(document).ready(function() {
    // Set the CSRF token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetup so that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $(".vote").on("click", function() {
        var button = $(this);
        var post_id = button.attr('id');
        var reaction_type = button.children("i").attr('id');

        $.ajax({
            url: '/reaction',
            type: 'POST',
            data: JSON.stringify({ post_id: post_id, reaction_type: reaction_type }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                if (response.status === 'OK') {
                    if (reaction_type === "like") {
                        button.find("#sup").text(" " + response.likes);
                    } else {
                        button.find("#sdown").text(" " + response.dislikes);
                    }
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});