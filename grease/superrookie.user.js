/**
 * Created by peter on 9/19/16.
 */

// ==UserScript==
// @name                Super Rookie
// @namespace	        http://v.numag.net/grease/
// @description	        locate new posts on piratebay
// @include		https://thepiratebay.org/top/*
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

    $x("/html/body/div[@id='main-content']/table[@id='searchResult']/tbody/tr/td[2]/a").map(function (element) {
        if (localStorage.getItem(element.href) == undefined){
            localStorage.setItem(element.href,1);
            element.style= 'background: hotpink;';
        }
        else {
            localStorage.setItem(element.href,localStorage.getItem(element.href)+1);;
        };
    });
})();
