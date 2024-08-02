#import detection model
from PIL import Image
import torch
from torchvision import transforms
from PytorchWildlife.models import detection as pw_detection
import os


# Function to check if the model detects an animal in the image
def contains_animal(image_tensor, detector, threshold=0.5):
    detections = detector.single_image_detection(image_tensor)
    for label in detections['labels']:
        parts = label.split();
        if parts[0] == 'animal' and float(parts[1]) > threshold:
            print("Animal detected")
            return True
    return False


def detect_result(directory, threshold):
    detection_model = pw_detection.MegaDetectorV5()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    convert_tensor = transforms.Compose([transforms.ToTensor()])

    animal_images = []
    photoPaths = os.listdir(directory)
    for i in range(0, len(photoPaths), 3):
        if i + 1 >= len(photoPaths):
            imgPath1 = directory + "/" + photoPaths[i]
            img1 = Image.open(imgPath1).convert('RGB')
            img1 = convert_tensor(img1).to('cuda')
            if contains_animal(img1, detection_model, threshold):
                animal_images.append(imgPath1)
            break
        s1 = torch.cuda.Stream()
        s2 = torch.cuda.Stream()
        imgPath1 = directory + "/" + photoPaths[i]
        imgPath2 = directory + "/" + photoPaths[i+1]
        img1 = Image.open(imgPath1).convert('RGB')
        img2 = Image.open(imgPath2).convert('RGB')
        # convert to Tensor
        
        img1 = convert_tensor(img1).to('cuda', non_blocking=True)
        img2 = convert_tensor(img2).to('cuda', non_blocking=True)

        result1 = None
        result2 = None
       
        if i + 2 >= len(photoPaths):
            # run detection
            torch.cuda.synchronize()
            with torch.cuda.stream(s1):
                
                result1 = contains_animal(img1, detection_model, threshold)
            with torch.cuda.stream(s2):
                result2 = contains_animal(img2, detection_model, threshold)
            torch.cuda.synchronize()
            if result1:
                animal_images.append(imgPath1)
            if result2:
                animal_images.append(imgPath2)
            break;
        
        s3 = torch.cuda.Stream()
        imgPath3 = directory + "/" + photoPaths[i+2]
        img3 = Image.open(imgPath3).convert('RGB')
        img3 = convert_tensor(img3).to('cuda', non_blocking=True)
        print(img3.device)
        # run detection
        torch.cuda.synchronize()
        with torch.cuda.stream(s1):
            result1 = contains_animal(img1, detection_model, threshold)
        with torch.cuda.stream(s2):
            result2 = contains_animal(img2, detection_model, threshold)
        with torch.cuda.stream(s3):
            result3 = contains_animal(img3, detection_model, threshold)
        torch.cuda.synchronize()

        if result1:
            animal_images.append(imgPath1)
        if result2:
            animal_images.append(imgPath2)
        if result3:
            animal_images.append(imgPath3)

    
        print("Finished detection on images " + str(i) + " to " + str(i+2))

    return animal_images, ""
        
# Transform to convert PIL images to tensors
convert_tensor = transforms.Compose([transforms.ToTensor()])


def load_images_as_batch(image_paths, device):
    images = []
    for img_path in image_paths:
        img = Image.open(img_path).convert('RGB')
        img_tensor = convert_tensor(img).to(device)
        images.append(img_tensor)
    # Stack images to create a batch tensor
    batch_tensor = torch.stack(images)
    print(batch_tensor.shape)
    return batch_tensor

# Function to perform batch detection
def batch_contains_animal(image_tensor_batch, detector, threshold=0.5):
    # Perform batch detection
    batch_detections = detector.batch_image_detection(image_tensor_batch) #error here
    
    results = []
    for detections in batch_detections:
        has_animal = False
        for label in detections['labels']:
            parts = label.split()
            if parts[0] == 'animal' and float(parts[1]) > threshold:
                has_animal = True
                break
        results.append(has_animal)
    return results

def batch_detection(directory, threshold):
    detection_model = pw_detection.MegaDetectorV5()
    
    # List of image file paths
    photo_paths = os.listdir(directory)
    photo_paths = [os.path.join(directory, photo) for photo in photo_paths]
    
    # Example: Load a batch of images
    batch_size = 8  # Adjust the batch size as needed
    num_batches = len(photo_paths) // batch_size + int(len(photo_paths) % batch_size != 0)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Loop over batches and process
    animal_images = []
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(photo_paths))
        image_batch = load_images_as_batch(photo_paths[start_idx:end_idx], device)
        print("Shape:")
        print(image_batch.shape)
        # Run batch detection
        results = batch_contains_animal(image_batch, detection_model, threshold)
        
        # Append detected animal images to the list
        for j, result in enumerate(results):
            if result:
                animal_images.append(photo_paths[start_idx + j])



    
    
    




