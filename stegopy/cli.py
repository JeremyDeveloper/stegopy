import argparse, os, sys, random
from stegopy.image import _core as image_core
from stegopy.audio import _core as audio_core
from stegopy.utils import _is_audio_file, _is_image_file, _estimate_capacity
from stegopy.errors import InvalidStegoDataError, PayloadTooLargeError, UnsupportedFormatError
from PIL import Image

def stegosaurus():
    STEGOSAUR_QUOTES = [
        "they found me rocking back and forth whispering 'bit shift left'.",
        "hospitalized once, embedded forever.",
        "I hardcoded my trauma into RGB.",
        "I don't need therapy, I have steganography.",
        "I put my feelings in the pixels.",
        "I encode my pain in the LSB.",
        "the doctors said 'get rest' so I wrote 40 unit tests.",
        "yes I cried while debugging. no, I regret nothing.",
        "built during a mental breakdown. perfected during the next one.",
        "I put the 'fun' in dysfunctional.",
        "my stego logic is more stable than I am.",
        "compression? no. psychosis? yes.",
        "I optimized it so hard I forgot to eat for 4 days.",
        "autistic fixation turned python package. you're welcome.",
        "this passed 40 tests and failed 5 social cues.",
        "flapping my hands over bit alignment.",
        "if you interrupt this compile, I will melt down.",
        "they asked me to explain my emotions. I wrote a steganography library.",
        "Bring your own XOR."
    ]

    print(f"""
              __
             / _)
     _.----._/ /
   /         /
__|  (|_|_|_|
  `--' `-'-'   

    🦕 stegopy: {random.choice(STEGOSAUR_QUOTES)}
    """)

def main():
    parser = argparse.ArgumentParser(
        prog="stegopy",
        description="🧠 stegopy: zero-bloat steganography for images & audio",
        add_help=False,
        usage="stegopy [message] <-e/--encode | -d/--decode> <-i input> [-o output] [--channel r/g/b] [--region center/topleft/topright/bottomleft/bottomright] [--alpha]"
    )

    parser.add_argument("payload", nargs="?", help="Payload to encode (required with --encode)")
    parser.add_argument("-e", "--encode", action="store_true", help="Encode mode")
    parser.add_argument("-d", "--decode", action="store_true", help="Decode mode")
    parser.add_argument("-i", "--input", required=False, help="Input file (image/audio)")
    parser.add_argument("-o", "--output", required=False, help="Output file (encode only)")
    parser.add_argument("--channel", choices=["r", "g", "b"], help="Color channel for image")
    parser.add_argument("--alpha", action="store_true", help="Use alpha channel for image")
    parser.add_argument("--region", choices=["center", "topleft", "topright", "bottomleft", "bottomright"], help="Use a specific image region")
    parser.add_argument("-c", "--capacity", action="store_true", help="Estimate how many UTF-8 characters can be embedded in the input")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    
    args = parser.parse_args()
    
    stegosaurus()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not args.input:
        print("❌ You must provide an input file.")
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"❌ File not found: {args.input}")
        sys.exit(1)
        
    if args.capacity:
        try:
            cap = _estimate_capacity(args.input, region=args.region, channel=args.channel, alpha=args.alpha)
            print(f"🧠 Estimated capacity: {cap} UTF-8 characters")
        except Exception as e:
            print(f"❌ Capacity estimation failed: {e}")
        return

    if args.encode:
        if not args.payload:
            print("❌ You must provide a payload when encoding.")
            sys.exit(1)
        if not args.input or not args.output:
            print("❌ Encoding requires both --input and --output.")
            sys.exit(1)

        try:
            if _is_audio_file(args.input):
                audio_core.encode(args.input, args.output, args.payload)
            elif _is_image_file(args.input):
                image_core.encode(
                    args.input, args.output, args.payload,
                    region=args.region, channel=args.channel, alpha=args.alpha
                )
            else:
                print("❌ Unsupported file type for encoding. Only images and audio files are supported.")
                sys.exit(1)
        except PayloadTooLargeError:
            print("❌ Encoding failed, the message may be too large for the input file. Try a smaller message or use the capacity estimation tool via -c.")
            sys.exit(1)
        except UnsupportedFormatError:
            print("❌ Unsupported file format. Please provide a supported image or audio file format, such as a PNG, WEBP, WAV, AIFF, or any other supported format.")
            sys.exit(1)
        return

    if args.decode:
        if not args.input:
            print("❌ You must provide an input file when decoding.")
            sys.exit(1)

        try:
            if _is_audio_file(args.input):
                message = audio_core.decode(args.input)
            elif _is_image_file(args.input):
                message = image_core.decode(
                    args.input,
                    region=args.region, channel=args.channel, alpha=args.alpha
                )
            else:
                print("❌ Unsupported file type for decoding. Only images and audio files are supported.")
                sys.exit(1)
        except InvalidStegoDataError:
            print(f"❌ Decoding failed, the message may be corrupted or incomplete.")
            sys.exit(1)
        except UnsupportedFormatError:
            print("❌ Unsupported file format. Please provide a supported image or audio file format, such as a PNG, WEBP, WAV, AIFF, or any other supported format.")
            sys.exit(1)

        if isinstance(message, Image.Image):
            if not args.output:
                print("❌ Decoded payload is an image, but no --output file was specified.")
                sys.exit(1)
            message.save(args.output)
            return

        print(f"-> {message}")
        return

    print("❌ You must specify either --encode or --decode.")
    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
