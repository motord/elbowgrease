/**
 * Created by peter on 9/15/16.
 */

// ==UserScript==
// @name                Axel Episodes
// @namespace	        http://v.numag.net/grease/
// @description	        grab all episodes for axel download
// @include		http://hyper.numag.net/*/
// @include		http://amsterdam.hikerlink.org/youtube/*/
// ==/UserScript==
(function () {
    function $x() {
        var x='';
        var node=document;
        var type=0;
        var fix=true;
        var i=0;
        var cur;

        function toArray(xp) {
            var final=[], next;
            while (next=xp.iterateNext()) {
                final.push(next);
            }
            return final;
        }

        while (cur=arguments[i++]) {
            switch (typeof cur) {
                case "string": x+=(x=='') ? cur : " | " + cur; continue;
                case "number": type=cur; continue;
                case "object": node=cur; continue;
                case "boolean": fix=cur; continue;
            }
        }

        if (fix) {
            if (type==6) type=4;
            if (type==7) type=5;
        }

        // selection mistake helper
        if (!/^\//.test(x)) x="//"+x;

        // context mistake helper
        if (node!=document && !/^\./.test(x)) x="."+x;

        var result=document.evaluate(x, node, null, type, null);
        if (fix) {
            // automatically return special type
            switch (type) {
                case 1: return result.numberValue;
                case 2: return result.stringValue;
                case 3: return result.booleanValue;
                case 8:
                case 9: return result.singleNodeValue;
            }
        }

        return fix ? toArray(result) : result;
    };

    var elmNewContent = document.createElement('div');

    elmNewContent.textContent = $x("/html/body/pre/a/@href").slice(1).map(function (element) {
        return 'x256 ' + window.location.href + element.value;
    }).join([separator = '; ']);
    elmNewContent.setAttribute("style", "color: #5fba7d; font-family: 'Raleway',sans-serif; font-size: 12px; font-weight: 500; line-height: 16px; margin: 0 0 24px; ");
    document.body.appendChild(elmNewContent);
})();
