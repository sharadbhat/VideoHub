$(document).ready(function(){
  $('form input').change(function () {
    var fullPath = this.value;
    var filename = fullPath.match(/^.*?([^\\/.]*)[^\\/]*$/)[1];
    $('form p').text(filename + " selected");
    var f2 = filename;
    document.getElementById("title").value = f2;
  });
});
