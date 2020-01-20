$(document).ready(function(){
  $('#datepickerStart, #datepickerEnd').datepicker({
    autoclose: true,
    todayHighlight: true,
    format: 'dd/mm/yyyy',
  });
  $('#timepickerStart, #timepickerEnd').timepicker({
    'timeFormat': 'H:i',
    'minTime': '06:00',
    'maxTime': '23:00'
  });

  $(document).on('submit','form',function(e){
    const date_start = $('#datepickerStart');
    const date_end = $('#datepickerEnd');
    const ds = new Date(date_start.val().split('/').reverse().join('-'))
    const de = date_end.val() ? new Date(date_end.val().split('/').reverse().join('-')) : null

    const time_start = $('#timepickerStart');
    const time_end = $('#timepickerEnd');
    const ts = new Date(date_start.val().split('/').reverse().join('-') + ' ' + time_start.val())
    const te = new Date(date_start.val().split('/').reverse().join('-') + ' ' + time_end.val())

    let is_date_valid = false;
    let is_time_valid = false;

    e.preventDefault();
    e.stopPropagation();
    if (ds && de && ds > de) {
      date_start.val('')
      date_end.val(' ')
      date_start.addClass('is-invalid');
      date_end.addClass('is-invalid');
      is_date_valid = false;
    }
    else {
      date_start.removeClass('is-invalid');
      date_end.removeClass('is-invalid');
      is_date_valid = true;
    };
    if (ts && te && ts > te) {
      time_start.val('')
      time_end.val(' ')
      time_start.addClass('is-invalid');
      time_end.addClass('is-invalid');
      is_time_valid = false;
    }
    else {
      time_start.removeClass('is-invalid');
      time_end.removeClass('is-invalid');
      is_time_valid = true;
    };

    const self = this;
    if (location.pathname.slice(-5) === 'event') {
      $.ajax({
        url: '/events/check_quantity',
        type: 'POST',
        data: {
          place: $('#placeSelect').val(),
          ticket_quantity: $('#ticketQuantity').val(),
        },
        success: function(result) {
          if (is_date_valid) {
            $('#ticketQuantity').removeClass('is-invalid')
            self.submit()
          }
        },
        error: function(r) {
          $('#ticketQuantity').val(' ')
          $('#ticketQuantity').addClass('is-invalid')
        }
    });
    }
    else {
      if (is_date_valid && is_time_valid){
        self.submit()
      }
    }


 });

 $('.btn-delete').click(function(e) {
   const event_id = Number(this.getAttribute('data-id'));
   $.ajax({
    url: '/events/' + event_id,
    type: 'DELETE',
    success: function(result) {
      location.reload();
    }
});
 })
})


