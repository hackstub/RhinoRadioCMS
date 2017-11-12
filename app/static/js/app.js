var player = new Player();

// Event when going back in the history...
window.addEventListener("popstate", function(e) {
    loadContent(e.target.location.pathname);
}, false);

// Capture 'click' for all content links
function captureContentLinks() {
    var links = document.getElementsByClassName("contentLink");
    var linksLen = links.length;

    function pushAndLoad(e) {
        e.preventDefault();
        var href = e.currentTarget.href;
        history.pushState({}, '', href);
        loadContent(href);
    }

    for (var i = 0; i < linksLen; i++) {
        if (links[i].onclick === null) {
            links[i].onclick = pushAndLoad;
        }
    }
}

captureContentLinks();

function displayMain(data) {
    document.getElementsByTagName("main")[0].innerHTML = data["content"];
}

function loadContent(target) {
    getJSON(target, function(response_data) {
        var f = eval(response_data[0]);
        var data = response_data[1];
        f(data);
        // Recapture content links (some might have been deleted/added)
        captureContentLinks();
    });
};

function getJSON(target, callback) {
    var req = new XMLHttpRequest();
    req.open('GET', target, true);
    req.setRequestHeader('X-Rhino-Base-Loaded', 'yes');
    req.overrideMimeType("application/json");
    req.onload = function() {
        if (req.status >= 200 && req.status < 400) {
            callback(JSON.parse(req.responseText));
        }
    };

    req.onerror = function() {
      // There was a connection error of some sort
    };

    req.send();
}
