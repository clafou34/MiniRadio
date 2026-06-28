var volume_slider_using = false;

// Settings global composant
const control_volume_drop_down = document.getElementById('volume-drop-down');
const control_volume_button = document.getElementById('control-volume-btn');

function volumeOnLoad() {
    document.addEventListener('click', volumeClickOutsideMenu);
}

function volumeClickOutsideMenu(ev) {
    if (!control_volume_drop_down.contains(ev.target)) {
        if (ev.target == control_volume_button) {
            volumeActivateDropDown();
        }
        else {
            volumeHideDropDown();
        }
    }
}

function volumeActivateDropDown() {
    if (control_volume_drop_down.style.display == "block")
        control_volume_drop_down.style.display = "none";
    else {
        control_volume_drop_down.style.display = "block";
        volumeAdjustTrack();
    }
}

function volumeHideDropDown() {
    if (control_volume_drop_down.style.display === "block")
        control_volume_drop_down.style.display = "none";
}

function volumeSliderOnMouseDown() {
    volume_slider_using = true;
}

function volumeSliderOnMouseUp() {
    volume_slider_using = false;
}


function volumeSliderOnChange(parValue) {
    volumeSetPlayerVolume(parValue);
}

function volumeSliderOnInput(parValue) {
    volumeAdjustTrack();
}

/**
 * Sets the slider value with the percentage provided as a parameter. 
 * @param {Int} parIntVolumePerCent 
 */
function volumeSetPosition(parIntVolumePerCent) {
    if (!volume_slider_using) {
        if (document.getElementById("volume-slider").value != parIntVolumePerCent) {
            document.getElementById("volume-slider").value = parIntVolumePerCent;
            volumeAdjustTrack();
        }
    }
}

/**
 * Synchronize colored track height of the slider with de position of the slider.
 */
function volumeAdjustTrack() {
    document.getElementById("volume-height").style.height = Math.round(((document.getElementById("volume-slider").offsetHeight - 2) * document.getElementById("volume-slider").value) / 100).toString() + "px";
    document.getElementById("volume-percentage").innerText = document.getElementById("volume-slider").value + " %";
}

/**
 * Change player volume on server.
 * @param {Int} parIntVolumePercent Volume between 0 and 100.
 */
function volumeSetPlayerVolume(parIntVolumePercent) {
    const params = new URLSearchParams();

    if (parIntVolumePercent < 0 || parIntVolumePercent > 100) {
        throw new RangeError("In controlSetPlayerVolume, parmameter must be an integer between 0 and 100.");
    }

    params.append("action", "set-range");
    params.append("range", Math.round(parIntVolumePercent).toString());
    fetch(utilsApiRoot() + `/player/volume?${params}`, { method: 'POST', headers: { 'Accept': 'application/json' } })
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

