rmdir /s /q dist
python ./setup.py sdist
for /R dist %%F in (*.tar.gz) do pip3 install "%%F"