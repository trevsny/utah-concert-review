
            // Venue Filter
            $("#ajax_venue_name").keyup(function(){
                $("#ajax_artist_name").val("")
                $.ajax({
                    url: '/filterbyvenue',
                    method: "get",
                    data: $(this).parent().serialize(),
                    success: function(serverResponse){
                        // console.log("success", serverResponse)
                        $("#placeholder1").html(serverResponse)
                    }
                }) 
            });
            // Artist Filter
            $("#ajax_artist_name").keyup(function(){
                $("#ajax_venue_name").val("")
                $.ajax({
                    url: '/filterbyartist',
                    method: "get",
                    data: $(this).parent().serialize(),
                    success: function(serverResponse){
                        // console.log("success", serverResponse)
                        $("#placeholder1").html(serverResponse)
                    }
                }) 
            });
            // Date Filter
            $("#ajax_month").change(function(){
                $("#ajax_venue_name").val("")
                $("#ajax_artist_name").val("")
                $.ajax({
                    url: '/filterbydate',
                    method: "get",
                    data: $(this).parent().serialize(),
                    success: function(serverResponse){
                        // console.log("success", serverResponse)
                        $("#placeholder1").html(serverResponse)
                    }
                }) 
            });
            // Show all concerts
            $("#showAll").click(function(){
                $("#ajax_venue_name").val("")
                $("#ajax_artist_name").val("")
                $.ajax({
                    url:'/showAll',
                    method: "get",
                    success: function(serverResponse){
                        console.log("success")
                        $("#placeholder1").html(serverResponse)
                    }
                })
            });
            //Run scrapy spider
            $("#scrape").click(function(){
                alert("Looking for new concerts -- please allow at least 15 seconds")
                $.ajax({
                    url: '/scrape',
                    method: "post",
                    success: function(serverResponse){
                        console.log("Success")
                        $("#placeholder1").html(serverResponse)
                    }
                })
            });
            //Show no concerts
            $("#showNone").click(function(){
                $("#placeholder1").html("<h3 class = 'mx-auto' style = 'color:black;' >No concerts displayed</h3")
            })
            //lazy loading for images
            var bLazy = new Blazy();
           //if img doesn't load, load the ucr.jpg
           $('img').on("error", function(){
               $(this).attr('src', 'static/ucr.jpg');
           });
    