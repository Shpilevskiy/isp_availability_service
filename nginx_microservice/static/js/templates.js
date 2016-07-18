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