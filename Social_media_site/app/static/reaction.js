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

    $(".reaction").on("click", function() {
        var button = $(this);
        var post_id = button.data('post-id');
        var reaction_type = button.data('reaction-type');

        $.ajax({
            url: '/reaction',
            type: 'POST',
            data: JSON.stringify({ post_id: post_id, reaction_type: reaction_type }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                if (response.status === 'OK') {
                    button.closest('.post').find("#sup").text(" " + response.likes);
                    button.closest('.post').find("#sdown").text(" " + response.dislikes);
                    button.closest('.post').find(".like-users").html(response.like_users.join(', '));
                }
            },
            error: function(error) {
                if (error.status === 401) {
                    window.location.href = '/login';
                } else {
                    console.log(error);
                }
            }
        });
    });
});