
// For all links, have a custom click handler....
$('a').click(function(e)
{
    e.preventDefault();
    loadStuff(e.target.href);
    history.pushState({}, '', e.target.href);
});

window.addEventListener("popstate", function(e) {
  console.log("going back !")
}, false);

function loadStuff(target)
{
    $.getJSON( "example.json", function( data ) {
        console.log(data.title)
        console.log(data.author)
        console.log(data.numberOfFlorps)
        console.log(data.description)
    });

    $( "#main" ).load( target );
}

