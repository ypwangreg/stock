document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.ctrlKey ) {
        if ( evt.keyCode == 90 ) {
            //alert("Ctrl-Z");
            sendwq('keycut', 'Ctrl-Z');
        }
    } else {
        if (evt.which >= 48 && evt.which <= 90) {
            // number and Cap Letter.
            sendwq('keycut', String.fromCharCode(evt.which));
        } else {
            // other key, like alt(18), shift,(16) Cap(20)..
            sendwq('keycut', evt.which);
        }
    }
};
