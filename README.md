# Simplified DEFLATE Compressor & Decompressor

A Python-based file compressor and decompressor inspired by the core ideas of DEFLATE.  
This project works with input files as raw bytes and converts them with an LZ77-based compression pipeline, followed by DEFLATE-style symbols, canonical Huffman coding, The final correctness goal is: `decompress(compress(data)) = data`, byte-for-byte. This is not a full .gz implementation. It doesn't use the official GZIP header,
CRC32, or official DEFLATE block structure.


## How It Works
  ### The compression pipeline is:
  Input Bytes → LZ77 Tokens → DEFLATE Symbols + Extra Bits → Canonical Huffman Bitstream
- **Stage 1: LZ77 Pattern Detection**  
  The compressor scans the input as bytes and uses a hash-based match search to replaces repeated sequences with either:
  - `Literal(byte)`
  - `Match(length, distance)`

- **Stage 2: DEFLATE Symbols and Extra Bits**  
  Tokens are mapped into two separate alphabets:
  - Literal/Length (0–285): Includes literal bytes (0–255), the EndEvent marker (256), and length symbols representing ranges (257–285).
  - Distance (0–29): Represents match distances from 1 to 32,768 (also in ranges).

  Extra bits are used to specify exact values within these ranges, minimizing the number of unique Huffman symbols needed.
- **Stage 3: Canonical Huffman Coding**  
  Instead of storing a complex tree structure, This uses Canonical Huffman Codes. These are generated based on the bit-lengths that are calculated from the tree itself, the coding process is deterministic. If two decoders have the same list of bit-lengths, they will reconstruct the exact same tree. Thus we only need to store the lengths which minimizes the amount of data in the header.

- **Stage 4: Custom Header and Payload**  
  The compressed file stores the Huffman code-length tables and the encoded payload in an `.sdfl` format.

### Decompression  
  The decoder reads the header, reconstructs the canonical Huffman codes, decodes the payload, and restores the original byte stream. This process is simpler so most of the work is written within a single function.

## Usage

### Compress a file
To compress a file, use the c flag then provide a filename to compress. This generates a <filename>.sdfl file in the same directory.
```bash
python main.py -c example.txt
```

This creates a compressed file in the same directory as the input file with the extension:

```text
example.txt.sdfl
```

### Decompress a file
```bash
python main.py -d example.txt.sdfl
```

This creates the decompressed output file in the same directory as the compressed input file.  
For example, decompressing `data.txt.sdfl` produces `data.txt`.

## Inputs
The compressor accepts any file as a raw byte stream.  
It does not treat the file as text internally, so binary files and text files are handled in the same way.

## Outputs & Metrics
* **Compressed Output:** A `.sdfl` file containing:
  - Huffman code-length tables in the header and Huffman-coded payload with the raw extra bits
  - The overall time taken and compression percentage
* **Decompressed Output:** The exact original file restored byte-for-byte and time metric

## Example Output
The results speed will vary and depend merely on the device specs. This example was performed on a high-spec machine.

```text
Compressing enwik8...
Finished in:     319.63s
Original:        100,000,000 bytes
Compressed:      37,583,500 bytes
Result:          Shrunk by 62.42%
```
```
Decompressing enwik8.sdfl...
Finished in:     56.21s
```

## Project Notes
This project uses as constants:
- a 32 KB LZ77 sliding window
- minimum match length of 3
- maximum match length of 258

## Authors
This project was a collaborative effort

* **Ali Tarek ([@AliTarek75](https://github.com/AliTarek75))** – DEFLATE Symbol Mapping & Decompression Engine.
* **Ahmed Abdelrazek ([@Abdelrazek0](https://github.com/Abdelrazek0))** – LZ77 Pattern Detection & Final Header and File Assembly.
* **John Bassem ([@fighterzi-eng](https://github.com/fighterzi-eng))** – Canonical Huffman Implementation & Tree Construction.