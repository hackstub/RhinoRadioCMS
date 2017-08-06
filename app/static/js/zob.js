
// For all links, have a custom click handler....
//$('a').click(function(e)
//{
//    e.preventDefault();
//    loadStuff(e.target.href);
//    history.pushState({}, '', e.target.href);
//});

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

//
//
// For all podcasts
//
//
$('a.podcast').click(function(e)
{
    console.log(e);
    console.log(e.target.href);
    e.preventDefault();
    playPodcast(e.target.href);
    history.pushState({}, '', e.target.href);
});

function playPodcast(target)
{
    $.getJSON(target, playPodcast_ );
}

function playPodcast_(data)
{
    console.log(data.src);
    console.log(data.title);
    var playerOggSrc = $('#bottomPlayer audio.audio-player source.ogg_src');
    var playerTitle = $('#bottomPlayer h3.currentTrackTitle');
    console.log(playerOggSrc);
    console.log(playerTitle);
    playerOggSrc.attr("src", data.src)
    playerTitle.html(data.title);
}

$(function(){
  console.log("Init");
});

