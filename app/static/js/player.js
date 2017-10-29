function Player() {
    this.audio         = document.getElementById("audio");

    this.playBtn       = document.getElementById("playBtn");
    this.pauseBtn      = document.getElementById("pauseBtn");
    var playpauseBtn   = document.getElementById("play");



    var trackProgress  = document.getElementById("track-progress");
    var currentTime    = document.getElementById("current-time");
    var totalTime      = document.getElementById("total-time");


    this.initListeners();

}
Player.prototype.initListeners = function() {
    var _this = this;

    function sliderListerner(e, action) {
        // generic sliders mouse event listener
        e.preventDefault();
        action(e);
        function removeListeners(e) {
            action(e);
            window.removeEventListener("mousemove", action);
            window.removeEventListener("mouseup", removeListeners);
        }
        window.addEventListener("mousemove", action);
        window.addEventListener("mouseup", removeListeners);
    }

    // init track slider listener
    var track = document.getElementById("track");
    track.onmousedown = function(e) {
        sliderListerner(e, _this.updateTrack);
    }

    // init volume slider listener
    var volume = document.getElementById("volume");
    volume.onmousedown = function(e) {
        sliderListerner(e, _this.updateVolume);
    }

    // init mute button listener
    var mute = document.getElementById("mute");
    mute.onclick = function() {
        _this.mute();
    }

};
Player.prototype.load = function(data) {
    var source = this.audio.children[0];
    var title = document.getElementById("track-title");

    // Update their data
    source.setAttribute("src", data.src);
    title.innerHtml = data.title;

    // Reload player with the newly fetched podcast
    this.audio.pause();
    this.audio.load();
    this.audio.oncanplaythrough = this.audio.play();

    this.playBtn.attributes.display.value = "none";
    this.pauseBtn.attributes.display.value = "";
};
Player.prototype.play = function() {
};
Player.prototype.pause = function() {
};
Player.prototype.togglePlayPause = function() {
};
Player.prototype.mute = function() {
    var actualVolume = this.audio.volume;
    var newVolume;

    if (actualVolume != 0) {
        this.previousVolume = actualVolume;
        newVolume = 0;
    } else {
        newVolume = this.previousVolume;
    }

    this.updateVolume(newVolume);

};
Player.prototype.updateVolume = function(value) {
    /* Update the volume and the graphic slider width. The parameter can be an
    integrer or an event */

    var volumeProgress = document.getElementById("volume-active");

    if (value.target !== undefined) {
        // if the parameter is an event, calculate the value depending on
        // the mouse position
        // FIXME clientX stuff not the best solution
        var w = window.innerWidth;
        var x = w - value.clientX;
        var volumeWidth = volumeBar.getBoundingClientRect().width;

        if (x <= 0) value = 1;
        else if (x >= volumeWidth) value = 0;
        else value = 1 - (x / volumeWidth);
    }

    this.audio.volume = value;
    volumeProgress.style.width = value * 100 + "%";
};
