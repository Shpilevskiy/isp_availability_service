var render_row = function(city, street, house, provider, provider_url, status){
    data = {
        city: city,
        street: street,
        house: house,
        provider: provider,
        url: provider_url,
        status: status 
    };
    var template = $('#connection-row-template').html();
    Mustache.parse(template);   // optional, speeds up future uses
    return Mustache.render(template, data);

};

$(document).ready(function($){
    var cityInput = $('#city-input');
    var streetInput = $('#street-input');

    var cityDatalist = $('#city-datalist');
    var streetDatalist = $('#street-datalist');

    var searchButton = $('#search-sumbit');
    var connectionsList = $('#connections-list');

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

    streetInput.on("keyup", function(e){
        // process alphanumerical characters only  
        if ( !(e.which >= 48  && e.which <= 90) )  {
             return;
        }
        street = $(this).val();
        city = cityInput.val();
        var ajax_url = '/api/streets?city=' + city + '&street_query=' + street;
        $.ajax(ajax_url,
            {
                crossDomain: true,
                success: function(result){
                    streetDatalist.empty();
                    result.streets.forEach(function(item, i, arr){
                        newOption = $('<option value=' + item + '>');
                        streetDatalist.append(newOption);
                    });
                }
            }
        );
    });

    searchButton.on("click", function(e){
        e.preventDefault();
        $('#connections-list .connection-row').remove();
    
        defaultData = {"connections": [
            {"city": "Минск", "street": "Карла Либнехта", "house": "98", "url": "http://byfly.by", "provider": "byfly", "status": "Хуй вам, а не XPON"},
            {"city": "Минск", "street": "Карла Либнехта", "house": "94", "url": "http://byfly.by", "provider": "byfly", "status": "Хуй вам, а не XPON"},
            {"city": "Минск", "street": "Карла Либнехта", "house": "96", "url": "http://byfly.by", "provider": "byfly", "status": "Хуй вам, а не XPON"}
                              ]};
      // city, street, house, provider, provider_url, status
        defaultData.connections.forEach(function(item, i, arr){
            var newRow = render_row(item.city, item.street, item.house, item.provider, item.url, item.status);
            connectionsList.append($(newRow));
        });
    });

});