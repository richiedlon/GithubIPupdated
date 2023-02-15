<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.png') }}" />
	  <link rel="stylesheet" href="static/css/sliders.css"/>

    <!-- Page loading indicator-->
    <link rel="stylesheet" href="static/css/pace-theme-center-atom.css"/>
    <script src="static/js/pace.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
    integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
    crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"
    integrity="sha256-WBkoXOwTeyKclOHuWtc+i2uENFpDZ9YPdf5Hf+D7ewM="
    crossorigin=""></script>
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="static/css/contact.css">
    
    <!-- Navigation Bar-->
    <script src="static/js/NavBar.js"></script>

    <!-- Font and bootstrap plugin--> 
    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    
    <!-- jquery-->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    
    <style>
    body {
      background-image: url('static/img/img.jpg');
      background-repeat: no-repeat;
      background-attachment: fixed;
      background-size: cover;
    }
    </style>
  </head>
  
  <body>
    <!-- link to the header.php -->
  	{% include 'header.php' %}
      
      <div id="container">
        <div  class="textbox">
          <h3 class="text-uppercase">Contact Form</h3>
          <div class="buffer"></div>
          <h5 class="describe">How was your experience using our app? We would love to hear from you!</h5>
          <div class="buffer"></div>
        </div>
      <div class ="row">
        <div class = "col">
          <div class="mapform" >
            <form action="https://formsubmit.co/f9b8e76c5c355bca4570bc313482a1ef" method="POST">
                <div class="form-control">
                    <div class="form-group">
                        <label class="label">Full Name</label>
                        <input id="form_name" type="text" name="name" class="form-control" placeholder="Full Name" name="full name" required="required" data-error="Name is required.">
                        <div class="form-control-border"></div>
                        <div class="help-block with-errors"></div>
                    </div>

                    <div class="form-group">
                        <label class="label">Email Address</label>
                        <input id="form_email" type="email" name="email" class="form-control" placeholder="Email Address" name="email" required="required" data-error="Valid email is required.">
                        <div class="form-control-border"></div>
                        <div class="help-block with-errors"></div>
                    </div>

                    <div class="form-group">
                      <label class="label">Message</label>
                        <textarea id="form_message" name="message" class="form-control" placeholder=" Your message goes here" rows="4" name="message/comment"  required="required" data-error="Please, leave us a message."></textarea>
                        <div class="form-control-border"></div>
                        <div class="help-block with-errors"></div>
                    </div>

                    <input type="submit" class="button btn btn-primary btn-send" value="Send message">
                </div>
             </form>
          </div>
        </div>

        <!-- The leaflet location map -->
        <div class="col">
          <div id="map"></div>
        </div>
      </div>
    
    <!-- leaflet map javascript -->
    <script>
      var map = L.map('map').setView([47.823092359253536, 13.039849629205637], 15);

      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

      var marker = L.marker([47.823092359253536, 13.039849629205637]).addTo(map);
      marker.bindPopup("<b>Proudly developed at Techno-Z!").openPopup();
    </script>
    
  </body>
</html>

