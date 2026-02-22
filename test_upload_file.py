import asyncio
from fastapi import UploadFile
from io import BytesIO

async def main():
    content = b"a" * 100
    f = UploadFile(filename="test", file=BytesIO(content))

    # Check seek/tell
    await f.seek(0, 2)
    size = await f.tell()
    print(f"Size: {size}")

    await f.seek(0)

    # Check if we can pass file.file to read
    print(f.file.read(10))

if __name__ == "__main__":
    asyncio.run(main())
