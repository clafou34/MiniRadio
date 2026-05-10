// Current queue version for detect modification
var control_queue_version = 0;

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

    // Check the current item in queue
    queueCheckCurrentItem();
}