function login()
{
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();

    if(username=="")
    {
        alert("Username cannot be empty.");
        return false;
    }

    if(password=="")
    {
        alert("password cannot be empty.");
        return false;
    }

    var spinner = document.getElementById("spinner");
    var element = document.getElementById("submit");

    spinner.className = "fa fa-spinner fa-spin spinner";

    element.style.opacity = ".5";
    element.disabled = true;
}