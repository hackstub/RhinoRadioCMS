




var mescouilles = document.getElementById("zoblink");
mescouilles.addEventListener("click", maFonctionDeMerde);

var zob;

function maFonctionDeMerde(e)
{
    e.preventDefault();
    console.log(e.target.id);
    console.log(e.target.href);
    $( "#main" ).load( e.target.href );

    //history.pushState({}, '', "bar.html");

}






