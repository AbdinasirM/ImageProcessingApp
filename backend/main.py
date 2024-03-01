from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from skimage.metrics import structural_similarity
import firebase_admin
from firebase_admin import credentials, storage
import cv2
import numpy as np
from fastapi.responses import JSONResponse
import datetime
import os
# Initialize Firebase Admin SDK
cred = credentials.Certificate("./ccc-hackathon-77a0d-firebase-adminsdk-7lcy1-5d870cc01a.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ccc-hackathon-77a0d.appspot.com'
})

app = FastAPI()

# Allow all origins for demonstration purposes. You may want to restrict this in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_image_to_firebase(image_path, content):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(image_path)

        # Upload the content as bytes
        blob.upload_from_string(content, content_type='image/png')

        # Set the access control to public read
        blob.acl.all().grant_read()
        blob.acl.save()

        # Explicitly check if the blob exists to ensure the upload is complete
        if not blob.exists():
            raise Exception("Error: Blob does not exist. Upload may not be complete.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")

async def compute_and_upload_difference(before_img, after_img, title):
    try:
        print("Computing difference...")
        # Convert images to grayscale
        before_gray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after_img, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between the two images
        (score, diff) = structural_similarity(before_gray, after_gray, full=True)
        print("Image Similarity: {:.4f}%".format(score * 100))

        # The diff image contains the actual image differences between the two images
        # and is represented as a floating point data type in the range [0,1] 
        # so we must convert the array to 8-bit unsigned integers in the range
        # [0,255] before we can use it with OpenCV
        diff = (diff * 255).astype("uint8")

        # Save the before and after images
        before_filename = f'{title}_before.jpg'
        after_filename = f'{title}_after.jpg'
        cv2.imwrite(before_filename, before_img)
        cv2.imwrite(after_filename, after_img)

        # Threshold the difference image to obtain the regions of the two input images that differ
        _, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        # Find contours in the difference image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the after_img to highlight the differences
        cv2.drawContours(after_img, contours, -1, (0, 0, 255), 2)

        # Save the highlighted difference image locally
        diff_highlighted_filename = f'{title}_diffhighlighted.jpg'
        cv2.imwrite(diff_highlighted_filename, after_img)

        print("Difference computation completed.")

        # Upload images to Firebase Storage
        upload_image_to_firebase(before_filename, open(before_filename, 'rb').read())
        upload_image_to_firebase(after_filename, open(after_filename, 'rb').read())
        upload_image_to_firebase(diff_highlighted_filename, open(diff_highlighted_filename, 'rb').read())



        # Generate URL for the difference image and return it in the API response
        firebase_diff_url = generate_image_url(title, 'diffhighlighted')
        
        # Delete local files after successful upload
        os.remove(before_filename)
        os.remove(after_filename)
        os.remove(diff_highlighted_filename)

        
        return {'message': 'Files uploaded and processed successfully',
                'before_image_url': generate_image_url(title, 'before'),
                'after_image_url': generate_image_url(title, 'after'),
                'diff_image_url': firebase_diff_url,
                'similarity_score': score * 100  # Include the similarity score in the response

                }
    except Exception as e:
        # Handle any exceptions during the process
        print(f"Error during compute_and_upload_difference: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_image_url(title, image_type):
    # Construct the image path based on the title and image type
    image_path = f'{title}_{image_type}.jpg'
    # Construct the full URL
    image_url = f'https://storage.googleapis.com/ccc-hackathon-77a0d.appspot.com/{image_path}'
    return image_url

@app.post("/upload-and-process")
async def upload_and_process(title: str = Form(...), artifact1: UploadFile = File(...), artifact2: UploadFile = File(...)):
    try:
        if title and artifact1 and artifact2:
            file_content1 = await artifact1.read()
            file_content2 = await artifact2.read()

            img1 = cv2.imdecode(np.frombuffer(file_content1, dtype=np.uint8), cv2.IMREAD_COLOR)
            img2 = cv2.imdecode(np.frombuffer(file_content2, dtype=np.uint8), cv2.IMREAD_COLOR)

            if img1.shape != img2.shape:
                raise HTTPException(status_code=422, detail="Images must have the same dimensions")

            # Run the compute_and_upload_difference function asynchronously
            await compute_and_upload_difference(img1, img2, title)

            # Generate URLs for the images (before, after, diffhighlighted)
            before_image_url = generate_image_url(title, 'before')
            after_image_url = generate_image_url(title, 'after')
            diffhighlighted_image_url = generate_image_url(title, 'diffhighlighted')

            return {
                'message': 'Files uploaded and processed successfully',
                'before_image_url': before_image_url,
                'after_image_url': after_image_url,
                'diffhighlighted_image_url': diffhighlighted_image_url,
                
            }
        else:
            raise HTTPException(status_code=422, detail="Invalid request")

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during upload_and_process: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-images/{title}")
async def get_images(title: str):
    try:
        # Generate URLs for the images (before, after, diffhighlighted)
        before_image_url = generate_image_url(title, 'before')
        after_image_url = generate_image_url(title, 'after')
        diffhighlighted_image_url = generate_image_url(title, 'diffhighlighted')

        return {
            'before_image_url': before_image_url,
            'after_image_url': after_image_url,
            'diffhighlighted_image_url': diffhighlighted_image_url
        }

    except Exception as e:
        print(f"Error during get_images: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

