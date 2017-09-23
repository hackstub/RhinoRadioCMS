var audioPlayer = document.querySelector('#bottomPlayer');
var playBtn = audioPlayer.querySelector('#playbtn');
var pauseBtn = audioPlayer.querySelector('#pausebtn');
var playpauseBtn = audioPlayer.querySelector("#play");
var progress = audioPlayer.querySelector("#track-progress");
var track = audioPlayer.querySelector("#track");
var player = audioPlayer.querySelector('audio');
var currentTime = audioPlayer.querySelector('#current-time');
var totalTime = audioPlayer.querySelector('#total-time');

track.addEventListener("mousedown", function(event) {
    function mouseUp(e) {
        rewind(e);
        window.removeEventListener("mousemove", rewind);
        window.removeEventListener("mouseup", mouseUp);
    }

    event.preventDefault();
    window.addEventListener("mousemove", rewind);

    window.addEventListener("mouseup", mouseUp);
});

var trackWidth = track.getBoundingClientRect().width;

function rewind(e) {
    e.preventDefault();
    var x = e.clientX;
    if (x >= trackWidth) {
        player.currentTime = player.duration;
    }
    else if (x <= 0) {
        player.currentTime = 0;
    }
    else {
        player.currentTime = (x/trackWidth)*player.duration;
    }
    updateProgress();
}

playpauseBtn.addEventListener('click', togglePlay);
player.addEventListener('timeupdate', updateProgress);
player.addEventListener('loadedmetadata', () => {
    totalTime.textContent = formatTime(player.duration);
});
// player.addEventListener('canplay', makePlay);
player.addEventListener('ended', function(){
    playBtn.attributes.display.value = "";
    pauseBtn.attributes.display.value = "none";
    //player.currentTime = 0;
});

function updateProgress() {
    var current = player.currentTime;
    var percent = (current / player.duration) * 100;
    progress.style.width = percent + '%';

    currentTime.textContent = formatTime(current);
}

function formatTime(time) {
    var min = Math.floor(time / 60);
    var sec = Math.floor(time % 60);
    return min + ':' + ((sec<10) ? ('0' + sec) : sec);
}

function togglePlay() {
    if(player.paused) {
        playBtn.attributes.display.value = "none";
        pauseBtn.attributes.display.value = "";
        player.play();
    } else {
        playBtn.attributes.display.value = "";
        pauseBtn.attributes.display.value = "none";
        player.pause();
    }
}
