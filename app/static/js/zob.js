
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

//
//
// For all podcasts
//
//
$('a podcast').click(function(e)
{
    e.preventDefault();
    loadStuff(e.target.href);
    history.pushState({}, '', e.target.href);
});

function playPodcast(target)
{
    $.getJSON(target, function( data ) {
        console.log(data.podcastUrl)
        console.log(data.title)
        console.log(data.author)
        console.log(data.numberOfFlorps)
        console.log(data.description)
    });
}


$(function(){
  $('#bottomPlayer').mediaelementplayer({
    alwaysShowControls: true,
    features: ['playpause','progress','volume'],
    audioVolume: 'horizontal',
    enableKeyboard: true,
    pauseOtherPlayers: true,
    iPadUseNativeControls: false,
    iPhoneUseNativeControls: false,
    AndroidUseNativeControls: false
  });
});

