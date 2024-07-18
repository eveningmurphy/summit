function setUp(){
  /*const nav_items = document.querySelectorAll(".nav-item");
  for (var i=0;i<nav_items.length;i++){
    //nav_items[i].removeEventListener("click",updateNavBar(event))
    nav_items[i].addEventListener("click", function(event) {
      updateNavBar(event);
    });
    debugger;
  } */ 
}

function updateNavBar(current_item){
    // Get all navigation items
    const nav_items = document.querySelectorAll('.nav-item');
    console.log(nav_items);

    // Loop through all nav items
    // navItems.forEach(item => {
      for (var i=0;i<nav_items.length;i++){
        // Remove 'active' class from all items
        nav_items[i].classList.remove('active');

        // Add 'active' class to the current item
        if ( nav_items[i].getAttribute('id') === current_item.id) {
          nav_items[i].classList.add('active');
        }
    }//);
}