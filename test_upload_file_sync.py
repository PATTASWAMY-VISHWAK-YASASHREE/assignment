import asyncio
from fastapi import UploadFile
from io import BytesIO

async def main():
    content = b"a" * 100
    f = UploadFile(filename="test", file=BytesIO(content))

    # Check sync seek/tell on underlying file
    f.file.seek(0, 2)
    size = f.file.tell()
    print(f"Size: {size}")

    f.file.seek(0)

    # Check if we can read
    print(f.file.read(10))

if __name__ == "__main__":
    asyncio.run(main())
