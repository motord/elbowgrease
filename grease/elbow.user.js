/**
 * Created by peter on 9/9/16.
 */
var myRequest = new Request('http://v.numag.net/grease', {method: 'POST', body: '{"url":"http://www.jandown.com/link.php?ref=QU8lml7MET"}'});
var myHeaders = new Headers();
myHeaders.append('Content-Type', 'application/json');
var myInit = { method: 'POST',
    headers: myHeaders,
    mode: 'cors',
    cache: 'default' };
fetch(myRequest,myInit).then(function(response) {
    console.info(response);
})