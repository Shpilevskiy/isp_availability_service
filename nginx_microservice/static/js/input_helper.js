$(document).ready(function($){
    var cityInput = $('#city-input');
    var streetInput = $('#street-input');


    var cityDatalist = $('#city-datalist');
    var streetDatalist = $('#street-datalist');

    cityInput.on("keyup", function(e){
        // process alphanumerical characters only  
        if ( !(e.which >= 48  && e.which <= 90) )  {
             return;
        }
       
        var ajax_url = '/api/cities?q=' + $(this).val();
        $.ajax(ajax_url,
            {
                crossDomain: true,
                success: function(result){
                    cityDatalist.empty();
                    result.cities.forEach(function(item, i, arr){
                        newOption = $('<option value=' + item + '>');
                        cityDatalist.append(newOption);
                    });
                }
            }
        );
    });
});