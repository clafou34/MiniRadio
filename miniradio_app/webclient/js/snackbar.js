function showSnackbar(var_str_message) {
  var x = document.getElementById("snackbar");
  x.innerText = var_str_message
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}
