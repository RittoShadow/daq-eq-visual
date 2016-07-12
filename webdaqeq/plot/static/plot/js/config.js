function enable(){
  var isDisabled = !document.getElementById("check").checked;
  document.getElementById("usr").disabled = isDisabled;
  document.getElementById("pwd").disabled = isDisabled;
}

function startDAQEQ(){
  return true;
}

function stopDAQEQ(){
  return true;
}
