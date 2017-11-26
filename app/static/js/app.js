
// ###########################################################################
// #  Partial content loading / management                                   #
// ###########################################################################

// When going back in the history, reload the content that was there
window.addEventListener('popstate', function(e) {
    loadContent(e.target.location.pathname);
}, false);

// Capture 'click' for all content links
function captureContentLinks() {
    // Getting the class name 'content-link' is specific to Radio Rhino
    // Could be factorized in the future ;)
    var links = document.getElementsByClassName('content-link');
    var linksLen = links.length;

    function load(e) {
        e.preventDefault();
        loadContent(e.currentTarget.href);
    }

    for (var i = 0; i < linksLen; i++) {
        if (links[i].onclick === null) {
            links[i].onclick = load;
        }
    }
}

function loadContent(target) {
    var req = new XMLHttpRequest();
    req.open('GET', target, true);
    req.setRequestHeader('X-Partial-Content', 'yes');
    req.overrideMimeType('application/json');
    req.onload = function() {
        if (req.status >= 200 && req.status < 400) {
            // Parse the response
            var resp = JSON.parse(req.responseText);

            // Load the content we got, using the function specified by the server
            var f = eval(resp.function);
            var data = resp.content;
            var hist = resp.history;
            f(data);

            // Push this content in the history
            // N.B : in the future, we might want to have a mechanism to do this only
            // for specific contents...
            if (window.location.pathname != target && hist) {
                history.pushState({}, '', target);
            }

            // Recapture content links (some might have been deleted/added)
            captureContentLinks();
        }
    };

    req.onerror = function() {
      // There was a connection error of some sort
    };

    req.send();
}

// ###########################################################################
// #  Partial content management specific to Radio Rhino                     #
// ###########################################################################

function displayMain(data) {
    document.getElementsByTagName('main')[0].innerHTML = data.template;

    var title = document.getElementsByTagName('title')[0];
    var desc = document.getElementsByName('description')[0];

    if (data.hasOwnProperty('title'))
        title.textContent = 'Radio Rhino | ' + data.title;
    else title.textContent = 'Radio Rhino';

    if (data.hasOwnProperty('description'))
        desc.setAttribute('content', data.description);
    else desc.setAttribute('content', "Radio radicale pour personnes sensibles.");
}

function checkLive() {
    loadContent(document.getElementById('live-autocheck').getAttribute('href'));
}

//checkLive();
//var checkLive_ = setInterval(checkLive, 15000);

function updateLive(data) {
    // If live started / is ongoing
    if (data.next_live_in < 0) {
        document.getElementById('live-autocheck').style.display = '';
        document.getElementById('live-play').setAttribute('href', data.stream_url_play);
    }
    // If live is not ongoing
    else {
        document.getElementById('live-autocheck').style.display = 'none';
        document.getElementById('live-play').setAttribute('href', '');
    }
}

// ###########################################################################
// #  Init a few things when loading the document                            #
// ###########################################################################

var player = new Player();

captureContentLinks();
