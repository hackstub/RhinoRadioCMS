// ╭───────────────────────────────────────────────────╮
// │     ╷╭─╴   ╭─┐╷ ╷┌─╮╶┬╴╭─╮   ┌─╮╷  ╭─┐╷ ╷┌─╴┌─╮   │
// │     │╰─╮   ├─┤│ ││ │ │ │ │   ├─╯│  ├─┤╰─┤├─╴├┬╯   │
// │   ╰─╯╶─╯   ╵ ╵╰─╯└─╯╶┴╴╰─╯   ╵  ╰─╴╵ ╵╶─╯╰─╴╵ ╰   │
// ╰───────────────────────────────────────────────────╯

function Player() {
    this.audio = document.getElementById("audio");

    this.playBtn = document.getElementById("playBtn");
    this.pauseBtn = document.getElementById("pauseBtn");

    this.currentTime = document.getElementById("current-time");
    this.totalTime = document.getElementById("total-time");

    this.trackBar = document.getElementById("track");
    this.trackSlider  = document.getElementById("track-progress");
    this.buffered = 0;
    this.mouseMove = false;

    this.volumeBar = document.getElementById("volume");
    this.volumeSlider = document.getElementById("volume-active");
    this.previousVolume = 1;

    this.initListeners();
}
Player.prototype.initListeners = function() {
    var _this = this;

    // init play button listener
    function togglePlayPause() {
        if (_this.audio.paused) _this.play();
        else _this.pause();
    }

    var playButton = document.getElementById("play");
    playButton.onclick = togglePlayPause;

    // init space bar listener (FIXME merge with upper function)
    window.onkeypress = function(e) {
        if (e.keyCode === 32 || e.key === " ") {
            e.preventDefault();
            togglePlayPause();
        }
    }

    // generic sliders mouse event listener
    function sliderListerner(e, action, graphicUpdate) {
        function removeListeners(e) {
            action(e, true);
            window.removeEventListener("mousemove", action);
            window.removeEventListener("mouseup", removeListeners);
        }
        e.preventDefault();
        action(e);

        window.addEventListener("mousemove", action);
        window.addEventListener("mouseup", removeListeners);
    }

    function getTrackValue(e, update) {
        // FIXME clientX stuff not the best solution
        var value;
        var x = e.clientX;
        var trackWidth = this.trackBar.getBoundingClientRect().width;

        var currentTime;
        if (x >= trackWidth) currentTime = this.audio.duration;
        else if (x <= 0) currentTime = 0;
        else currentTime = (x / trackWidth) * this.audio.duration;

        if (update === true) {
            this.mouseMove = false;
            this.audio.currentTime = currentTime;
            _this.updateLoading();
        }
        this.updateTrackGraphic(currentTime);
    }

    // init track slider listener
    this.trackBar.onmousedown = function(e) {
        _this.mouseMove = true;
        sliderListerner(e, getTrackValue.bind(_this));
    }

    function getVolumeValue(e) {
        // FIXME clientX stuff not the best solution
        var value;
        var w = window.innerWidth;
        var x = w - e.clientX;
        var volumeWidth = this.volumeBar.getBoundingClientRect().width;

        if (x <= 0) value = 1;
        else if (x >= volumeWidth) value = 0;
        else value = 1 - (x / volumeWidth);

        this.updateVolume(value);
    }
    // init volume slider listener
    this.volumeBar.onmousedown = function(e) {
        sliderListerner(e, getVolumeValue.bind(_this));
    }

    // init mute button listener
    var mute = document.getElementById("mute");
    mute.onclick = _this.mute.bind(_this);

    this.audio.addEventListener('progress', _this.updateLoading.bind(_this));
    this.audio.addEventListener('timeupdate', function() {
        if (!_this.mouseMove) {
            _this.updateTrackGraphic(_this.audio.currentTime);
            _this.updateLoading();
        }
    });
    this.audio.addEventListener('ended', _this.pause.bind(_this));

};
Player.prototype.load = function(data) {
    var _this = this;
    var source = this.audio.children[0];
    var title = document.getElementById("track-title");

    // Update their data
    source.setAttribute("src", data.link);
    title.textContent = data.title;

    // Reload player with the newly fetched podcast
    this.audio.pause();
    this.audio.load();
    this.buffered = 0;
    this.audio.onloadedmetadata = function () {
        _this.totalTime.textContent = _this.formatTime(_this.audio.duration);
    };
    this.audio.oncanplaythrough = this.play();

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
Player.prototype.updateLoading = function() {
    var length = this.audio.buffered.length;
    if (length > 0) {
        var buffered = this.audio.buffered.end(length-1);
        if (buffered > this.buffered) {
            this.buffered = buffered;
            var loading = document.getElementById("track-loading");
            var percent = (buffered / this.audio.duration) * 100;
            loading.style.width = percent + '%';
        }
    }
};
Player.prototype.updateTrackGraphic = function(value) {
    var percent = (value / this.audio.duration) * 100;
    this.trackSlider.style.width = percent + '%';

    this.currentTime.textContent = this.formatTime(value);
};
Player.prototype.updateVolume = function(value) {
    /* Update the volume and the graphic slider width. The parameter can be an
    integrer or an event */

    this.audio.volume = value;
    this.volumeSlider.style.width = value * 100 + "%";
};
Player.prototype.formatTime = function(time) {
    var min = Math.floor(time / 60);
    var sec = Math.floor(time % 60);

    return min + ':' + ((sec<10) ? ('0' + sec) : sec);
};
