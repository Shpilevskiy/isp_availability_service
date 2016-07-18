var buildCitySearchURL = function(city){
    return '/api/cities?q=' + city;
};

var buildStreetSearchURL = function(city, street){
    return '/api/streets?city=' + city + '&street=' + street;
};

var buildSearchURL = function(city, street){
    return '/api/search?city=' + city + '&street=' + street;
};


/** This function analyses whether the valid key
 *  (alpha numerical characters, backspace, delete keys)
 *  has been pressed . */
var isValidInputKey = function (char_code) {
    if ( !(char_code >= C_FULL_STOP  && char_code <= C_LATIN_CAPITAL_LETTER_Z) && char_code != C_DELETE_KEY && char_code != C_BACKSPACE_KEY)  {
         return false;
    }
    return true;
};
