FROM fedora:26

# run dnf to have some cache to work with
RUN dnf check-update || exit 0

ADD bug.py /usr/local/bin

ENTRYPOINT python3 /usr/local/bin/bug.py
