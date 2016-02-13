$(document).ready(function() {
    $('#sidebar').append('<a href="#" class="list-group-item clearfix">'
  + '<div class="package-item-title">Lorem Ipsum jest tekstem stosowanym jako przykładowy wypełniacz w przemyśle poligraficznym.</div>'
  + '<div class="pull-right package-item-delete">'
      + '<button class="confirm-delete btn btn-md btn-error" id="hello" role="button" data-id="1">'
          + '<span class="glyphicon glyphicon-trash"></span>'
      + '</button>'
  + '</div>'
  + '</a>');

  $('.confirm-delete').on('click', function(e) {
      e.preventDefault();
      var id = $(this).data('id');
      $('#delConfModal').data('id', id).modal('show');
  });

  $('#deleteYes').click(function() {
      var id = $('#delConfModal').data('id');
      $('[data-id=' + id + ']').parent().parent().remove();
      $('#delConfModal').modal('hide');
  });

  $('#delConfModal').on('show', function() {
 var id=$(this).data('id');document.write(id);
});
                  
  $('.list-group-item').on('click', function() {
                           $.getJSON( "/package", function( data ) {
                                     var items = [];
                                     var lat = 0;
                                     var long = 0;
                                     $.each( data, function( key, val ) {
                                            if(key=='lat') lat=val;
                                            if(key=='lon') lon=val;
                                            });
                                     
                                     $(".map").html('<iframe class="hfill vfill bare" frameborder="0" src="https://maps.google.com/maps?q='+lat+','+long+'&hl=es;z=14&amp;output=embed"></iframe>');
                                     }
                                     });
  }
});



/*
Lorem Ipsum jest tekstem stosowanym jako przykładowy wypełniacz w przemyśle poligraficznym. Został po raz pierwszy użyty w XV w. przez nieznanego drukarza do wypełnienia tekstem próbnej książki. Pięć wieków później zaczął być używany przemyśle elektronicznym, pozostając praktycznie niezmienionym. Spopularyzował się w latach 60. XX w. wraz z publikacją arkuszy Letrasetu, zawierających fragmenty Lorem Ipsum, a ostatnio z zawierającym różne wersje Lorem Ipsum oprogramowaniem przeznaczonym do realizacji druków na komputerach osobistych, jak Aldus PageMaker
*/
