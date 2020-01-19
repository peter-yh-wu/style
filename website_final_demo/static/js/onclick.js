function clickButton(name) {
  var names = ["musk", "obama", "trump"];
  for (var i = 0; i < names.length; i++) {
    otherName = names[i];
    document.getElementById(otherName).setAttribute("class", "unclicked");
  }
  document.getElementById(name).setAttribute("class", "clicked");
  document.getElementById("name").innerHTML = name;
}

