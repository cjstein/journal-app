(function($) {
    $('#add-form').click(function() {
        var index = $('#id_inline_test_models-TOTAL_FORMS').val()
        var newTable = $('#id_inline_test_models-__prefix__-DELETE').parents('table').clone()
        newTable.find(':input').each(function() {
            for (attr of ['name', 'id'])
                $(this).attr(
                    attr,
                    $(this).attr(attr).replace('__prefix__', index)
                )
        })
        newTable.insertBefore($(this))
        $('#id_inline_test_models-TOTAL_FORMS').val(
            parseInt($('#id_inline_test_models-TOTAL_FORMS').val()) + 1
        )
        newTable.slideDown()
    })
})($)
