jQuery(document).ready(function () {
    var table = $('#sample_1');

    /* Table tools samples: https://www.datatables.net/release-datatables/extras/TableTools/ */

    /* Set tabletools buttons and button container */

    var oTable = table.dataTable({
        "order": [
            [0, 'desc']
        ],

        "paging": false,

        "dom": "<'row' <'col-md-12'T>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>", // horizobtal scrollable datatable

        // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
        // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js).
        // So when dropdowns used the scrollable div should be removed.
        //"dom": "<'row' <'col-md-12'T>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",


    });

    var tableWrapper = $('#sample_1_wrapper'); // datatable creates the table wrapper by adding with id {your_table_jd}_wrapper

    $(".trigger", table.fnGetNodes()).popover({
        placement: 'bottom',
        html: true,
        trigger: "click",
        title: function () {
            return $(this).parent('.popover-markup').find('.head').html();
        },
        content: function () {
            return $(this).parent('.popover-markup').find('.content').html();
        }
    }).click(function (e) {
        e.preventDefault();
    });

    table.on('shown.bs.dropdown', function (e) {
        var $table = $(this),
            $menu = $(e.target).find('.dropdown-menu'),
            tableOffsetHeight = $table.offset().top + $table.height(),
            menuOffsetHeight = $menu.offset().top + $menu.outerHeight(true);

        if (menuOffsetHeight > tableOffsetHeight)
            $table.css("padding-bottom", menuOffsetHeight - tableOffsetHeight);
    });

    table.on('hide.bs.dropdown', function () {
        $(this).css("padding-bottom", 0);
    })
});