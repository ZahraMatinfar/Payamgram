let searchInput = document.getElementById("search-input");

searchInput.addEventListener("focus", function() {
    searchInput.style.textAlign = "left";
    document.getElementById("search-icon").style.left = 9;
}, false);

searchInput.addEventListener("blur", function() {
    searchInput.style.textAlign = "center";
    document.getElementById("search-icon").style.left = "31%";
}, false);