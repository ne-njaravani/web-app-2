$(document).ready(function() {
    // Set the token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetup so that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $('.reaction').on('click', function() {
        var post_id = $(this).data('post-id');
        var reaction_type = $(this).data('reaction-type');
        console.log('Post ID:', post_id);
        console.log('Reaction Type:', reaction_type);
        handleReaction(post_id, reaction_type, $(this));
    });
});

function handleReaction(post_id, reaction_type, element) {
    $.ajax({
        url: '/reaction',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            post_id: post_id,
            reaction_type: reaction_type
        }),
        success: function(response) {
            console.log('Response:', response);
            if (response.status === 'OK') {
                var postElement = element.closest('.post');
                postElement.find('.like-count').text(response.likes);
                postElement.find('.dislike-count').text(response.dislikes);
                postElement.find('.like-users').text(response.like_users.join(', '));
            }
        },
        error: function(error) {
            console.log('AJAX Error:', error);
        }
    });
}