var player = new Player();

// Event when going back in the history...
window.addEventListener("popstate", function(e) {
  console.log("going back !")
}, false);

// Capture 'click' for all content links
function captureContentLinks()
{
    $('a.contentLink').unbind("click");
    $('a.contentLink').click(function(e)
    {
        e.preventDefault();
        history.pushState({}, '', e.currentTarget.href);
        loadContent(e.currentTarget.href);
    });
}

captureContentLinks();

function displayMain(data)
{
    document.getElementsByTagName("main")[0].innerHTML = data["content"];
}

$.ajaxSetup({
  headers : {
    'X-Rhino-Base-Loaded' : 'yes'
  }
});
function loadContent(target)
{
    $.getJSON(target, function(response_data) {
        var f = eval(response_data[0]);
        var data = response_data[1];
        f(data);
        // Recapture content links (some might have been deleted/added)
        captureContentLinks();
    });
};


