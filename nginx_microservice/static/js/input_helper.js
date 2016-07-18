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

/** This function analyses whether the valid key
     *  (alpha numerical characters, backspace, delete keys)
     *  has been pressed . */

    var isValidInputKey = function (char_code) {
        var C_FULL_STOP = 46;
        var C_LATIN_CAPITAL_LETTER_Z = 90;
        var C_DELETE_KEY = 8;
        var C_BACKSPACE_KEY = 46;
        if ( !(char_code >= C_FULL_STOP  && char_code <= C_LATIN_CAPITAL_LETTER_Z) && char_code != C_DELETE_KEY && char_code != C_BACKSPACE_KEY)  {
             return false;
        }
        return true;
    };

    var cityInput = $('#city-input');
    var streetInput = $('#street-input');

    var searchButton = $('#search-sumbit');
    var connectionsList = $('#connections-list');

$(document).ready(function($){

    streetInput.keyup(function (event) {
       if (event.keyCode == 13){
           searchButton.click();
       }
    });

    searchButton.on("click", function(e){
        e.preventDefault();
        $('#connections-list').find('.connection-row').remove();

        var street = streetInput.val();
        var city = cityInput.val();
        var ajax_url = '/api/search?city=' + city + '&street=' + street;
        $.ajax(ajax_url,
            {
                crossDomain: true,
                success: function(result){
                    result.connections.forEach(function(item, i, arr){
                        console.log(item);
                        var newRow = render_row(result.city, result.street, item.house, item.provider, item.url, item.status);
                        connectionsList.append($(newRow));
                    });
                }
            }
        );
      // city, street, house, provider, provider_url, status

    });

});


streetInput.typeahead({
    hint: true,
    highlight: true,
    minLength: 1  //set minimal query length
},
{
  name: 'streets',
  limit: 100,
  source: function (query, p, process) {
        var city = cityInput.val();
        console.log(query, city);
        var ajax_url = '/api/streets?city=' + city + '&street_query=' + query;
        return $.get(ajax_url, function (data) {
            console.log(data.streets);
            return process(data.streets);
        });
  },
  templates: {
    empty: [
      '<div class="empty-message">',
        'К сожалению, не удается найти данную улицу, пожалуйста, проверьте, правильно ли введен город',
      '</div>'
    ].join('\n')
  }
});


cityInput.typeahead({
  hint: true,
  highlight: true
},
{
  name: 'streets',
  limit: 100,
  source: function (query, p, process) {
        console.log(query);
        var ajax_url = '/api/cities?q=' + query;
        return $.get(ajax_url, function (data) {
            console.log(data.cities);
            return process(data.cities);
        });
  },
  templates: {
    empty: [
      '<div class="empty-message">',
        'К сожалению, у нас нет такого города, пожалуйста, попробуйте проверить правильность написания =(',
      '</div>'
    ].join('\n')
  }
});
