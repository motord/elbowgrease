/**
 * Created by peter on 9/15/16.
 */

// ==UserScript==
// @name                Axel Episodes
// @namespace	        http://v.numag.net/grease/
// @description	        grab all episodes for axel download
// @include		http://hyper.numag.net/
// @include		http://amsterdam.hikerlink.org/youtube/*/
// ==/UserScript==
(function () {
    var elmNewContent = document.createElement('div');

    elmNewContent.textContent = $x("/html/body/pre/a/@href").slice(1).map(function (element) {
        return 'x256 ' + window.location.href + element.value;
    }).join([separator = '; ']);
    elmNewContent.setAttribute("style", "color: #5fba7d; font-family: 'Raleway',sans-serif; font-size: 12px; font-weight: 500; line-height: 16px; margin: 0 0 24px; ");
    document.body.appendChild(elmNewContent);
    console.log('bingo')
})();
