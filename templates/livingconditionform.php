<div class="wrap">
    <form id="upload-form" action="/living" method="POST" enctype="multipart/form-data">
    
            <div class="slidecontainer">
                <p>1. Level of consideration for Ambulances</p>
                <input type="range" min="1" max="10" class="slider" id="myRangeAmbu" name="Ambuvalue">
                <p>Value: <span id="demoAmbu"></span></p>
            </div>
            <script>
            var slider = document.getElementById("myRangeAmbu");
            var outputAmbu = document.getElementById("demoAmbu");
            outputAmbu.innerHTML = slider.value;

            slider.oninput = function() {
              outputAmbu.innerHTML = this.value;
            }
            </script>

<br>
            <div class="slidecontainer">
                <p>2. Level of consideration for Hospitals</p>
                <input type="range" min="1" max="10" class="slider" id="myRangeHosp" name="Hospvalue">
                <p>Value: <span id="demoHosp"></span></p>
            </div>
            <script>
            var slider = document.getElementById("myRangeHosp");
            var outputHosp = document.getElementById("demoHosp");
            outputHosp.innerHTML = slider.value;

            slider.oninput = function() {
              outputHosp.innerHTML = this.value;
            }
            </script>

<br>
            <div class="slidecontainer">
                <p>3. Level of consideration for Fire and Rescue Services</p>
                <input type="range" min="1" max="10" class="slider" id="myRangeFire" name="firevalue">
                <p>Value: <span id="demoFire"></span></p>
            </div>
            <script>
            var slider = document.getElementById("myRangeFire");
            var outputFire = document.getElementById("demoFire");
            outputFire.innerHTML = slider.value;

            slider.oninput = function() {
              outputFire.innerHTML = this.value;
            }
            </script>

<br>
            <div class="slidecontainer">
                <p>4. Level of consideration for Super Markets</p>
                <input type="range" min="1" max="10" class="slider" id="myRangeMarkets" name="marketvalue">
                <p>Value: <span id="demoMarkets"></span></p>
            </div>
            <script>
            var slider = document.getElementById("myRangeMarkets");
            var outputMarkets = document.getElementById("demoMarkets");
            outputMarkets.innerHTML = slider.value;

            slider.oninput = function() {
              outputMarkets.innerHTML = this.value;
            }
            </script>

<br>
            <div class="slidecontainer">
                <p>5. Level of consideration for Parks and Green Spaces</p>
                <input type="range" min="1" max="10" class="slider" id="myRangeParks" name="parkvalue">
                <p>Value: <span id="demoParks"></span></p>
            </div>
            <script>
            var slider = document.getElementById("myRangeParks");
            var outputParks = document.getElementById("demoParks");
            outputParks.innerHTML = slider.value;

            slider.oninput = function() {
              outputParks.innerHTML = this.value;
            }
            </script>

<br>
            <div class="slidecontainer">
                <p>6. Level of consideration for school accessibility</p>
                <input type="range" min="1" max="10" class="slider" id="myRangeSchools" name="schoolvalue">
                <p>Value: <span id="demoSchools"></span></p>
            </div>
            <script>
            var slider = document.getElementById("myRangeSchools");
            var outputSchools = document.getElementById("demoSchools");
            outputSchools.innerHTML = slider.value;

            slider.oninput = function() {
              outputSchools.innerHTML = this.value;
            }
            </script>

<br>
            <div class="slidecontainer">
<<<<<<< Updated upstream
                <p>Enter your Email address</p>
                <input type="email" class="slider" id="emailRecipient" name="emailRecipient">
            </div>
<br> 
        
=======
                <p>Enter your Email address to recieve coordinates of apartments</p>
                <input type="email" class="slider" id="emailRecipient" name="emailRecipient">
            </div>
<br>
>>>>>>> Stashed changes
        <div class="buttons">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>


    </form>
</div>
        