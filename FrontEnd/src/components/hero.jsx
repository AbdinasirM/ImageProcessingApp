
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
              This system takes both a "before" image and an "after" image,
              sending them to the backend for processing. The backend utilizes
              OpenCV, a machine learning library in Python, to analyze the
              images. The result is a new image that highlights the areas where
              something is missing in the "after" image, marked with a red
              highlight.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div className="col-lg-6 col-md-12 ">
      <img
        src="/public/imageDifference.png"
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
