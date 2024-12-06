$(document).ready(function() {

    // Set the CSRF token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetupso that the CSRF token is added to the header of every request
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $(".like-button").on("click", function() {
        var button = $(this);

        // Which idea was clicked? Fetch the idea ID
        var reaction_id = button.attr('id');
        // Is it an upvote or downvote?
        var reaction_type = button.children()[0].id;

        $.ajax({
            url: '/like',
            type: 'POST',
            data: JSON.stringify({ idea_id: idea_id, reaction_type: reaction_type}),
      // We are using JSON, not XML
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);

                // Update the html rendered to reflect new count
                // Check which count to update
                if(vote_type == "like") {
                    clicked_obj.children()[1].innerHTML = " " + response.like;
                } else {
                    clicked_obj.children()[1].innerHTML = " " + response.dislike;
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});