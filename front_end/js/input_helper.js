$(document).ready(function($){
    var cityInput = $('#city-input');
    var streetInput = $('#street-input');


    var cityDatalist = $('#city-datalist');
    var streetDatalist = $('#street-datalist');

    cityInput.on("keyup", function(e){
        var ajax_url = 'http:127.0.0.1:8000/cities?q=' + $(this).val();
        $.ajax(ajax_url,
            {
                crossDomain: true,
                success: function(result){
                    cityDatalist.empty();
                    result.cities.forEach(function(item, i, arr){
                        console.log(item);
                        newOption = $('<option value=' + item + '>');
                        cityDatalist.append(newOption);
                    });
                }
            }
        );
    });
});