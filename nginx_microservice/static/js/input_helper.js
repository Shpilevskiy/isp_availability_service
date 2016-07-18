var cityInput = $('#city-input');
var streetInput = $('#street-input');

var searchButton = $('#search-sumbit');
var connectionsList = $('#connections-list');

$(document).ready(function($){

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
                        var newRow = render_row(result.city, result.street, item.house, item.provider, item.url, item.status);
                        connectionsList.append($(newRow));
                    });
                }
            }
        );
      // city, street, house, provider, provider_url, status

    });

});

cityInput.typeahead({
  hint: true,
  highlight: true
},
{
  name: 'cities',
  limit: 100,
  source: function (query, p, process) {
        var ajax_url = '/api/cities?q=' + query;
        return $.get(ajax_url, function (data) {
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

streetInput.typeahead({
    hint: true,
    highlight: true,
    minLength: 3  //set minimal query length
},
{
  name: 'streets',
  limit: 100,
  source: function (query, p, process) {
        var city = cityInput.val();
        var ajax_url = '/api/streets?city=' + city + '&street_query=' + query;
        return $.get(ajax_url, function (data) {
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
