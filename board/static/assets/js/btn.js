$("#toggle-create-article").click(function() {
    if ($("#create-article").attr('hidden')) {
        $("#create-article").removeAttr('hidden');
    } else {
        $("#create-article").attr('hidden', true);
    }
});