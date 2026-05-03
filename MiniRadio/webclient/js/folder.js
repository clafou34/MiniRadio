// Templates variables
var folderListTemplate = null;
var folderLiItemTemplate=null;
var folderLiSongItemTemplate=null;

// Root folder HTML element
var folderRoot=null

function folderOnLoad() {
    folderInitialisation();
}

function folderDetailsOnToggle(par_current_html_node) {
    var_folder_li = par_current_html_node.parentElement;

    if(var_folder_li.hasAttribute("data-folder-path")) {
        var_folder_path = var_folder_li.getAttribute("data-folder-path");
        
        var_inner_list = var_folder_li.querySelector("ul.folder-list");
        if(var_inner_list==null) {
            var_node_of_list = var_folder_li.querySelector("details").appendChild(folderListTemplate.cloneNode(true));
            folderListFillContent(var_node_of_list, var_folder_path);
        }
    }
    else {
        console.error("Folder name not in parent attribute.")
    }
    
}

function folderPlayOnClick(par_current_html_node) {
    var_folder_li = par_current_html_node.parentElement.parentElement.parentElement.parentElement;

    if(var_folder_li.hasAttribute("data-folder-path")) {
        var_folder_path = var_folder_li.getAttribute("data-folder-path");
        
        folderAddItem(var_folder_path,true,true);
    }
    else {
        console.error("Folder path not in parent attribute.");
    }
}

function folderAddOnClick(par_current_html_node) {
    var_folder_li = par_current_html_node.parentElement.parentElement.parentElement.parentElement;

    if(var_folder_li.hasAttribute("data-folder-path")) {
        var_folder_path = var_folder_li.getAttribute("data-folder-path");
        
        folderAddItem(var_folder_path,false,false);
    }
    else {
        console.error("Folder path not in parent attribute.");
    }
}


function folderSongPlayOnClick(par_current_html_node) {
    var_song_li = par_current_html_node.parentElement;

    if(var_song_li.hasAttribute("data-item-file")) {
        var_item_file = var_song_li.getAttribute("data-item-file");
        
        folderAddItem(var_item_file,true,true);
    }
    else {
        console.error("Item file not in parent attribute.");
    }
}

function folderSongAddOnClick(par_current_html_node) {
    var_song_li = par_current_html_node.parentElement;

    if(var_song_li.hasAttribute("data-item-file")) {
        var_item_file = var_song_li.getAttribute("data-item-file");
        
        folderAddItem(var_item_file,false,false);
    }
    else {
        console.error("Item file not in parent attribute.");
    }    
}

function folderInitialisation() {
    varFolderLiSongItemTemplate = document.querySelector("#folder-list-template > li.folder-song-item");
    folderLiSongItemTemplate = varFolderLiSongItemTemplate.cloneNode(true);
    varFolderLiSongItemTemplate.remove();

    varFolderLiItemTemplate = document.querySelector("#folder-list-template > li.folder-item");
    folderLiItemTemplate = varFolderLiItemTemplate.cloneNode(true);
    varFolderLiItemTemplate.remove();

    folderRoot = document.querySelector("#folder-list-template");
    folderListTemplate = folderRoot.cloneNode(true);
    folderListTemplate.removeAttribute("id");

    folderRefreshRoot();
}

function folderRefreshRoot() {
    // Clear root content
    while(folderRoot.firstChild) { 
        folderRoot.removeChild(folderRoot.firstChild);
    }

    // Fill root folder
    folderListFillContent(folderRoot);
}

function folderDisplayList(par_json_folder_content, par_html_node_folder_list) {
    if(par_json_folder_content.folders) {
        for (const var_folder_item of par_json_folder_content.folders) {
            var_new_item = folderLiItemTemplate.cloneNode(true);
            var_new_item.querySelector("span[name='folder-title-text']").innerText = var_folder_item.name;
            var_path_attribute = document.createAttribute("data-folder-path");
            var_path_attribute.value = var_folder_item.path;
            var_new_item.setAttributeNode(var_path_attribute);
            par_html_node_folder_list.appendChild(var_new_item);
        }
    }

    if(par_json_folder_content.items) {
        for (const var_song_item of par_json_folder_content.items) {
            var_new_song_item = folderLiSongItemTemplate.cloneNode(true);
            var_new_song_item.children["song-title-text"].innerText = var_song_item.title;
            var_file_attribute = document.createAttribute("data-item-file");
            var_file_attribute.value = var_song_item.file;
            var_new_song_item.setAttributeNode(var_file_attribute);
            par_html_node_folder_list.appendChild(var_new_song_item);
        }
    }

}

function folderListFillContent(par_html_node_folder_list, par_str_folder_path = "") {
    fetch(utilsApiRoot() + `/folders/${par_str_folder_path}`, {method: 'GET', headers: {'Accept': 'application/json'}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('When getting folders, network response was KO ' + response.statusText);
            }
        
        return response.json()
    })
    .then(data => {
        if(data.success) {
            if(data.success == "OK" && data.payload){
                if(data.payload.folders && data.payload.items) {
                    folderDisplayList(data.payload, par_html_node_folder_list);
                }
                else {
                    throw new Error('Folder content not in returned payload.');
                };
            };
        };
    });
}

function folderAddItem(par_str_item_path, par_bool_replace = false, par_bool_play = false) {
    const params = new URLSearchParams();

    params.append("action", "add-to-queue");
    if(par_bool_replace)
        params.append("replace", "true");
    if(par_bool_play)
        params.append("play", "true");

    fetch(utilsApiRoot() + `/folders/${par_str_item_path}?${params}`, {method: 'GET', headers: {'Accept': 'application/json'}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('When adding folder item in queue, network response was KO ' + response.statusText);
            }
        
        return response.json()
    })
    .then(data => {
        if(data.success) {
            if(!par_bool_replace)
                showSnackbar("Added in queue");
            else
                showSnackbar("Queue replaced");
                
            controlManageStatus();
        }
        else {
            throw new Error('Error when adding folder item in queue.');
        }
    });
}