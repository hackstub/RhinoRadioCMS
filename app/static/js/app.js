
// Even when going back in the history...
window.addEventListener("popstate", function(e) {
  console.log("going back !")
}, false);

// Capture 'clock' for all podcast
$('a.podcast').click(function(e)
{
    e.preventDefault();
    fetchAndPlayPodcast(e.target.href);
    history.pushState({}, '', e.target.href);
});

function fetchAndPlayPodcast(target)
{
    $.getJSON(target, function(data) {

    // Get relevant items
    var player = $('#bottomPlayer audio.audio-player')[0];
    var playerSrc = $('#bottomPlayer audio.audio-player source.mp3_src');
    var playerTitle = $('#bottomPlayer h3.currentTrackTitle');
    
    // Update their data
    playerSrc.attr("src", data.src);
    playerTitle.html(data.title);

    // Reload player with the newly fetched podcast
    player.pause();
    player.load();
    player.oncanplaythrough = player.play();

    });
}

