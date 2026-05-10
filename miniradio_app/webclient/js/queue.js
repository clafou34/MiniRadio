// Get list element template
const queueListItemTemplate = document.getElementById('queue-list-item-template');
queueListItemTemplate.removeAttribute("id");

function queueOnLoad() {
    queueRefresh();
}

/**
 * Handles the click event for removing a queue item.
 * This function removes the clicked queue item from the DOM, sends a request to remove it from the server,
 * and updates the control status.
 *
 * @param {Event} evt - The click event object that triggered this function.
 *                      This parameter contains information about the event,
 *                      including the target element that was clicked.
 */
function queueRemoveBtnOnClick(evt) {
    // Get parent element which has id of song to remove.
    var_item_li = evt.currentTarget.parentElement;

    // Check if "data-item-id" attribute is define.
    if(var_item_li.hasAttribute("data-item-id")) {
        var_item_id = var_item_li.getAttribute("data-item-id");

        // Hide the element so that the user cannot perform 2 deletions on the same item.
        var_item_li.remove();

        // Remove item in player queue
        queueRemoveItem(var_item_id);

        // Update status
        controlManageStatus();

    }
    else {
        console.error("Item id not in parent attribute.")
    }
}

function queueRemoveItem(parItemId) {
        fetch(utilsApiRoot() + "/queue/items/" + String(parItemId), {method: 'DELETE', headers: {'Accept': 'application/json'}
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('When removing queue item, network response was KO ' + response.statusText);
                }
            
            return response.json()
            })
        .then(data => {
            if(data.success) {
                if(data.success == "OK"){
                    showSnackbar("Item removed from queue");
                }
            }
        })
    }

/**
 * Handles the click event for clearing the queue.
 * This function clears the queue and updates the control status.
 * It is typically used as an event listener for a button click.
 *
 * @param {Event} evt - The click event object that triggered this function.
 *                      This parameter contains information about the event,
 *                      including the target element that was clicked.
 */
function queueClearBtnOnClick(evt) {
    queueClear();

    // Update status
    controlManageStatus();
}

function queueClear() {
        const params = new URLSearchParams();

        params.append("action", "clear");
        fetch(utilsApiRoot() + `/queue/items?${params}`, {method: 'GET', headers: {'Accept': 'application/json'}
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('When clearing queue, network response was KO ' + response.statusText);
                }
            
            return response.json()
            })
        .then(data => {
            if(data.success) {
                if(data.success == "OK"){
                    queueRefresh();
                    showSnackbar("Queue cleared");
                }
                else {
                    throw new Error('Error when clearing queue.');
                };
            };
        });

}

/**
 * Refreshes the queue by fetching the current list of items from the server.
 * This function sends a GET request to the queue items endpoint and updates the queue display
 * with the returned items.
 */
function queueRefresh() {
    fetch(utilsApiRoot() + "/queue/items", {method: 'GET', headers: {'Accept': 'application/json'}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('When getting queue items, network response was not ok ' + response.statusText);
            }
        
        return response.json()
    })
    .then(data => {
        if(data.success) {
            if(data.success == "OK" && data.payload){
                if(data.payload.items) {
                    queueDisplayList(data.payload.items);
                }
                else {
                    throw new Error('Items not in returned payload.');
                };
            };
        };
    });
}


function queueDisplayList(parItemList) {
    queueContent = document.querySelector("#queue-list > form > ul");

    // Clear content
    while(queueContent.firstChild) { 
        queueContent.removeChild(queueContent.firstChild); 
    } 

    // Insert new items
    for (const var_item of parItemList) {
        var queueNewItem = queueContent.appendChild(queueListItemTemplate.cloneNode(true));

        // Create attribute id for <li> node
        var_item_id_attribute = document.createAttribute("data-item-id");
        var_item_id_attribute.value = var_item.id;
        queueNewItem.setAttributeNode(var_item_id_attribute);

        // Set id for <radio> button
        queueNewItem.children["queue-current-item"].setAttribute("id","queue-item-id-" + var_item.id);
        queueNewItem.children["label-queue-current-item"].setAttribute("for","queue-item-id-" + var_item.id); 

        // Set value for <radio> button
        queueNewItem.children["queue-current-item"].setAttribute("value", var_item.id);

        if(var_item.queued_item.name.length>0)
            queueNewItem.children["label-queue-current-item"].innerText = var_item.queued_item.name;
        else
            queueNewItem.children["label-queue-current-item"].innerText = var_item.queued_item.title;
        queueNewItem.children["removeBtn"].addEventListener('click', queueRemoveBtnOnClick);
    }

    queueCheckCurrentItem();
}

function queueCheckCurrentItem() {
    // Get HTML node for radio group
    var_radio_group_node = document.forms["queue-form"].elements["queue-current-item"];

    // Get id of current playing item
    var_current_playing_item_id = document.getElementById("current-item-id").value;

    // If current playing item is not checked then changing checked item.
    if(var_radio_group_node)
        if(var_current_playing_item_id!="" && var_current_playing_item_id!=var_radio_group_node.value)
            var_radio_group_node.value = var_current_playing_item_id;
}

function queueCurrentItemOnChange(par_current_html_node) {
    var_li_html_node = par_current_html_node.parentElement;

    if(var_li_html_node.hasAttribute("data-item-id")) {
        var_song_id = var_li_html_node.getAttribute("data-item-id");

        queueSetCurrentPlayingSong(var_song_id);
    }
    else {
        console.error("No song id in parent node.");
    }  
}

/**
 * Sets the current playing song in the player by sending a request to the server.
 * This function sends a POST request to the player endpoint with the song ID to play.
 *
 * @param {string} parSongId - The ID of the song to set as the current playing song.
 */
function queueSetCurrentPlayingSong(parSongId) {
        const options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json','Accept': 'application/json'},
            body: JSON.stringify({
                action: 'play',
                id: String(parSongId)
            })
        }

        fetch(utilsApiRoot() + `/player`, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('When changing current playing song, network response was KO ' + response.statusText);
                }
            
            return response.json()
            })
        .then(data => {
            if(data.success) {
                if(data.success == "OK"){
                    controlManageStatus();
                }
                else {
                    throw new Error('Error when changing current playing song.');
                };
            };
        });
}



