$(document).ready(function(){
  $('form input').change(function ()
  {
    var fullPath = this.value;
    if (fullPath)
    {
      var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
      var filename = fullPath.substring(startIndex);
      if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0)
      {
          filename = filename.substring(1);
      }
    }
    var res = filename.slice(0,-4);
    $('form p').text(filename);
    document.getElementById("title").value = res;
  });
});
