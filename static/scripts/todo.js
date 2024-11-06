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

  $('.delete-todo-button').click(function() {
        /*if (!confirm('Are you sure you want to delete this task?')) {
            return; // Exit if the user cancels
        }*/
        let todoId = $(this).data('id');

        $.ajax({
            url: `/ajax-delete/${todoId}/`,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.status === 'ok') {
                    $(`li:has(button[data-id="${todoId}"])`).remove();
                } else {
                    alert('There was an error deleting the todo. Please try again.');
                }
            },
            error: function() {
                alert('There was an error deleting the todo. Please try again.');
            }
        });
    });

    $('.edit-todo-button').click(function() {
        let todoId = $(this).data('id');
        let todoContent = $(`#todo-${todoId} .todo-content`);
        let title = todoContent.find('.todo-title').text().trim();
        let description = todoContent.find('.todo-description').text().trim();

        // Replace content with input fields for editing
        todoContent.html(`
            <input type="text" class="form-control mb-1 edit-todo-title" value="${title}">
            <textarea class="form-control mb-1 edit-todo-description">${description}</textarea>
            <button class="btn btn-success btn-sm save-todo-button" data-id="${todoId}">Save</button>
            <button class="btn btn-secondary btn-sm cancel-edit-button" data-id="${todoId}">Cancel</button>
        `);
    });

    // Handle save event for editing todos
    $(document).on('click', '.save-todo-button', function() {
        let todoId = $(this).data('id');
        let title = $(`#todo-${todoId} .edit-todo-title`).val();
        let description = $(`#todo-${todoId} .edit-todo-description`).val();

        $.ajax({
            url: `/ajax-edit/${todoId}/`,
            method: 'POST',
            data: {
                'title': title,
                'description': description,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.status === 'ok') {
                    let todoContent = $(`#todo-${todoId} .todo-content`);
                    // Update the DOM with new values
                    todoContent.html(`
                        <h5 class="mb-1 todo-title">${title}</h5>
                        <p class="mb-1 text-muted todo-description">${description}</p>
                    `);
                } else {
                    alert('There was an error saving the changes. Please try again.');
                }
            },
            error: function() {
                alert('There was an error saving the changes. Please try again.');
            }
        });
    });

    // Handle cancel edit event
    $(document).on('click', '.cancel-edit-button', function() {
        let todoId = $(this).data('id');
        let todoContent = $(`#todo-${todoId} .todo-content`);
        let title = todoContent.find('.edit-todo-title').val();
        let description = todoContent.find('.edit-todo-description').val();

        // Restore the original content
        todoContent.html(`
            <h5 class="mb-1 todo-title">${title}</h5>
            <p class="mb-1 text-muted todo-description">${description}</p>
        `);
    });
});