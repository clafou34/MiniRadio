// Templates variables
var radioLiItemTemplate = null;
var radioLiSelectionTemplate=null;
var radioListTemplate=null;

// Root list HTML element
var radioRoot=null;


function radioOnLoad() {
    radioInitialisation();
}

function radioInitialisation() {
    // Get radio item template
    var varRadioLiItemTemplate = document.querySelector("#radio-list-template > li.folder-song-item");
    radioLiItemTemplate = varRadioLiItemTemplate.cloneNode(true);
    varRadioLiItemTemplate.remove();

    // Get selection item template
    var varRadioLiSelectionTemplate = document.querySelector("#radio-list-template > li.folder-item");
    radioLiSelectionTemplate = varRadioLiSelectionTemplate.cloneNode(true);
    varRadioLiSelectionTemplate.remove();

    // Get list of radios items
    radioRoot = document.querySelector("#radio-list-template");
    radioListTemplate = radioRoot.cloneNode(true);
    radioListTemplate.removeAttribute("id");

    radioFillSelectionList(radioRoot);
}

function radioRefreshRoot() {
    // Clear root content
    while(radioRoot.firstChild) { 
        radioRoot.removeChild(radioRoot.firstChild);
    }

    // Fill root list
    radioFillSelectionList(radioRoot);
}

function radioSelectionDetailsOnToggle(par_current_html_node) {
    var_selection_li = par_current_html_node.parentElement;

    if(var_selection_li.hasAttribute("data-playlist-index")) {
        var_playlist_index = var_selection_li.getAttribute("data-playlist-index");
        
        var_inner_list = var_selection_li.querySelector("ul.folder-list");
        if(var_inner_list==null) {
            var_node_of_list = var_selection_li.querySelector("details").appendChild(radioListTemplate.cloneNode(true));
            radioFillSelectionItemsList(var_node_of_list, var_playlist_index);
        }
    }
    else {
        console.error("Folder name not in parent attribute.")
    }
}

function radioFillSelectionItemsList(par_list_html_node, par_selection_index) {
    fetch(utilsApiRoot() + `/playlists/${par_selection_index}/items`, {method: 'GET', headers: {'Accept': 'application/json'}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('When getting items of radio selection, network response was KO ' + response.statusText);
            }
        
        return response.json()
    })
    .then(data => {
        if(data.success) {
            if(data.success == "OK" && data.payload){
                if(data.payload.items) {
                    radioDisplaySelectionItemsList(data.payload.items, par_list_html_node);
                }
                else {
                    throw new Error('Playlist items not in returned payload.');
                };
            };
        };
    });
}

function radioDisplaySelectionItemsList(parQueuedItems, par_list_html_node) {
    // Populate items list with radios of current selection
    for (const var_queued_item of parQueuedItems) {
        var_new_radio_item = radioLiItemTemplate.cloneNode(true);
        var_new_radio_item.children["song-title-text"].innerText = var_queued_item.item.mr_stream_name;
        var_playlist_index_attribute = document.createAttribute("data-playlist-index");
        var_playlist_index_attribute.value = var_queued_item.item.mr_playlist_index;
        var_new_radio_item.setAttributeNode(var_playlist_index_attribute);
        var_item_index_attribute = document.createAttribute("data-item-index");
        var_item_index_attribute.value = var_queued_item.index;
        var_new_radio_item.setAttributeNode(var_item_index_attribute);
        par_list_html_node.appendChild(var_new_radio_item);
    }
}

function radioDisplaySelectionList(par_playlists, par_selection_list_html_node) {
    // Populate selection list with radio selections
    for (const var_playlist of par_playlists) {
        var_new_item = radioLiSelectionTemplate.cloneNode(true);
        var_new_item.querySelector("span[name='folder-title-text']").innerText = var_playlist.name;
        var_playlist_index_attribute = document.createAttribute("data-playlist-index");
        var_playlist_index_attribute.value = var_playlist.index;
        var_new_item.setAttributeNode(var_playlist_index_attribute);
        par_selection_list_html_node.appendChild(var_new_item);
    }
}

function radioFillSelectionList(par_selection_list_html_node) {
    const params = new URLSearchParams();

    params.append("type", "webradio");
    fetch(utilsApiRoot() + `/playlists/list?${params}`, {method: 'GET', headers: {'Accept': 'application/json'}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('When getting radio selections, network response was KO ' + response.statusText);
            }
        
        return response.json()
    })
    .then(data => {
        if(data.success) {
            if(data.success == "OK" && data.payload){
                if(data.payload.playlists) {
                    radioDisplaySelectionList(data.payload.playlists, par_selection_list_html_node);
                }
                else {
                    throw new Error('Playlists not in returned payload.');
                };
            };
        };
    });
}

/**
 * Handles the click event on a radio play button
 * @param {HTMLElement} par_current_html_node - The HTML node of the clicked play button
 */
function radioBtnPlayOnClick(par_current_html_node) {
    var_radio_parent = par_current_html_node.parentElement;
    var_playlist_index = var_radio_parent.getAttribute("data-playlist-index");
    var_item_index = var_radio_parent.getAttribute("data-item-index");

    // Launch item playing
    radioPlayItem(var_playlist_index, var_item_index);

    // Refresh status
    controlManageStatus();
}

/**
 * Play a specific radio item from a playlist
 * @param {string} parSelectionId - The ID of the playlist containing the radio item
 * @param {string} parItemId - The ID of the radio item to play
 */
function radioPlayItem(parSelectionId, parItemId) {
    const params = new URLSearchParams();

    params.append("action", "add-to-queue");
    params.append("replace", "true");
    params.append("play", "true");
    fetch(utilsApiRoot() + `/playlists/${parSelectionId}/items/${parItemId}?${params}`, {method: 'GET', headers: {'Accept': 'application/json'}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('When adding radio item in queue, network response was KO ' + response.statusText);
            }
        
        return response.json()
    })
    .then(data => {
        if(data.success) {
            showSnackbar("Radio pushed in queue");
        }
        else {
            throw new Error('Error when adding radio item in queue.');
        };
    });
}


