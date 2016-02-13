window.pack_uuids = {};

function loadList(uuids) {
    if(window.pack_uuids.length == 0) return;

    var packages = [];

    for(var key in window.pack_uuids) {
        $.ajax({
            url: '/package?uuid=' + window.pack_uuids[key],
            dataType: 'json',
            async: false,
            success: function(data) {
                packages.push(data);
            }
        });
    }

    var pack_keys = Object.keys(window.pack_uuids);
    var html = '<div class="list-group vfill">';
    for(var i = 0; i < packages.length; i++) {
        html += '<a href="#" class="list-group-item clearfix" data-id="' + window.pack_uuids[pack_keys[i]] + '">'
                  + '<div class="package-item-title">' + packages[i].name + ' at ' + packages[i].lat + ', ' + packages[i].lon + '</div>'
            + '<div class="pull-right package-item-delete">'
                + '<button class="confirm-delete btn btn-md btn-error" id="hello" role="button" data-id="' + pack_keys[i] + '">'
                    + '<span class="glyphicon glyphicon-trash"></span>'
                + '</button>'
            + '</div>'
        + '</a>'
    }
    html += '</div>';

    if($('#sidebar').children().length > 0)
        $('#sidebar').children()[0].remove();
    $('#sidebar').append(html);
}

function searchNavHeader() {
        $('#sideNavHeader').append('<div class="input-group">'
        + '<input type="search" name="search" id="searchBar" class="form-control input-lg" placeholder="Package IDs, comma separated...">'
        + '<span class="input-group-btn">'
            + '<button type="button" class="btn btn-info btn-lg" id="searchBtn">'
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
    $(document.body).on('click', '.confirm-delete', function(e) {
        e.preventDefault();
        var id = $(this).data('id');
        $('#delConfModal').data('id', id).modal('show');
    });

    $(document.body).on('click', '#deleteYes', function() {
        var id = $('#delConfModal').data('id');
        $('[data-id=' + id + ']').parent().parent().remove();

        $('#delConfModal').modal('hide');
    });

    $(document.body).on('click', '#searchBtn', function() {
        var query = $('#searchBar').val();
        var uuids = $.map(query.split(','), $.trim);

        for(var i = 0; i < uuids.length; i++) {
            if($.inArray(uuids[i], window.pack_uuids) != -1)
                continue;
            window.pack_uuids['' + i] = uuids[i];
        }

        loadList();
    });

    $(document.body).on('click', '#backOverview', function() {
        $('#sideNavHeader').children()[0].remove();
        searchNavHeader();
        loadList();
    });

    $(document.body).on('click', '#sidebar .list-group-item .package-item-title', function() {
        var id = $(this).parent().data('id');

        $('#sideNavHeader').children()[0].remove();
        itemNavHeader();
        $('#sidebar').children()[0].remove();

        var lat = 0;
        var lon = 0;

        $.ajax({
            url: '/package?uuid=' + id,
            dataType: 'json',
            async: false,
            success: function(data) {
                var items = [];
                $.each( data, function( key, val ) {
                    if(key=='lat') lat=val;
                    if(key=='lon') lon=val;
                });
            }
        });

        $(".map").html('<iframe class="hfill vfill bare" frameborder="0" src="https://maps.google.com/maps?q='+lat+','+lon+'&hl=es;z=14&amp;output=embed"></iframe>');
    });

    loadList();
});
