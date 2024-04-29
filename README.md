# Colony Counter
This repository hosts a Python script utilizing OpenCV to automatically count bacterial colonies in petri dishes. The script employs various image processing techniques to isolate and enumerate colonies efficiently and accurately.

## Features
- **Interactive Image Selection**: Use a graphical interface to select an image of a petri dish.
- **Automatic Resizing**: Adjust images to a standard size while maintaining aspect ratio for consistent processing.
- **Grid Overlay**: Apply a reference grid to the image, aiding in manual adjustments or assessments.
- **ROI Selection**: Manually select regions of interest within the image for focused analysis.
- **Image Cropping**: Isolate the selected ROI for detailed processing.
- **Contrast Enhancement**: Use blackhat morphological transformations to improve visibility of colonies against the medium.
- **Binary Thresholding**: Simplify the image to binary form to facilitate colony detection.
- **Noise Reduction**: Clean up the image background using morphological operations.
- **Watershed Algorithm**: Segment the image to distinguish individual colonies.
- **Counting and Visualization**: Calculate and display the number of colonies, highlighting each detected colony.

## Prerequisites
Ensure these prerequisites are installed on your system:

- Python 3.x
- OpenCV
- NumPy
- Tkinter
Install the required libraries using pip:

```bash
pip install opencv-python numpy
```

## Usage
1.Download the script or clone this repository.

2.Run the script:

```bash
python colony_counter.py
```
3.Follow the GUI prompts to select an image and proceed through the steps of processing and counting the colonies.

## Contributing
Contributions are welcome!

You can help by:

- Reporting issues
- Suggesting improvements
- Adding new features through pull requests

## License
This project is licensed under the MIT License.
