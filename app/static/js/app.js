var player = new Player();

// Event when going back in the history...
window.addEventListener("popstate", function(e) {
  console.log("going back !")
}, false);

// Capture 'click' for all content links
$('a.contentLink').click(function(e)
{
    e.preventDefault();
    history.pushState({}, '', e.currentTarget.href);
    loadContent(e.currentTarget.href);
});

function displayMain(data)
{
    document.getElementsByTagName("main")[0].innerHTML = data["content"];
}

function loadContent(target)
{
    $.getJSON(target, function(response_data) {
        var f = eval(response_data[0]);
        var data = response_data[1];
        f(data);
    });
};


