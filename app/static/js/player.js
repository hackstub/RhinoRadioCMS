var audioPlayer = document.querySelector('#bottomPlayer');
var playBtn = audioPlayer.querySelector('#playbtn');
var pauseBtn = audioPlayer.querySelector('#pausebtn');
var playpauseBtn = audioPlayer.querySelector("#play");
var progress = audioPlayer.querySelector("#track-progress");
var track = audioPlayer.querySelector("#track");
var player = audioPlayer.querySelector('audio');
var currentTime = audioPlayer.querySelector('#current-time');
var totalTime = audioPlayer.querySelector('#total-time');
var volume = document.getElementById("volume");
var volumeProgress = document.getElementById("volume-active");

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

volume.addEventListener("mousedown", function(event) {
    // FIXME same stuff, combo it !
    function mouseUp(e) {
        changeVolume(e);
        window.removeEventListener("mousemove", changeVolume);
        window.removeEventListener("mouseup", mouseUp);
    }

    event.preventDefault();
    window.addEventListener("mousemove", changeVolume);

    window.addEventListener("mouseup", mouseUp);
});
document.getElementById("mute").addEventListener("click", function() {
    player.volume = 0;
    volumeProgress.style.width = "0%";
});

var trackWidth = track.getBoundingClientRect().width;
var volumeWidth = volume.getBoundingClientRect().width;

function rewind(e) {
    //FIXME clientX not the best idea
    e.preventDefault();
    var x = e.clientX;

    if (x >= trackWidth) {
        player.currentTime = player.duration;
    }
    else if (x <= 0) {
        player.currentTime = 0;
    }
    else {
        player.currentTime = (x / trackWidth) * player.duration;
    }
    updateProgress();
}

function changeVolume(e) {
    //FIXME clientX not the best idea
    e.preventDefault();
    var w = window.innerWidth;
    var x = w - e.clientX;

    if (x <= 0) {
        player.volume = 1;
    }
    else if (x >= volumeWidth) {
        player.volume = 0;
    }
    else {
        player.volume = 1 - (x / volumeWidth);
    }
    volumeProgress.style.width = player.volume * 100 + "%";
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
