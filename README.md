# MPCPy

Exemple d'un reproductor MP3 amb Python basat amb MPD i MPC per GNU Linux.

## Requeriments

- GNU Linux: Ubuntu 22.04.1 LTS
- python >= 3.8
- MPD: Music Player Daemon 0.23.5 (0.23.5)
- MPC: A minimalist command line interface to MPD

## MPD
https://www.musicpd.org/
https://mpd.readthedocs.io/en/stable/user.html

- apt install mpd
- configure /etc/mpd.conf
```
music_directory		"/home/aleon/Música"
playlist_directory		"/home/aleon/playlists"
...
```
- load mp3 music in music_directory
- sudo systemctl enable mpd
- sudo systemctl start mpd
- sudo systemctl status mpd
- reboot if is necessary

## MPC
https://www.musicpd.org/clients/mpc/
https://www.musicpd.org/doc/mpc/html/

- apt install mpc
- mpc update
- mpc ls
- mpd add /
- mpc play


## Run

