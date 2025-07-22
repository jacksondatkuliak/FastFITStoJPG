# FastFITStoJPG is designed to import a FITS cube, grab the last exposure,
# autostretch the image, and save it to a jpeg. Optionally, it should be
# able to also send that jpg to a control server using a HTTP REST request

# Remember to activate virtual environment 
# imports
import argparse
from astropy.io import fits
from PIL import Image
import numpy as np

def float_100(value):
    ivalue = float(value)
    if ivalue < 0 or ivalue > 100:
        raise argparse.ArgumentTypeError(f"Low, high stretch %, and arcsinh boost must be in range 0-100, got {value}")
    return ivalue

def int_100(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 100:
        raise argparse.ArgumentTypeError(f"JPEG quality must be in range 1-100, got {value}")
    return ivalue

def int_hdu(value):
    ivalue = int(value)
    if ivalue < -1:
        raise argparse.ArgumentTypeError(f"HDU number must be >= -1, got {value}")
    return ivalue

# stretch the image
def stretch_image(image, low_pct, high_pct, mode, boost):
    # stretch if none is not selected
    if (mode != "none"):
        low = np.nanpercentile(image, low_pct)
        high = np.nanpercentile(image, high_pct)
        scaled = np.clip((image - low) / (high - low), 0, 1)

    if mode == 'arcsinh':
        # Apply arcsinh stretch: scaled to [0, π/2] range
        scaled = np.arcsinh(boost * scaled) / np.arcsinh(boost)
    elif mode == 'linear':
        pass  # Already linear/none
    else:
        raise ValueError(f"Unsupported stretch mode: {mode}")

    return (scaled * 255).astype(np.uint8)

# program entry point
def main(fits_file, output_file, low_pct, high_pct, stretch_mode, boost, quality, hdu):
    with fits.open(fits_file, memmap=False) as hdul:
        data = hdul[hdu].data  # Get last frame from cube

    # stretch image (or don't)
    if (stretch_mode != "none"):
        img_array = stretch_image(data, low_pct, high_pct, stretch_mode, boost)
    else:
        img_array = (data * 255).astype(np.uint8)
    # print to jpeg
    Image.fromarray(img_array).save(output_file, format='JPEG', quality=quality)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert FITS to JPEG with auto-stretching")
    parser.add_argument("--input", type=str, default="input.fits", help="Path to input FITS file (default input.fits)")
    parser.add_argument("--output", type=str, default="output.jpg", help="Path to output JPEG file (default output.jpg)")
    parser.add_argument("--low", type=float_100, default=0.5, help="Low percentile for stretch (0-100, default: 0.5)")
    parser.add_argument("--high", type=float_100, default=99.5, help="High percentile for stretch (0-100, default: 99.5)")
    parser.add_argument("--stretch", choices=["linear", "arcsinh", "none"], default="linear", help="Stretch mode: linear, arcsinh, or none (default linear)")
    parser.add_argument("--boost", type=float_100, default=10,help="Arcsinh boost factor, only used if arcsinh stretch is selected (0-100, default 10)")
    parser.add_argument("--quality", type=int_100, default=80, help="JPEG quality (1-100, default: 80)")
    parser.add_argument("--hdu", type=int_hdu, default=-1, help="FITS HDU to convert (-1-INT_MAX, default: -1 (last HDU))")
    args = parser.parse_args()

    main(args.input, args.output, args.low, args.high, args.stretch, args.boost, args.quality, args.hdu)