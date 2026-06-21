// Current queue version for detect modification
var control_queue_version = 0;

var control_volume_slider_using = false;

/************************************
 * 
 *  Event manager at page loading.
 * 
 ************************************/
function controlOnLoad() {
    controlManageStatus();
    window.setInterval(controlManageStatus, 3000);
}

function controlBtnPreviousOnClick() {
    const params = new URLSearchParams();

    params.append("action", "previous");
    fetch(utilsApiRoot() + `/player?${params}`, {method: 'POST', headers: { 'Accept': 'application/json' }})
        .then(response => {
            if (!response.ok) {
                throw new Error('When going to previous item : Network response was not ok ' + response.statusText);
            }
            return response.json()
        })
        .then(data => {
            if (data.success) {
                controlManageStatus();
            }
        });
}

function controlBtnPlayPauseOnClick() {
    const params = new URLSearchParams();

    params.append("action", "toggle-play-pause");
    fetch(utilsApiRoot() + `/player?${params}`, {method: 'POST', headers: { 'Accept': 'application/json' }})
        .then(response => {
            if (!response.ok) {
                throw new Error('When toggling play/pause : Network response was not ok ' + response.statusText);
            }
            return response.json()
        })
        .then(data => {
            if (data.success) {
                controlManageStatus();
            }
        })
}

function controlBtnNextOnClick() {
    const params = new URLSearchParams();

    params.append("action", "next");
    fetch(utilsApiRoot() + `/player?${params}`, {method: 'POST', headers: { 'Accept': 'application/json' }})
        .then(response => {
            if (!response.ok) {
                throw new Error('When going to next item : Network response was not ok ' + response.statusText);
            }
            return response.json()
        })
        .then(data => {
            if (data.success) {
                controlManageStatus();
            }
        });
}

function controlBtnSettingsOnClick() {
    settingsActivateDropDown();
}

function controlManageStatus() {
    fetch(utilsApiRoot() + "/player/status", {
        method: 'GET', headers: { 'Accept': 'application/json' }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('When getting player status : Network response was not ok ' + response.statusText);
            }

            return response.json()
        })
        .then(data => {
            if (data.success) {
                if (data.success == "OK" && data.payload) {
                    if (data.payload) {
                        settingsTestRefreshDb(data.payload);
                        controlShowStatus(data.payload);
                    }
                    else {
                        throw new Error('Status not in returned payload.');
                    };
                };
            };
        });
}

function controlShowStatus(parStatusJson) {

    // Update play/pause icon
    if (parStatusJson.state) {
        varBtnPlayPauseSong = document.querySelector("#control-play-pause > button");
        if (parStatusJson.state == "play") {
            varBtnPlayPauseSong.setAttribute("class", "control-pause-btn");
        }
        else {
            varBtnPlayPauseSong.setAttribute("class", "control-play-btn");
        }
    }

    // If queue has changed, refresh his display.
    if (control_queue_version != parStatusJson.queue_version) {
        control_queue_version = parStatusJson.queue_version;
        queueRefresh();
    }

    // Show current item
    var_current_item_id = parStatusJson.current_song_id;
    var_display_title = "";
    var_display_complement = "";
    if ("current_song_item" in parStatusJson) {
        var_mr_stream_name = "";
        var_title = "";
        var_artist = "";

        // Get current item attributes
        if("mr_stream_name" in parStatusJson.current_song_item)
            var_mr_stream_name = parStatusJson.current_song_item.mr_stream_name;
        if("title" in parStatusJson.current_song_item)
            var_title = parStatusJson.current_song_item.title;
        if("artist" in parStatusJson.current_song_item)
            var_artist = parStatusJson.current_song_item.artist;

        // Calculate display title and display complement
        if (var_mr_stream_name.length > 0) {
            var_display_title = var_mr_stream_name;
            var_display_complement = var_title;
        }
        else {
            var_display_title = var_title;
            var_display_complement = var_artist;
        }
    }

    // Show display title and display complement
    document.getElementById("current-item-title").innerText = var_display_title;
    document.getElementById("current-item-complement").innerText = var_display_complement;
    document.getElementById("current-item-id").value = var_current_item_id

    // Set control volume position
    if(("volume" in parStatusJson)&&(!control_volume_slider_using)) {
        varIntVolume = Number(parStatusJson.volume);
        if(!isNaN(varIntVolume))
            controlVolumeSetPosition(varIntVolume);
    }
    controlVolumeAdjustTrack();


    // Check the current item in queue
    queueCheckCurrentItem();
}

/************************************
 * 
 *  Volume management
 * 
 ************************************/
function controlVolumeSliderOnMouseDown() {
    control_volume_slider_using = true;
}

function controlVolumeSliderOnMouseUp() {
    control_volume_slider_using = false;
}


function controlVolumeSliderOnChange(parValue) {
    console.log("controlVolumeSliderOnChange");
    controlSetPlayerVolume(parValue);
}

function controlVolumeSliderOnInput(parValue) {
    controlVolumeAdjustTrack();
}

/**
 * Sets the slider value with the percentage provided as a parameter. 
 * @param {Int} parIntVolumePerCent 
 */
function controlVolumeSetPosition(parIntVolumePerCent) {
    if (document.getElementById("volume-slider").value!=parIntVolumePerCent) {
        console.log("controlVolumeSetPosition : parIntVolumePerCent=" + parIntVolumePerCent + "    document.getElementById(\"volume-slider\").value=" + document.getElementById("volume-slider").value);
        document.getElementById("volume-slider").value = parIntVolumePerCent;
        controlVolumeAdjustTrack();
    }
}

/**
 * Synchronize colored track height of the slider with de position of the slider.
 */
function controlVolumeAdjustTrack() {
    document.getElementById("volume-height").style.height = Math.round(((document.getElementById("volume-slider").offsetHeight - 2) * document.getElementById("volume-slider").value) / 100).toString() + "px";
}

/**
 * Change player volume on server.
 * @param {Int} parIntVolumePercent Volume between 0 and 100.
 */
function controlSetPlayerVolume(parIntVolumePercent) {
    const params = new URLSearchParams();

    if(parIntVolumePercent<0 || parIntVolumePercent>100) {
        throw new RangeError("In controlSetPlayerVolume, parmameter must be an integer between 0 and 100.");
    }

    params.append("action", "set-range");
    params.append("range", Math.round(parIntVolumePercent).toString());
    fetch(utilsApiRoot() + `/player/volume?${params}`, {method: 'POST', headers: { 'Accept': 'application/json' }})
        .then(response => {
            if (!response.ok) {
                throw new Error('Error when setting volume to this value : ' + parIntVolumePercent);
            }
            return response.json()
        })
        .then(data => {
            if (!data.success) {
                throw new Error('Error when setting volume to this value : ' + parIntVolumePercent + '. Error is returned by server.');
            }
        });
}