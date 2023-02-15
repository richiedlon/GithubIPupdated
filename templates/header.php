<nav class="navbar navbar-dark bg-primary">
  <a class="navbar-brand" href="#">Salzburg Living Condition Assessment Portal</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarText">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a href="/">
                <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#">Home</button></a>
      </li>
      <li class="nav-item">
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bd-example-modal-lg">Find the Most Suitable Area for You</button>
      </li>
      <li class="nav-item">
        <a href="/contact">
                <button type="button" class="btn btn-primary" data-toggle="modal" data-target="contact">Contact Us</button></a>
      </li>
    </ul>
  </div>
</nav>

<!-- Modal -->
<div class="modal fade bd-example-modal-lg" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Enter your Living Condition Preference (Value = 10 Highest consideration)</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        
        <!-- link to the form -->
        {% include 'livingconditionform.php' %}
        
      </div>

    </div>
  </div>
</div>