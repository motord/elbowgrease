/**
 * Created by peter on 9/9/16.
 */

// ==UserScript==
// @name                Elbow Grease
// @namespace	        http://v.numag.net/grease/
// @description	        grab torrents for direct download
// @include		http://bt.aisex.com/bt/html_data/*
// ==/UserScript==

var elmTopic = document.getElementById('read_tpc');
var links=document.evaluate('a',elmTopic, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
for (var i = links.snapshotLength - 1; i >= 0; i--) {
    var link = links.snapshotItem(i);
    if (link.host && link.host == 'www.jandown.com') {
        var elmTorrent=link;
    }
}
var myRequest = new Request('http://v.numag.net/grease', {method: 'POST', body: '{"url":"'+elmTorrent.href+'"}'});
var myHeaders = new Headers();
myHeaders.append('Content-Type', 'application/json');
var myInit = { method: 'POST',
    headers: myHeaders,
    mode: 'cors',
    cache: 'default' };
fetch(myRequest,myInit).then(function(response) {
    return response.json().then(function(json) {
        elmTorrent.href = json.torrent;
        elmTorrent.textContent = json.torrent;
    });
})