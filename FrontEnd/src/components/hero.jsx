
function Hero() {
  return (
    <>
<div className="container mt-3">
  <div className="row">
    <div className="col-lg-6 col-md-12 text-center d-flex align-items-center">
      <div className="container mt-3">
        <div className="row justify-content-center">
          <div className="col-md-8 col-sm-12 text-center">
            <h2 id="header1">Image Processing App</h2>
            <p id="description" className="fs-5">
            This system works with two pictures – a 'before' and an 'after.' Both pictures need to be the same size for the system to do its magic. The backend, powered by OpenCV in Python, analyzes these images. The end result is a new picture that shows where things are missing in the 'after' image, highlighted in red.            </p>
          </div>
        </div>
      </div>
    </div>
    <div className="col-lg-6 col-md-12 ">
      <img
        src="/banner.png"
        className="img-fluid"
        alt="..."
      />
    </div>
  </div>
</div>







    


    </>
  );
}

export default Hero;
