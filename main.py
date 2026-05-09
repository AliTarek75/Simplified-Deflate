import argparse
from bitwriter import compress
from decompressor import decompress
import time

def main():
    # Parser setup
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--compress", action="store_true")
    parser.add_argument("-d", "--decompress", action="store_true")
    parser.add_argument("filename")
    args = parser.parse_args()

    print()

    # Deompression
    if args.decompress:

        # If the user gave a non sdfl file to decompress
        if not args.filename.endswith('.sdfl'):
            parser.error("File must end in '.sdfl' to decompress")

        print(f"Decompressing {args.filename}...")
        
        start = time.time()

        with open(args.filename, "rb") as file:
            data = file.read()
        
        # Convert the data to a bitstring instead of a bytestring 
        # because that's what the decompress function work with
        bit_string = "".join(format(byte, '08b') for byte in data)
        decompressed_data = decompress(bit_string)

        with open(args.filename[:-5], "wb") as file:
            file.write(decompressed_data)

        end = time.time()

        print(f"Finished in: \t {end - start:.2f}s")

    # Compression
    elif args.compress:

        print(f"Compressing {args.filename}...")

        start = time.time()

        with open(args.filename, "rb") as file:
            data = file.read()

        compressed_data = compress(data)

        # Calculate the original and new file sizes and the percentage
        original_size = len(data)
        compressed_size = len(compressed_data)
        diff = abs(original_size - compressed_size)
        percentage = (diff / original_size) * 100   
            
        with open(args.filename + ".sdfl", "wb") as file:
            file.write(compressed_data)

        end = time.time()

        print(f"Finished in: \t {end - start:.2f}s")
        print(f"Original: \t {original_size:,} bytes")
        print(f"Compressed: \t {compressed_size:,} bytes")
        
        # Based on the difference, if the difference is negative that means the file got expanded instead of compress
        # this mostly happens with already compressed files or very small files 
        if diff > 0:
            print(f"Result: \t Shrunk by {percentage:.2f}%")
        elif diff < 0:
            print(f"Result: \t Expanded by {percentage:.2f}% (Inefficient)")
        else:
            print(f"Result: \t No change in file size")
    
    # User didn't give either flags
    else:
        parser.error("You must use either -c to compress or -d to decompress.")

    print()

if __name__ == "__main__":
    main()