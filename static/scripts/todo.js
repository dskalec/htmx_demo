$(document).ready(function() {
  $('.todo-completed-checkbox').change(function () {
    let todoId = $(this).data('id');
    let completed = $(this).is(':checked');

    $.ajax({
      url: `/ajax-complete/${todoId}/`,
      method: 'POST',
      data: {
        'completed': completed,
      },
      success: function (response) {
        if (response.status === 'ok') {
          let badge = $(`#badge-${todoId}`);
          if (completed) {
            badge.removeClass('bg-warning').addClass('bg-success')
                  .text(`Completed on ${response.completed_at}`);
          } else {
            badge.removeClass('bg-success').addClass('bg-warning')
                  .text('Not Completed');
          }
        }
      },
      error: function () {
        alert('There was an error updating the todo. Please try again.');
      }
    });
  });
});