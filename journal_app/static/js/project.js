function ConfirmAction(msg, pk){
    // triggers a popup to make sure user is ok with a destructive operation
    if(confirm(msg)){
        fetch("/journal/contact/" + pk + "/delete/").then(r => location.reload());
    } else {
        return false;
    }
}
