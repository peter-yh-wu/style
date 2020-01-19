function translateText() {
  let text = document.getElementById("text");

  var formData = new FormData();
  var input = document.getElementById("inputtext").value;
  formData.append("input", input);

  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("outputtext").innerHTML = request.responseText;
    }
  };

  request.open("POST", "http://34.83.30.177:5000/elon")
  //request.open("POST", "http://localhost:5001/");
  request.send(formData);
  return false;
}
