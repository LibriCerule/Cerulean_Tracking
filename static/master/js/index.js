function loadList(uuids) {
    var packages = [];

    for(var i = 0; i < uuids.length; i++) {
        $.getJSON("/package?uuid=" + uuids[i]).error(function(xhr) {
            packages.push($.parseJSON(xhr.responseText));
        });
    }

    var html = '<div class="list-group vfill">';
    for(var i = 0; i < packages.length; i++) {
        html += '<a href="#" class="list-group-item clearfix">'
                  + '<div class="package-item-title">' + packages[i].name + ' at ' + packages[i].lat + ', ' + packages[i].lon + '</div>'
            + '<div class="pull-right package-item-delete">'
                + '<button class="confirm-delete btn btn-md btn-error" id="hello" role="button" data-id="1">'
                    + '<span class="glyphicon glyphicon-trash"></span>'
                + '</button>'
            + '</div>'
        + '</a>'
    }
    html += '</div>';

    $('#sidebar').append(html);

        // Temporary sidebar appends (TESTING ONLY)
        $('#sidebar').append('<div class="list-group vfill">'
        + '<a href="#" class="list-group-item clearfix">'
            + '<div class="package-item-title">Lorem Ipsum jest tekstem stosowanym jako przykładowy wypełniacz w przemyśle poligraficznym.</div>'
            + '<div class="pull-right package-item-delete">'
                + '<button class="confirm-delete btn btn-md btn-error" id="hello" role="button" data-id="1">'
                    + '<span class="glyphicon glyphicon-trash"></span>'
                + '</button>'
            + '</div>'
        + '</a>'
        + '<a href="#" class="list-group-item clearfix">'
            + '<div class="package-item-title">Został po raz pierwszy użyty w XV w.</div>'
            + '<div class="pull-right package-item-delete">'
                + '<button class="confirm-delete btn btn-md btn-error" id="hello" role="button" data-id="1">'
                    + '<span class="glyphicon glyphicon-trash"></span>'
                + '</button>'
            + '</div>'
        + '</a>'
        + '<a href="#" class="list-group-item clearfix">'
            + '<div class="package-item-title">Pięć wieków później zaczął być używany przemyśle elektronicznym, pozostając praktycznie niezmienionym.</div>'
            + '<div class="pull-right package-item-delete">'
                + '<button class="confirm-delete btn btn-md btn-error" id="hello" role="button" data-id="1">'
                    + '<span class="glyphicon glyphicon-trash"></span>'
                + '</button>'
            + '</div>'
        + '</a>'
        + '</div>');
}

function searchNavHeader() {
        $('#sideNavHeader').append('<div class="input-group">'
        + '<input type="search" name="search" class="form-control input-lg" placeholder="Package IDs, comma separated...">'
        + '<span class="input-group-btn">'
            + '<button type="button" class="btn btn-info btn-lg">'
                + '<span class="glyphicon glyphicon-search"></span>'
            + '</button>'
        + '</span>'
        + '</div>');
}

function itemNavHeader() {
        $('#sideNavHeader').append('<div>'
        + '<a href="#" class="navbar-brand glyphicon glyphicon-menu-left" id="backOverview"></a>'
            + '<span class="navbar-brand" id="packName">Package Name</span>'
        + '</div>');
}

$(document).ready(function() {
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

    $(document.body).on('click', '#backOverview', function() {
        $('#sideNavHeader').children()[0].remove();
        searchNavHeader();
        loadList(['de305d54-75b4-431b-adb2-eb6b9e546010']);
    });

    $(document.body).on('click', '#sidebar .list-group-item', function() {
        $('#sideNavHeader').children()[0].remove();
        itemNavHeader();
        $('#sidebar').children()[0].remove();

        $.getJSON("/package").error(function(xhr) {
            var data = $.parseJSON(xhr.responseText);
            var items = [];
            var lat = 0;
            var long = 0;
            $.each( data, function( key, val ) {
                if(key=='lat') lat=val;
                if(key=='lon') lon=val;
            });
        });
    });

    $(".map").html('<iframe class="hfill vfill bare" frameborder="0" src="https://maps.google.com/maps?q='+lat+','+long+'&hl=es;z=14&amp;output=embed"></iframe>');
    loadList(['de305d54-75b4-431b-adb2-eb6b9e546010']);
});
