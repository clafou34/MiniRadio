// Settings global variable
var control_settings_refreshing_db = false;

// Settings global composant
const control_settings_drop_down = document.getElementById('settings-drop-down');
const control_settings_button = document.getElementById('control-settings-btn');

function settingsOnLoad() {
    document.addEventListener('click', settingsClickOutsideMenu);
}

function settingsClickOutsideMenu(ev) {
    if(ev.target==control_settings_button) {
        settingsActivateDropDown();
    }
    else {
        settingsHideDropDown();
    }
}

function settingsActivateDropDown() {
    if(control_settings_drop_down.style.display=="block")
        control_settings_drop_down.style.display = "none";
    else
        control_settings_drop_down.style.display = "block"; 
}

function settingsHideDropDown() {
    if(control_settings_drop_down.style.display==="block")
        control_settings_drop_down.style.display = "none"; 
}

function settingsRefreshDbOnClick() {
    const params = new URLSearchParams();

    params.append("action", "refresh-db");
    fetch(utilsApiRoot() + `/settings?${params}`, {method: 'POST', headers: { 'Accept': 'application/json' }})
        .then(response => {
            if (!response.ok) {
                throw new Error('When launching database refresh : Network response was not ok ' + response.statusText);
            }
            return response.json()
        })
        .then(data => {
            if (data.success) {
                control_settings_refreshing_db = true;
                showSnackbar("Database is being refreshed.");
            }
        });
}

/**
 * Check if database refresh is finish and refresh folder list.
 * @param parStatusJson - Object that contain result of player status.
 */
function settingsTestRefreshDb(parStatusJson) {
    if (parStatusJson.db_refreshing) {
        if(parStatusJson.db_refreshing=="false" && control_settings_refreshing_db) {
            folderRefreshRoot();
            radioRefreshRoot();
            control_settings_refreshing_db = false;
        }
    }
}


function settingsToggleExpertMode() {
    showSnackbar("The feature is comming soon");
}
