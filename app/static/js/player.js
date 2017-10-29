function Player() {
    this.audio = document.getElementById("audio");

    this.playBtn = document.getElementById("playBtn");
    this.pauseBtn = document.getElementById("pauseBtn");

    this.currentTime = document.getElementById("current-time");
    this.totalTime = document.getElementById("total-time");

    this.trackBar = document.getElementById("track");
    this.trackSlider  = document.getElementById("track-progress");

    this.volumeBar = document.getElementById("volume");
    this.volumeSlider = document.getElementById("volume-active");
    this.previousVolume = 1;

    this.initListeners();

}
Player.prototype.initListeners = function() {
    var _this = this;

    // init play button listener
    var playButton = document.getElementById("play");
    playButton.onclick = function() {
        if (_this.audio.paused) _this.play();
        else _this.pause();
    }

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
    this.trackBar.onmousedown = function(e) {
        sliderListerner(e, _this.updateTrack.bind(_this));
    }

    // init volume slider listener
    this.volumeBar.onmousedown = function(e) {
        sliderListerner(e, _this.updateVolume.bind(_this));
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
    this.playBtn.attributes.display.value = "none";
    this.pauseBtn.attributes.display.value = "";
    this.audio.play();
};
Player.prototype.pause = function() {
    this.playBtn.attributes.display.value = "";
    this.pauseBtn.attributes.display.value = "none";
    this.audio.pause();
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

    if (value.target !== undefined) {
        // if the parameter is an event, calculate the value depending on
        // the mouse position
        // FIXME clientX stuff not the best solution
        var w = window.innerWidth;
        var x = w - value.clientX;
        var volumeWidth = this.volumeBar.getBoundingClientRect().width;

        if (x <= 0) value = 1;
        else if (x >= volumeWidth) value = 0;
        else value = 1 - (x / volumeWidth);
    }

    this.audio.volume = value;
    this.volumeSlider.style.width = value * 100 + "%";
};
