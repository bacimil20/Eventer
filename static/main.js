$(document).ready(function(){
  $('#datepickerStart, #datepickerEnd').datepicker({
    autoclose: true,
    todayHighlight: true,
    format: 'dd/mm/yyyy',
  });


  $(document).on('submit','form',function(e){
    const date_start = $('#datepickerStart');
    const date_end = $('#datepickerEnd');
    const ds = new Date(date_start.val().split('/').reverse().join('-'))
    const de = new Date(date_end.val().split('/').reverse().join('-'))
    let to_submit = false;

    e.preventDefault();
    if (ds > de) {
      date_start.val('')
      date_end.val(' ')
      date_start.addClass('is-invalid');
      date_end.addClass('is-invalid');
      to_submit = false;
    }
    else {
      date_start.removeClass('is-invalid');
      date_end.removeClass('is-invalid');
      to_submit = true;
    };
    const self = this;
    $.ajax({
      url: '/events/check_quantity',
      type: 'POST',
      data: {
        place: $('#placeSelect').val(),
        ticket_quantity: $('#ticketQuantity').val(),
      },
      success: function(result) {
        if (to_submit) {
          $('#ticketQuantity').removeClass('is-invalid')
          self.submit()
        }
      },
      error: function(r) {
        $('#ticketQuantity').val(' ')
        $('#ticketQuantity').addClass('is-invalid')
      }
  });

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


