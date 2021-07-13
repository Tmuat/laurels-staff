$('#hub-select').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();

    if(selectedVal == "reset"){
        currentUrl.searchParams.delete("hub");
    } else {
        currentUrl.searchParams.set("hub", selectedVal);
    }

    window.location.replace(currentUrl);
})

$('#employee-select').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();

    if(selectedVal == "reset"){
        currentUrl.searchParams.delete("user");
    } else {
        currentUrl.searchParams.set("user", selectedVal);
    }

    window.location.replace(currentUrl);
})