from django.shortcuts import render
from django.template import RequestContext
from app.forms import UploadFileForm
from PIL import Image, ImageOps,ImageFilter
from django.templatetags.static import static
import boto3
from os.path import exists
from time import time_ns
from project_1.settings import OUTPUT_DIR, MEDIA_DIR, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Amazon AWS S3 Storage
s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
bucket = 'p1storage'

def applyfilter(filename, preset):
    inputfile = MEDIA_DIR + filename

    f = filename.split('.')
    # add time in ns to prevent caching of images
    outputfilename = f[0] + '-' + str(time_ns()) + '.' + f[1]
    outputfile = OUTPUT_DIR + outputfilename

    image = Image.open(inputfile)

    if preset == 'gray':
        image = ImageOps.grayscale(image)

    if preset == 'edge':
        image = ImageOps.grayscale(image)
        image = image.filter(ImageFilter.FIND_EDGES)

    if preset == 'poster':
        image = ImageOps.posterize(image,3)

    if preset == 'solar':
        image = ImageOps.solarize(image, threshold=80) 

    if preset == 'blur':
        image = image.filter(ImageFilter.BLUR)

    if preset == 'sepia':
        sepia = []
        r, g, b = (239, 224, 185)
        for i in range(255):
            sepia.extend((r*i//255, g*i//255, b*i//255))
        image = image.convert("L")
        image.putpalette(sepia)
        image = image.convert("RGB")

    image.save(outputfile)

    while exists(outputfile) == False:
        continue

    return outputfilename

def handle_uploaded_file(f,preset):
    uploadfilename = MEDIA_DIR + f.name
    with open(uploadfilename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Try to apply filter otherwise return None
    try:
        outputfilename = applyfilter(f.name, preset)
    except:
        outputfilename = None
    return outputfilename

def home(request):
    # if serving a request from the form
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # if the submitted form is a valid form
        if form.is_valid():
            preset = request.POST.get('preset', False)
            outputfilename = handle_uploaded_file(request.FILES['myfilefield'],preset)
            # error applying filter, alert user with error message.
            if outputfilename == None:
                return render(request, 'index.html', {'form': form, 'errormsg': 'Error: Could not apply filter! Make sure the file submitted is an image with an image file extension (Ex. `.png`, `.jpeg`, etc.)'})
            # filter was successfully applied to the image, redirect the user to the process page
            print(f'Uploading `{outputfilename}` to AWS S3 Storage...')
            s3.Bucket(bucket).upload_file(OUTPUT_DIR + outputfilename, outputfilename)
            print(f'Uploaded `{outputfilename}` to AWS S3 Storage!')
            return render(request, 'process.html', {'outputfilename': outputfilename, 'preset': preset.capitalize(), 'bucket': bucket})
    # if not yet serving a request from the form
    else:
        form = UploadFileForm() 
    return render(request, 'index.html', {'form': form})

def process(request):
    return render(request, 'process.html')
