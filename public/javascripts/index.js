
document.getElementById('search-button').addEventListener('click',function(){
    var query =encodeURIComponent(document.getElementById('search').value);
    var sort = encodeURIComponent(document.querySelector("#sort-type>option:checked").value);
    var title = encodeURIComponent(document.getElementById('checkbox_title').checked ? 1 : 0);
    var req = new XMLHttpRequest();
    req.open('GET','/api?q='+query+"&s="+sort+"&t="+title,true);
    req.onload = function(){
      document.getElementsByClassName("result-container")[0].outerHTML =  req.responseText;
    };
    req.send();
});
// Get the input field
var input = document.getElementById("search");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("search-button").click();
  }
});
