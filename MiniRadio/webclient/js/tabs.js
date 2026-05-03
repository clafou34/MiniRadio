var tabsCurrent = "queue" // Possibles values are "radio", "folder", "queue"

function tabsBtnGoToFoldersOnClick() {
    if(tabsCurrent != "folder") {
        tabsCurrent = "folder";
        tabsShowCurrent();
    }
}

function tabsBtnGoToRadiosOnClick() {
    if(tabsCurrent != "radio") {
        tabsCurrent = "radio";
        tabsShowCurrent();
    }
}

function tabsBtnGoToQueueOnClick() {
    if(tabsCurrent != "queue") {
        tabsCurrent = "queue";
        tabsShowCurrent();
    }
}

function tabsShowCurrent() {
    if(tabsCurrent == "folder") {
        document.getElementById("btn-go-to-folders").setAttribute("class","current-tab");
        document.getElementById("btn-go-to-radios").setAttribute("class","not-current-tab");
        document.getElementById("btn-go-to-queue").setAttribute("class","not-current-tab");
        document.getElementById("queue-section").style.display = "none";
        document.getElementById("folders-section").style.display = "block";
        document.getElementById("radios-section").style.display = "none";
    }
    else if(tabsCurrent == "radio") {
        document.getElementById("btn-go-to-folders").setAttribute("class","not-current-tab");
        document.getElementById("btn-go-to-radios").setAttribute("class","current-tab");
        document.getElementById("btn-go-to-queue").setAttribute("class","not-current-tab");
        document.getElementById("queue-section").style.display = "none";
        document.getElementById("folders-section").style.display = "none";
        document.getElementById("radios-section").style.display = "block";
    }
    else if(tabsCurrent == "queue") {
        document.getElementById("btn-go-to-folders").setAttribute("class","not-current-tab");
        document.getElementById("btn-go-to-radios").setAttribute("class","not-current-tab");
        document.getElementById("btn-go-to-queue").setAttribute("class","current-tab");
        document.getElementById("queue-section").style.display = "block";
        document.getElementById("folders-section").style.display = "none";
        document.getElementById("radios-section").style.display = "none";
    }
}