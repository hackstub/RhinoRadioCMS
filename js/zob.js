




var mescouilles = document.getElementById("zoblink");
mescouilles.addEventListener("click", maFonctionDeMerde);

var zob;

function maFonctionDeMerde(e)
{
    e.preventDefault();
    console.log(e.target.id);
    console.log(e.target.href);
    $( "#main" ).load( e.target.href );

    history.pushState({}, '', e.target.href);
}

window.addEventListener("popstate", function(e) {
  console.log("going back !")
}, false);

