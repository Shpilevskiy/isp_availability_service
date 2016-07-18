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
