var player = new Player();

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

// Capture all internal links
$('a.intern').click(function(e)
{
    e.preventDefault();
    console.log(e.currentTarget.href);
    history.pushState({}, '', e.currentTarget.href);
    $('#main').load(e.currentTarget.href + " #mainframe" );
});

function fetchAndPlayPodcast(target)
{
    $.getJSON(target, function(data) {
    player.load(data);
    // // Get relevant items
    // var playerSrc = $('audio source.mp3_src');
    // var playerTitle = $('#play-infos h3');
    //
    // // Update their data
    // playerSrc.attr("src", data.src);
    // playerTitle.html(data.title);
    //
    // // Reload player with the newly fetched podcast
    // player.pause();
    // player.load();
    // player.oncanplaythrough = player.play();
    // playBtn.attributes.display.value = "none";
    // pauseBtn.attributes.display.value = "";
    });
};
