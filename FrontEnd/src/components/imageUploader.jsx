import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

const UploadComponent = () => {
  const { register, handleSubmit } = useForm();
  const [beforeImage, setBeforeImage] = useState(null);
  const [afterImage, setAfterImage] = useState(null);
  const [diffImage, setDiffImage] = useState(null);
  const [similarityScore, setSimilarityScore] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // New state to track loading



  const getRandomTitle = () => {
    return Math.floor(Math.random() * 1000000).toString();
  };

  const onSubmit = async (data) => {
    const randomTitle = getRandomTitle();
    setIsLoading(true); // Set loading to true when upload button is clicked

    console.log('Random Title:', randomTitle);

    const formData = new FormData();
    formData.append('title', randomTitle);
    formData.append('artifact1', data.artifact1[0]);
    formData.append('artifact2', data.artifact2[0]);

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload-and-process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log(response.data);

      // Set the URLs for the images after successful processing
      setBeforeImage(response.data.before_image_url);
      setAfterImage(response.data.after_image_url);
      setDiffImage(response.data.diffhighlighted_image_url);
      setSimilarityScore(response.data.similarity_score);

    } catch (error) {
      console.error('Error uploading files:', error);
    }finally {
        setIsLoading(false); // Set loading back to false when upload is complete
      }
    };

 

  return (
    <div className="container mt-5">
    <div className="row justify-content-center">
      <div className="col-md-6">
        <form onSubmit={handleSubmit(onSubmit)} className="row g-3">
          <div className="col-md-6">
            <label htmlFor="artifact1" className="form-label fs-4">
              Upload the before image:
            </label>
            <input type="file" className="form-control" {...register('artifact1')} id="artifact1" />
          </div>
          <div className="col-md-6">
            <label htmlFor="artifact2" className="form-label fs-4">
              Upload the after image:
            </label>
            <input type="file" className="form-control" {...register('artifact2')} id="artifact2" />
          </div>
  
          
            <button type="submit" className="btn btn-primary btn-lg">
              Upload
            </button>
         
        </form>
      </div>
    </div>


      <div className="row mt-3 justify-content-center">
      {isLoading && (
  <div className="col-md-4 mt-4 mb-4 col-sm-12 col-lg-3">
    <div className="card is-loading">
      <div className="image"></div>
      <div className="content">
        
      <div className="card-body">
        <h5 className="card-title">Processing images</h5>
        </div>
      </div>
    </div>
  </div>
)}
{isLoading && (
  <div className="col-md-4 mt-4 mb-4 col-sm-12 col-lg-3">
    <div className="card is-loading">
      <div className="image"></div>
      <div className="content">
        
      <div className="card-body">
        <h5 className="card-title">Processing images</h5>
        </div>
      </div>
    </div>
  </div>
)}

{isLoading && (
  <div className="col-md-4  mt-4 mb-4 col-sm-12 col-lg-3">
    <div className="card is-loading">
      <div className="image"></div>
      <div className="content">
        
        <div className="card-body">
        <h5 className="card-title">Processing images</h5>
        </div>
      </div>
    </div>
  </div>
)}



            {!isLoading && beforeImage && (
              <div className="col-md-4 mt-4 col-sm-12 col-lg-3">
                <div className="card">
                  <img src={beforeImage} className="card-img-top" alt="Before Image" />
                  <div className="card-body">
                    <h5 className="card-title">Before Image</h5>
                  </div>
                </div>
              </div>
            )}

            {!isLoading && afterImage && (
              <div className="col-md-4 mt-4 col-sm-12 col-lg-3">
                <div className="card">
                  <img src={afterImage} className="card-img-top" alt="After Image" />
                  <div className="card-body">
                    <h5 className="card-title">After Image</h5>
                  </div>
                </div>
              </div>
            )}

            {!isLoading && diffImage && (
              <div className="col-md-4 mt-4 mb-4 col-sm-12 col-lg-3">
                <div className="card">
                  <img src={diffImage} className="card-img-top" alt="Difference Image" />
                  <div className="card-body">
                    <h5 className="card-title">Difference Image</h5>
                    
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
    
  );
};



export default UploadComponent;