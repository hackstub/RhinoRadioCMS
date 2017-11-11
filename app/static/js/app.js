var player = new Player();

// Event when going back in the history...
window.addEventListener("popstate", function(e) {
  console.log("going back !")
}, false);

// Capture 'click' for all content links
$('a.contentLink').click(function(e)
{
    e.preventDefault();
    history.pushState({}, '', e.target.href);
    loadContent(e.target.href);
});

/*
// Capture all internal links
$('a.intern').click(function(e)
{
    e.preventDefault();
    console.log(e.currentTarget.href);
    history.pushState({}, '', e.currentTarget.href);
    $('#main').load(e.currentTarget.href + " #mainframe" );
});
*/

function loadContent(target)
{
    $.getJSON(target, function(response_data) {
        var f = eval(response_data[0]);
        var data = response_data[1];
        f(data);
    });
};


